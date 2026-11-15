from scripts.index_publications import prepare_document, reconstruct_abstract


def test_reconstruct_abstract_returns_none_when_empty():
    assert reconstruct_abstract(None) is None
    assert reconstruct_abstract({}) is None


def test_reconstruct_abstract_orders_words_by_position():
    inverted = {"zeta": [0], "alpha": [1], "mid": [2]}
    assert reconstruct_abstract(inverted) == "zeta alpha mid"


def test_reconstruct_abstract_handles_repeated_words():
    inverted = {"the": [0, 2], "sky": [1]}
    assert reconstruct_abstract(inverted) == "the sky the"


def test_prepare_document_drops_mongo_id_and_extracts_fields():
    publication = {
        "_id": "https://openalex.org/W1",
        "id": "https://openalex.org/W1",
        "title": "A Title",
        "authorships": [
            {
                "author": {"display_name": "Alice"},
                "institutions": [{"display_name": "MIT", "country_code": "US"}],
            }
        ],
        "concepts": [{"display_name": "Physics"}],
        "topics": [{"display_name": "Climate"}],
        "abstract_inverted_index": {"hello": [0], "world": [1]},
    }

    document = prepare_document(publication)

    assert "_id" not in document
    assert document["author_names"] == ["Alice"]
    assert document["institution_names"] == ["MIT"]
    assert document["country_codes"] == ["US"]
    assert document["concept_names"] == ["Physics"]
    assert document["topic_names"] == ["Climate"]
    assert document["abstract"] == "hello world"


def test_prepare_document_handles_missing_authorships():
    document = prepare_document({"_id": "W2", "id": "W2"})

    assert document["author_names"] == []
    assert document["institution_names"] == []
    assert document["country_codes"] == []
    assert document["concept_names"] == []
    assert document["abstract"] is None
