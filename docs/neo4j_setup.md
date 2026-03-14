# 🔧 Neo4j Desktop Setup & n10s Installation

## 🧠 What is Neosemantics (n10s)?

Neosemantics is an extension that allows Neo4j to store and query data in RDF format. It is the engine that processed our medical ontologies, transforming complex OWL logic into a navigable graph of Diseases and Symptoms.

Before you can run any Cypher queries for ontologies, you must prepare your Neo4j instance.

**1. Create a New Database Instance**

- Open Neo4j Desktop.

- Click **Create instance**.

- **Instance Details**: Give it a name (e.g., NeSy-Graph).

- **Create database user**: Set your password (ensure it matches the `NEO4J_PASSWORD` in your .env file).

- **Load from .dump**: Browse for the **neo4j.dump** file (found in the `/data` folder of this repo) .

- Click Create.

**2. Install n10s**

Even though the data is loaded, you must still enable the required logic engines.

_Note: Neosemantics (n10s) is not available directly in the Desktop UI it must be downloaded manually._

**Install Neosemantics (n10s):**

- Download the compiled `.jar` file from the [official n10s GitHub Releases](https://github.com/neo4j-labs/neosemantics/releases).
  _Make sure to download the version that matches your Neo4j database version (e.g., 5.x)._

- In Neo4j Desktop, click the **...** (three dots) next to your instance.
- Select **Open** -> **Instance Folder**.
- Open the `plugins` folder and paste the downloaded `.jar` file inside.
- Go back to Neo4j Desktop, click **...** -> **Open** -> **neo4j.conf**.
- Scroll to the bottom of the configuration file and add this exact line:

  ```
  server.unmanaged_extension_classes=n10s.endpoint=/rdf
  dbms.security.procedures.allowlist=apoc.*,n10s.*
  dbms.security.procedures.unrestricted=apoc.*,n10s.*
  ```

**Restart the Database**

After modifying the `neo4j.conf` file, you must restart the database for the plugin configuration to take effect.

- Go back to Neo4j Desktop.
- Click **Stop** on your database.
- Wait a few seconds.
- Click **Start** to run the database again.

Once the database restarts, the n10s plugin will be loaded and ready to use.

---

### Next Steps

Now that your ontologies are loaded and labeled, you need to calculate weights and embeddings.
➡️ **[Go to Data Enrichment Instructions](../notebooks/README.md)**
