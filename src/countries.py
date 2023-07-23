import argparse
import os

import pandas as pd
import pyperclip
from loguru import logger

COLUMNS = {
    "English short": "labelEn",
    "French short": "labelFr",
    "Spanish short": "labelEs",
    "Russian short": "labelRu",
    "Chinese short": "labelZh",
    "Arabic short": "labelAr",
    "English formal": "labelEnFormal",
    "French formal": "labelFrFormal",
    "Spanish formal": "labelEsFormal",
    "Russian formal": "labelRuFormal",
    "Chinese formal": "labelZhFormal",
    "Arabic formal": "labelArFormal",
}


def run(filePath: str) -> None:
    """
    This function reads an Excel file and generates Cypher statements to create
    Country nodes in Neo4j.

    Parameters
    ----------
    `filePath` : `str`
        The path to the Excel file.
    """
    logger.info(f"Reading the Excel file '{filePath}'...")

    if not os.path.exists(filePath):
        logger.error("The file does not exist.")
        return

    df = pd.read_excel(filePath)

    df = df.rename(columns=COLUMNS)

    # Convert the DataFrame to a list of dictionaries
    dictList = df.to_dict("records")

    # Generate the Cypher statements
    cypherStatements = []
    for record in dictList:
        fields = ", ".join(f'{key}: "{value.upper()}"' for key, value in record.items())
        cypherStatements.append(f"MERGE (n:Country {{ {fields} }});")

    logger.info("Statements: \n")

    # Format correctly the statements
    cypherQuery = (
        "\n".join(cypherStatements)
        .replace('"nan"', "null")
        .replace(" **", "")
        .replace(" *", "")
    )

    logger.debug(cypherQuery)

    # Copy the statements to the clipboard
    pyperclip.copy(cypherQuery)

    logger.success("Done! The statements have been copied to the clipboard.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=True,
        help="The path to the Excel file.",
    )
    args = parser.parse_args()

    run(args.file)
