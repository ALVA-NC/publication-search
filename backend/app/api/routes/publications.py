
from fastapi import APIRouter, HTTPException, Query
from elasticsearch import NotFoundError, ApiError, ConnectionError as ElasticsearchConnectionError

from app.database.elasticsearch import es, INDEX_NAME


router = APIRouter(
    prefix="/api/publications",
    tags=["Publications"]
)


@router.get("")
def search_publications(
    q: str | None = None,
    author: str | None = None,
    institution: str | None = None,
    country: str | None = None,
    concept: str | None = None,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
):
    """Search and filter publications using Elasticsearch."""

    filters = []

    if author:
        filters.append({
            "term": {"author_names.keyword": author}
        })

    if institution:
        filters.append({
            "term": {"institution_names.keyword": institution}
        })

    if country:
        filters.append({
            "term": {"country_codes": country.upper()}
        })

    if concept:
        filters.append({
        "term": {
            "concept_names.keyword": concept}
        })

    if q:
        search_query = {
            "multi_match": {
                "query": q,
                "fields": [
                    "title^3",
                    "author_names",
                    "institution_names",
                    "country_codes",
                    "concept_names",
                    "topic_names"
                ],
                "type": "best_fields",
                "fuzziness": "AUTO"
            }
        }
    else:
        search_query = {"match_all": {}}

    body = {
        "query": {
            "bool": {
                "must": [search_query],
                "filter": filters
            }
        },
        "sort": (
            [{"_score": "desc"}, {"publication_date": "desc"}]
            if q
            else [{"publication_date": "desc"}]
        )
    }

    try:
        result = es.search(
            index=INDEX_NAME,
            body=body,
            from_=(page - 1) * per_page,
            size=per_page
        )

    except ElasticsearchConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Could not connect to Elasticsearch"
        )

    except ApiError:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while searching publications"
        )

    hits = result["hits"]["hits"]
    total = result["hits"]["total"]["value"]

    return {
        "results": [
            {
                "id": hit["_id"],
                **hit["_source"]
            }
            for hit in hits
        ],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page
        }
    }


@router.get("/{work_id}")
def get_publication(work_id: str):
    """Retrieve a complete publication from Elasticsearch."""

    publication_id = f"https://openalex.org/{work_id}"

    try:
        result = es.get(
            index=INDEX_NAME,
            id=publication_id
        )

        return {
            **result["_source"],
            "id": result["_id"]
        }

    except NotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Publication not found"
        )

    except ElasticsearchConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Could not connect to Elasticsearch"
        )

    except ApiError:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving publication"
        )

