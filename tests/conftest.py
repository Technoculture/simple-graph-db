import pytest
from unittest.mock import patch


@pytest.fixture
def mock_atomic():
    with patch("libsql_graph_db.database.atomic") as mock_atomic:
        yield mock_atomic


@pytest.fixture
def mock_db_connection_and_cursor():
    with patch("libsql_graph_db.database.libsql.connect") as mock_connect:
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        yield mock_connection, mock_cursor


@pytest.fixture
def mock_embeddings_model():
    with patch(
        "libsql_graph_db.database.embed_obj.get_embedding"
    ) as mock_get_embedding:
        # Define fixed embeddings for testing
        fixed_embeddings = {
            '{"name": "Alice", "age": 30}': [0.1, 0.2, 0.3],
            '{"name": "Peri", "age": "90"}': [0.4, 0.5, 0.6],
            '{"name": "Pema", "age": "66"}': [0.7, 0.8, 0.9],
            '{"name": "Bob", "age": 35}': [0.11, 0.22, 0.33],
        }
        # Mock the get_embedding function to return fixed embeddings
        mock_get_embedding.side_effect = lambda x: fixed_embeddings.get(x, [])

        yield mock_get_embedding
