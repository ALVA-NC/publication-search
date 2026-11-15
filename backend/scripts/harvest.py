
import logging
import time

import httpx
from pymongo import ReplaceOne

from app.config import settings
from app.database.mongodb import (
    publications,
    close_connection,
)


OPENALEX_API_URL = "https://api.openalex.org/works"

MAX_RECORDS = 1000
PAGE_SIZE = 100

SEARCH_TERM = "climate change"

FILTER = (
    "institutions.country_code:DK,"
    "from_publication_date:2025-01-01,"
    "to_publication_date:2025-12-31"
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def fetch_page(
    client: httpx.Client,
    page: int
) -> dict:
    """Fetch one page of publications from OpenAlex."""

    params = {
        "search": SEARCH_TERM,
        "filter": FILTER,
        "per_page": PAGE_SIZE,
        "page": page,
        "api_key": settings.openalex_api_key,
    }

    response = client.get(OPENALEX_API_URL, params=params)
    response.raise_for_status()

    return response.json()


def save_publications(works: list[dict]) -> int:
    """Upsert publications into MongoDB."""

    if not works:
        return 0

    operations = []

    for work in works:
        work_id = work.get("id")

        if not work_id:
            logger.warning("Skipping publication without an ID")
            continue

        document = {
            **work,
            "_id": work_id,
        }

        operations.append(
            ReplaceOne(
                {"_id": work_id},
                document,
                upsert=True
            )
        )

    if not operations:
        return 0

    result = publications.bulk_write(
        operations,
        ordered=False
    )

    return result.upserted_count + result.modified_count


def harvest() -> None:
    """Retrieve and store up to MAX_RECORDS publications."""
    page = 1
    total_fetched = 0

    logger.info("Starting OpenAlex harvesting")

    try:
        with httpx.Client(timeout=30.0) as client:

            while total_fetched < MAX_RECORDS:

                logger.info("Fetching page %s", page)

                data = fetch_page(client, page)

                works = data.get("results", [])

                if not works:
                    logger.info("No more publications found")
                    break

                remaining = MAX_RECORDS - total_fetched
                works = works[:remaining]

                saved = save_publications(works)

                total_fetched += len(works)

                logger.info(
                    "Fetched %s publications; %s inserted or updated",
                    len(works),
                    saved
                )

                if len(data.get("results", [])) < PAGE_SIZE:
                    break

                page += 1
                time.sleep(0.2)

        logger.info(
            "Harvesting completed. Total publications fetched: %s",
            total_fetched
        )

    except httpx.HTTPStatusError as error:
        logger.error(
            "OpenAlex returned HTTP %s: %s",
            error.response.status_code,
            error.response.text
        )
        raise

    except httpx.RequestError as error:
        logger.error("Error communicating with OpenAlex: %s", error)
        raise

    finally:
        close_connection()


if __name__ == "__main__":
    harvest()
