from neo4j import AsyncGraphDatabase
from app.core import logger, settings
from typing import List
from app.domain import SymptomOntologyData, RawDiseaseMatch
from .queries import get_query

class Neo4jRepository:
    """
    Handles connection and raw queries to the Neo4j Graph Database.
    """

    def __init__(self):
        self.uri = settings.NEO4J_URI
        self.user = settings.NEO4J_USERNAME
        self.password = settings.NEO4J_PASSWORD
        self.driver = None

    async def connect(self):
        """Establish the connection to the database."""
        try:

            self.driver = AsyncGraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password))


            await self.driver.verify_connectivity()
            logger.info(f"Successfully connected to Neo4j ({settings.ENVIRONMENT} mode).")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {str(e)}")
            raise

    async def close(self):
        """Close the database connection."""
        if self.driver:
            await self.driver.close()
            logger.info("Neo4j connection closed.")

    async def get_ontology_symptoms(self) -> List[SymptomOntologyData]:
        """
        Fetches all symptoms and their pre-computed embeddings from the graph.
        Returns:
            A list of tuples, where each tuple contains the symptom label and its embedding vector.
        """
        try:
            query = get_query("get_ontology_symptoms")

            async with self.driver.session() as session:
                result = await session.run(query)
                return [
                    SymptomOntologyData(
                        label=r["label"], 
                        embedding=r["embedding"]
                    ) async for r in result if r["embedding"]
                ]
        except Exception as e:
            logger.error(f"Error fetching symptoms from Neo4j: {str(e)}")
            return []
        
    async def infer_diseases(
        self, 
        present_symptoms: List[str], 
        absent_symptoms: List[str], 
        min_match: int = 2, 
        has_symptom_rel: str = "http://purl.obolibrary.org/obo/RO_0002452",
        top_k: int = 5,
        top_excluded: int = 3
    ) -> List[RawDiseaseMatch]:
        """
        Executes the inference Cypher query to find matching diseases.
        """
        if not present_symptoms and not absent_symptoms:
            logger.warning("No symptoms provided for inference.")
            return []
        try:
            query = get_query("infer_diseases")
            
            async with self.driver.session() as session:
                result = await session.run(
                    query, 
                    has_symptom=has_symptom_rel, 
                    present_symptoms=present_symptoms,
                    absent_symptoms=absent_symptoms, 
                    min_match=min_match
                )

                records = await result.data()
            
            return [RawDiseaseMatch(**r) for r in records]
        
        except Exception as e:
            logger.error(f"Error executing inference query: {str(e)}")
            return []