"""
Template memory module for GPT agents.
"""

import chromadb
import chromadb.config

import GPTAgents.paths as paths

client = chromadb.Client(
    chromadb.config.Settings(
        # chroma_db_impl="duckdb+parquet",
        # persist_directory=paths.get_memory_path(),
        anonymized_telemetry=False,
    )
)


class Config:
    """
    Configuration of the AI system
    """

    Name: str
    Goal: str
