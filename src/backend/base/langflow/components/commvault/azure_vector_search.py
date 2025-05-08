#!/usr/bin/env python3
import json
import os

import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

from langflow.custom import Component
from langflow.io import DropdownInput, MessageTextInput, Output
from langflow.schema import Data

load_dotenv()

# Environment variable loading and validation
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "10"))

if not BASE_URL or not API_KEY:
    msg = "BASE_URL and API_KEY must be set in the environment."
    raise OSError(msg)


class SemanticSearchRequest(BaseModel):
    collection_name: str = Field(default="")
    search_query: str = Field(default="")
    search_type: str = Field(default="SimilaritySearch")
    num_search_results: int = Field(default=5, ge=1, le=MAX_SEARCH_RESULTS)
    where_filter: dict | None = Field(default=None)
    threshold: float = Field(default=1.0)


class AzureVectorSearch(Component):
    """Custom Component to get data from Azure Vector documents."""

    display_name = "Azure Vector Search"
    description = "Custom Component to get data from Azure Vector documents"
    icon = "Azure"
    name = "AzureVectorSearchClient"

    INDEX_NAMES = [
        "arlie_documentation_28",
        "arlie_documentation_32",
        "arlie_documentation_34",
        "arlie_documentation_36",
        "arlie_documentation__feedback",
        "arlie_documentation__header28",
        "arlie_documentation__header32",
        "arlie_documentation__header34",
        "arlie_documentation__header36",
        "arlie_documentation__headerexpert28",
        "arlie_documentation__headerexpert32",
        "arlie_documentation__headerexpert34",
        "arlie_documentation__headerexpert36",
        "arlie_documentation__headermetallic34",
        "arlie_documentation__headermetallic36",
        "arlie_documentation__expert28",
        "arlie_documentation__expert32",
        "arlie_documentation__expert34",
        "arlie_documentation__expert36",
        "arlie_documentation__metallic34",
        "arlie_documentation__metallic36",
    ]

    inputs = [
        DropdownInput(
            name="index_name",
            display_name="Index Name",
            info="The name of the collection to search within.",
            options=sorted(INDEX_NAMES),
            value=INDEX_NAMES[0],
        ),
        MessageTextInput(
            name="search_text",
            value="Search Text",
            display_name="Search Text",
            info="The query string that will be searched in the collection.",
            required=True,
        ),
        MessageTextInput(
            name="top_k",
            value="5",
            display_name="Number of Search Results",
            info=f"The maximum number of search results to return (1-{MAX_SEARCH_RESULTS}).",
            required=True,
            field_type="str",
        ),
    ]

    outputs = [
        Output(display_name="Output", name="output", method="build_output"),
    ]

    def build_output(self) -> Data:
        """Build the output by performing a semantic search request.

        Returns:
            Data: The result of the search or an error message.
        """
        # Validate and parse inputs
        try:
            top_k = int(self.top_k)
            if not 1 <= top_k <= MAX_SEARCH_RESULTS:
                msg = f"top_k must be between 1 and {MAX_SEARCH_RESULTS}."
                raise ValueError(msg)
        except (ValueError, TypeError) as e:
            self.status = f"Invalid input for top_k: {e!r}"
            return Data(value=self.status)

        try:
            search_params = SemanticSearchRequest(
                collection_name=self.index_name,
                search_query=self.search_text,
                num_search_results=top_k,
            )
        except ValidationError as e:
            self.status = f"Invalid search parameters: {e!r}"
            return Data(value=self.status)

        payload = json.dumps(search_params.model_dump())
        headers = {"x-api-Key": API_KEY, "Content-Type": "application/json"}

        # Make the API request
        try:
            response = requests.post(
                url=BASE_URL,
                headers=headers,
                data=payload,
                timeout=TIMEOUT,
            )
            response.raise_for_status()
            documents = response.json()
            self.status = "Success" if documents else "No documents found"
            return Data(value=documents)
        except requests.exceptions.RequestException as e:
            self.status = f"Request failed: {e!r}"
            return Data(value=self.status)
