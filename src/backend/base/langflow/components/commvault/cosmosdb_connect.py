#!/usr/bin/env python3
import os

from azure.cosmos import CosmosClient
from dotenv import load_dotenv

from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema import Data

load_dotenv()

BASE_URL = os.getenv("COSMOS_ENDPOINT")
API_KEY = os.getenv("COSMOS_KEY")

if not BASE_URL or not API_KEY:
    msg = "COSMOS_ENDPOINT and COSMOS_KEY must be set in environment variables."
    raise OSError(msg)


class AzureCosmoDBClient(Component):
    """Custom Component to get data from Azure CosmosDB."""

    display_name = "Azure CosmosDB"
    description = "Custom Component to get data from Azure CosmosDB."
    icon = "Azure"
    name = "AzureCosmosDBClient"

    inputs = [
        MessageTextInput(
            name="database_name",
            value="Database Name",
            display_name="Database Name",
            info="Your Azure CosmosDB database name.",
            required=True,
        ),
        MessageTextInput(
            name="container_name",
            value="Container Name",
            display_name="Container Name",
            info="Your Azure CosmosDB database container name.",
            required=True,
        ),
        MessageTextInput(
            name="offset",
            value="1",
            display_name="Offset",
            info="Query offset (default: 1).",
            required=False,
        ),
        MessageTextInput(
            name="limit",
            value="10",
            display_name="Limit",
            info="Query limit (default: 10).",
            required=False,
        ),
    ]

    outputs = [
        Output(display_name="Output", name="output", method="build_output"),
    ]

    def build_output(self) -> Data:
        """Query CosmosDB for items with pagination."""
        offset = int(getattr(self, "offset", 1) or 1)
        limit = int(getattr(self, "limit", 10) or 10)
        try:
            client = CosmosClient(url=BASE_URL, credential=API_KEY)
            database = client.get_database_client(self.database_name)
            container = database.get_container_client(self.container_name)
            query = "SELECT c.id, c.pageContent FROM c OFFSET @offset LIMIT @limit"
            parameters = [
                {"name": "@offset", "value": offset},
                {"name": "@limit", "value": limit},
            ]
            items = list(container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True))
            return Data(value=items)
        except (ValueError, TypeError, RuntimeError) as e:
            return Data(value={"error": str(e)})
