#!/usr/bin/env python3

from azure.cosmos import CosmosClient

from langflow.custom import Component
from langflow.io import MessageTextInput, Output, SecretStrInput
from langflow.schema import Data


class AzureCosmoDBClient(Component):
    display_name = "Azure CosmosDB"
    description = "Custom Component to get data from Azure CosmosD."
    icon = "Azure"
    name = "AzureCosmosDBClient"

    inputs = [
        MessageTextInput(
            name="account_uri",
            display_name="Account URI",
            value="Account URI",
            info="Your Azure Account URI, Example: `https://example-resource.azure.com/port_numer`",
            required=True,
        ),
        SecretStrInput(name="account_api_key", display_name="Account API Key", required=True),
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
    ]

    outputs = [
        Output(display_name="Output", name="output", method="build_output"),
    ]

    def build_output(self) -> Data:
        client = CosmosClient(self.account_uri, credential=self.account_api_key)
        database = client.get_database_client(self.database_name)
        container = database.get_container_client(self.container_name)
        query = "SELECT c.id, c.pageContent FROM c OFFSET @offset LIMIT @limit"
        parameters = [
            {"name": "@offset", "value": 1},
            {"name": "@limit", "value": 10},
        ]
        items = list(container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True))
        return Data(value=items)
