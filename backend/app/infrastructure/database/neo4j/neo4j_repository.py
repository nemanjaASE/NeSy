import logging
from neo4j import AsyncGraphDatabase
from app.core import settings
from app.domain import RawDiseaseMatch, SymptomOntologyData
from app.core import timed
from .constants import HAS_SYMPTOM_REL, GET_ONTOLOGY_SYMPTOMS, INFERENCE_QUERY
from .queries.get_query import get_query

logger = logging.getLogger(__name__)

class Neo4jRepository:
    """
    Data access layer for the Neo4j graph database.

    Responsible for establishing and closing the database connection,
    fetching ontology symptom data, and executing diagnostic inference
    queries. Contains no business logic — it serves purely as a
    translator between the application domain and the graph database.
    """

    def __init__(self):
        self.uri      = settings.NEO4J_URI
        self.user     = settings.NEO4J_USERNAME
        self.password = settings.NEO4J_PASSWORD
        self.driver   = None

    async def connect(self) -> None:
        """
        Establish and verify the connection to the Neo4j database.

        Called once during application startup via the lifespan handler.

        Raises:
            Exception: If the driver cannot connect or connectivity
                       verification fails.
        """
        try:
            self.driver = AsyncGraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
            await self.driver.verify_connectivity()
            logger.info(f"Connected to Neo4j")
        except Exception as e:
            logger.exception(f"Failed to connect to Neo4j")
            raise

    async def close(self) -> None:
        """
        Close the active Neo4j database connection.

        Called once during application shutdown via the lifespan handler.
        Safe to call even if the driver was never initialized.
        """
        if self.driver:
            await self.driver.close()
            logger.debug("Neo4j connection closed")

    @timed("Fetch Ontology Symptoms")
    async def get_ontology_symptoms(self) -> list[SymptomOntologyData]:
        """
        Fetch all symptoms and their pre-computed embeddings from the knowledge graph.

        Ontology symptoms are used as the reference space for semantic matching
        against patient-reported symptoms. Nodes without embeddings are excluded
        from the result to ensure matching integrity.

        Returns:
            list[SymptomOntologyData]: Ontology symptoms with their labels and
            embedding vectors. Returns an empty list on failure.
        """
        try:
            query = get_query(GET_ONTOLOGY_SYMPTOMS)

            async with self.driver.session() as session:
                result = await session.run(query)
                symptoms = [
                    SymptomOntologyData(label=r["label"], embedding=r["embedding"])
                    async for r in result if r["embedding"]
                ]

            logger.debug(f"Fetched {len(symptoms)} ontology symptom from neo4j.")
            return symptoms

        except Exception as e:
            logger.exception(f"Failed to fetch ontology symptoms")
            return []

    @timed("Infer Diseases")
    async def infer_diseases(
        self,
        present_symptoms: list[str],
        absent_symptoms:  list[str],
        min_match: int = 2,
    ) -> list[RawDiseaseMatch]:
        """
        Execute the diagnostic inference Cypher query against the knowledge graph.

        Matches the patient's ontologically mapped symptoms against disease
        definitions stored in the graph. Returns raw scored candidates for
        further processing by the scoring and ranking pipeline.

        Args:
            present_symptoms: Ontological symptom terms the patient reports having.
            absent_symptoms:  Ontological symptom terms the patient explicitly denies.
            min_match:        Minimum number of matched symptoms required for a disease
                              to qualify as a candidate. Defaults to 2.

        Returns:
            list[RawDiseaseMatch]: Raw disease candidates with match scores and
            symptom coverage data. Returns an empty list if no present symptoms
            are provided or if the query fails.
        """
        if not present_symptoms:
            logger.debug("Inference skipped: no present symptoms provided.")
            return []

        try:
            query = get_query(INFERENCE_QUERY)

            logger.debug("Executing inference query")

            async with self.driver.session() as session:
                result = await session.run(
                    query,
                    has_symptom=HAS_SYMPTOM_REL,
                    present_symptoms=present_symptoms,
                    absent_symptoms=absent_symptoms,
                    min_match=min_match
                )
                records = await result.data()

            logger.info(f"Inference returned {len(records)} candidates")
            return [RawDiseaseMatch(**r) for r in records]

        except Exception as e:
            logger.error(f"Failed to execute inference query")
            return []