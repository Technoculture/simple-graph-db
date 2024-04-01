#! /usr/bin/python
import os
import logging
from dotenv import load_dotenv
from libsql_graph_db import database as db
from libsql_graph_db import natural


def main(url, token):
    # Initialize the Database
    db.initialize(url, token)

    # Testing insert query into graph db
    nl_query = "increased thirst, weight loss, increased hunger, frequent urination etc. are all symptoms of diabetes."
    graph = natural.insert_into_graph(query=nl_query)

    logging.info("Nodes in the Knowledge Graph: \n")
    for node in graph.nodes:
        logging.info(f"ID: {node.id}, Label: {node.label}, Body: {node.body}")

    logging.info("Edges in the Knowledge Graph: \n")
    for edge in graph.edges:
        logging.info(
            f"Source: {edge.source}, Target: {edge.target}, Label: {edge.label}"
        )

    # Testing search query from graph db
    search_query = "I am losing my weight too frequent."
    knowledge_graph = natural.search_from_graph(search_query)

    logging.info(f"Knowledge Graph: \n{knowledge_graph}")


if __name__ == "__main__":
    load_dotenv()
    db_url = os.getenv("LIBSQL_URL")
    auth_token = os.getenv("LIBSQL_AUTH_TOKEN")

    logging.basicConfig(
        level=logging.DEBUG,
        filemode="w",
        filename="./log/nl_interface.log",
    )

    main(db_url, auth_token)