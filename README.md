# Misc scripts for SemUN project

This repository contains the script to populate Neo4j databse with static data from the UN, independent of the actual documents.

As of now are supported:

- UN member states
- UN bodies

The scripts in [`src/`](src/) take a file as input and output a Cypher script to populate the database.

You can find useful targets in the [`Makefile`](Makefile) to run the scripts.
