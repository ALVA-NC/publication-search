
from elasticsearch import Elasticsearch

from app.config import settings


INDEX_NAME = "publications"

es = Elasticsearch(settings.elasticsearch_url)
