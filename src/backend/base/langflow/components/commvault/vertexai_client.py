#!/usr/bin/env python3

import json

import requests

from langflow.base.models.model import LCModelComponent
from langflow.custom import Component
from langflow.io import Output
from langflow.schema.message import Message

# Constants
# BASE_URL = os.getenv("BASE_URL", "https://cvchatapp.commvault.com/api/v1/search")
# API_KEY = os.getenv("API_KEY", "default_api_key")
# TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 10))


BASE_URL = "https://cvchatapp.commvault.com/api/v1/vertexchat"
API_KEY = "dgAoKzFJ_xy8dwuFebKz9Atba957t_FAkjPXyfR2"
TIMEOUT = 30


class VertexAIClient(Component):
    display_name = "VertexAI"
    description = "Custom Component to get data from Vertex Chat documents"
    icon = "VertexAI"
    name = "VertexAIClient"

    inputs = [*LCModelComponent._base_inputs]

    outputs = [
        Output(display_name="Output", name="output", method="build_output"),
    ]

    def build_output(self) -> Message:
        search_text = str(self.system_message) + str(self.input_value)
        payload = json.dumps({"query": search_text.strip()})
        headers = {"x-api-Key": API_KEY, "Content-Type": "application/json"}
        try:
            response = requests.post(url=BASE_URL, headers=headers, data=payload, timeout=TIMEOUT)
            response.raise_for_status()
            response = response.json()["response"]
            self.status = "Success" if response else "No documents found"
            return Message(text=response)
        except requests.exceptions.RequestException as e:
            self.status = f"Request failed: {e!r}"
            return Message(text=f"Request failed: {e!r}")
