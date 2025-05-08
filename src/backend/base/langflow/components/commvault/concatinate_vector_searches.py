#!/usr/bin/env python3

from langflow.custom import Component
from langflow.io import HandleInput, Output
from langflow.schema import Data


class CombineDataFromMultipleVectorSearches(Component):
    display_name = "Merge Data"
    description = "Concatenate data from multiple vector searches."
    icon = "merge"
    name = "Merge Data"

    inputs = [
        HandleInput(
            name="input_value",
            display_name="Input",
            info="Object(s) to which Metadata should be added",
            required=False,
            input_types=["Message", "Data"],
            is_list=True,
        )
    ]

    outputs = [
        Output(
            name="data",
            display_name="Data",
            info="List of input objects each with added metadata",
            method="process_output",
        ),
    ]

    def process_output(self) -> Data:
        merged = []
        for item in self.input_value or []:
            values = getattr(item, "data", {}).get("value", [])
            for result in values:
                page_content = result.get("page_content")
                metadata = result.get("metadata", {})
                filtered_metadata = {k: metadata[k] for k in ("title", "selfLink") if k in metadata}
                merged.append(
                    {
                        "page_content": page_content,
                        "metadata": filtered_metadata,
                    }
                )
        return Data(value=merged)

