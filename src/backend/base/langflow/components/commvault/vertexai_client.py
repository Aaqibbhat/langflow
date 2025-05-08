#!/usr/bin/env python3
import os

import requests
from dotenv import load_dotenv

from langflow.base.models.model import LCModelComponent
from langflow.custom import Component
from langflow.io import Output
from langflow.schema.message import Message

load_dotenv()

# Constants
BASE_URL = os.environ.get("VERTEXAI_BASE_URL")
API_KEY = os.environ.get("VERTEXAI_API_KEY")
TIMEOUT = int(os.environ.get("VERTEXAI_REQUEST_TIMEOUT", "10"))


class VertexAIClient(Component):
    """Custom Component to get data from Vertex Chat documents."""

    display_name = "VertexAI"
    description = "Custom Component to get data from Vertex Chat documents"
    icon = "VertexAI"
    name = "VertexAIClient"

    inputs = [*LCModelComponent._base_inputs]

    outputs = [
        Output(display_name="Output", name="output", method="build_output"),
    ]

    def build_output(self) -> Message:
        """Sends a query to the VertexAI endpoint and returns the response as a Message."""
        if not BASE_URL or not API_KEY:
            self.status = "Missing BASE_URL or API_KEY"
            return Message(text=self.status)

        search_text = f"{self.system_message}{self.input_value}".strip()
        headers = {"x-api-Key": API_KEY, "Content-Type": "application/json"}
        try:
            response = requests.post(
                url=BASE_URL,
                headers=headers,
                json={"query": search_text},
                timeout=TIMEOUT,
            )
            response.raise_for_status()
            data = response.json().get("response", "")
            self.status = "Success" if data else "No documents found"
            return Message(text=data)
        except requests.exceptions.RequestException as e:
            self.status = f"Request failed: {e!r}"
            return Message(text=self.status)
