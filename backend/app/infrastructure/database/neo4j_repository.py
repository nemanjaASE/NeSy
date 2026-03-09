from neo4j import GraphDatabase
from app.core import logger, settings
from typing import Any, Dict, List, Tuple

from .queries import get_query

class Neo4jRepository:
    """
    Handles connection and raw queries to the Neo4j Graph Database.
    """

    def __init__(self):
        self.uri = settings.NEO4J_URL
        self.user = settings.NEO4J_USERNAME
        self.password = settings.NEO4J_PASSWORD
        self.driver = None

    def connect(self):
        """Establish the connection to the database."""
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            self.driver.verify_connectivity()
            logger.info("Successfully connected to Neo4j database.")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {str(e)}")
            raise

    def close(self):
        """Close the database connection."""
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed.")

    async def get_ontology_symptoms(self) -> List[Tuple[str, List[float]]]:
        """
        Fetches all symptoms and their pre-computed embeddings from the graph.
        Returns:
            A list of tuples, where each tuple contains the symptom label and its embedding vector.
        """
        try:
            query = get_query("get_ontology_symptoms")

            with self.driver.session() as session:
                result = session.run(query)

                return [(r["label"], r["embedding"]) for r in result if r["embedding"]]
        except Exception as e:
            logger.error(f"Error fetching symptoms from Neo4j: {str(e)}")
            return []
        
    async def infer_diseases(
        self, 
        mapped_symptoms: List[str], 
        min_match: int = 1, 
        has_symptom_rel: str = "http://purl.obolibrary.org/obo/RO_0002452"
    ) -> List[Dict[str, Any]]:
        """
        Executes the inference Cypher query to find matching diseases.
        """
        if not mapped_symptoms:
            logger.warning("No mapped symptoms provided for inference.")
            return []
        try:
            query = get_query("infer_diseases")
            
            with self.driver.session() as session:
                result = session.run(
                    query, 
                    has_symptom=has_symptom_rel, 
                    symptoms=mapped_symptoms, 
                    min_match=min_match
                )

                records = [dict(r) for r in result]
                logger.info(f"Inference query executed successfully. Found {len(records)} potential diseases.")
                return records

        except Exception as e:
            logger.error(f"Error executing inference query: {str(e)}")
            return []    