
import logging

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from app.config import settings
from app.database.mongodb import publications, close_connection
from app.database.elasticsearch import es, INDEX_NAME

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Avoid logging request URLs and query parameters unnecessarily.
logging.getLogger("elastic_transport").setLevel(logging.WARNING)


def reconstruct_abstract(inverted_index: dict | None) -> str | None:
    """Convert OpenAlex's inverted abstract index into normal text."""

    if not inverted_index:
        return None

    words = []

    for word, positions in inverted_index.items():
        for position in positions:
            words.append((position, word))

    words.sort(key=lambda item: item[0])

    return " ".join(word for _, word in words)


def create_elasticsearch_index(es: Elasticsearch) -> None:
    """Create the publications index with appropriate field mappings."""

    if es.indices.exists(index=INDEX_NAME):
        logger.info("Deleting existing index: %s", INDEX_NAME)
        es.indices.delete(index=INDEX_NAME)

    mapping = {
        "properties": {
            "id": {"type": "keyword"},
            "title": {
                "type": "text",
                "fields": {"keyword": {"type": "keyword"}}
            },
            "publication_date": {"type": "date"},
            "doi": {"type": "keyword"},
            "cited_by_count": {"type": "integer"},
            "abstract": {"type": "text"},

            # Keep the original inverted index in _source,
            # but do not create thousands of separate mapped fields.
            "abstract_inverted_index": {
                "type": "object",
                "enabled": False
            },

            # Convenient fields for searching and filtering.
            "author_names": {
                "type": "text",
                "fields": {"keyword": {"type": "keyword"}}
            },
            "institution_names": {
                "type": "text",
                "fields": {"keyword": {"type": "keyword"}}
            },
            "country_codes": {"type": "keyword"},
            "concept_names": {
                "type": "text",
                "fields": {"keyword": {"type": "keyword"}}
            },
            "topic_names": {
                "type": "text",
                "fields": {"keyword": {"type": "keyword"}}
            }
        }
    }

    es.indices.create(
        index=INDEX_NAME,
        mappings=mapping
    )

    logger.info("Created Elasticsearch index: %s", INDEX_NAME)


def prepare_document(publication: dict) -> dict:
    """
    Preserve the complete OpenAlex record and add
    convenient fields for searching and filtering.
    """

    # Keep the original record, except MongoDB's internal _id.
    document = {
        key: value
        for key, value in publication.items()
        if key != "_id"
    }

    authorships = publication.get("authorships", [])

    author_names = []
    institution_names = []
    country_codes = []

    for authorship in authorships:
        author = authorship.get("author") or {}

        if author.get("display_name"):
            author_names.append(author["display_name"])

        for institution in authorship.get("institutions", []):
            if institution.get("display_name"):
                institution_names.append(
                    institution["display_name"]
                )

            if institution.get("country_code"):
                country_codes.append(
                    institution["country_code"]
                )

    concepts = [
        concept["display_name"]
        for concept in publication.get("concepts", [])
        if concept.get("display_name")
    ]

    topics = [
        topic["display_name"]
        for topic in publication.get("topics", [])
        if topic.get("display_name")
    ]

    # Add fields specifically intended for searching/filtering.
    document["author_names"] = list(set(author_names))
    document["institution_names"] = list(set(institution_names))
    document["country_codes"] = list(set(country_codes))
    document["concept_names"] = concepts
    document["topic_names"] = topics

    # Add a readable abstract while retaining the original
    # abstract_inverted_index in the document.
    document["abstract"] = reconstruct_abstract(
        publication.get("abstract_inverted_index")
    )

    return document


def index_publications() -> None:

    try:
        if not es.ping():
            raise ConnectionError("Could not connect to Elasticsearch")

        # Recreate the index using the updated mapping.
        create_elasticsearch_index(es)

        def generate_actions():
            for publication in publications.find({}):
                publication_id = publication["_id"]

                yield {
                    "_index": INDEX_NAME,
                    "_id": publication_id,
                    "_source": prepare_document(publication)
                }

        success, errors = bulk(
            es,
            generate_actions(),
            chunk_size=100,
            raise_on_error=False
        )

        logger.info("Successfully indexed %s publications", success)

        if errors:
            failed_count = errors if isinstance(errors, int) else len(errors)
            logger.error(
                "Failed to index %s documents",
                failed_count
            )

    finally:
        es.close()
        close_connection()


if __name__ == "__main__":
    index_publications()
