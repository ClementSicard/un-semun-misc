import argparse
import os

import pandas as pd
import pyperclip
from loguru import logger


def run(filePath: str) -> None:
    """
    This function reads a CSV file and generates Cypher statements to create
    UNBody nodes in Neo4j.

    Parameters
    ----------
    `filePath` : `str`
        The path to the CSV file.
    """
    logger.info(f"Reading the CSV file '{filePath}'...")
    if not os.path.exists(filePath):
        logger.error("The file does not exist.")
        return

    df = pd.read_csv(
        filePath,
        sep=";",
        header=None,
        names=["accronym", "labelEn"],
    )

    logger.debug(df.head())

    # Convert the DataFrame to a list of dictionaries
    dictList = df.to_dict("records")
    cypherStatements = []
    for record in dictList:
        fields = ", ".join(f'{key}: "{value}"' for key, value in record.items())
        cypherStatements.append(f"MERGE (n:UNBody {{ {fields} }});")

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

    logger.success(
        f"Done! {len(cypherStatements)} statements have been copied to the clipboard."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=True,
        help="The path to the CSV file",
    )
    args = parser.parse_args()

    run(args.file)
