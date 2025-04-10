#!/usr/bin/env python3

from langflow.custom import Component
from langflow.io import HandleInput, Output
from langflow.schema import Data


class CombineDataFromMultipleVectorSearches(Component):
    display_name = "Merge Data"
    description = "Concatinate data from Multiple Vector Searches."
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
            info="List of Input objects each with added Metadata",
            method="process_output",
        ),
    ]

    def process_output(self) -> Data:
        return Data(
            value=[
                {
                    "page_content": result_dict["page_content"],
                    "metadata": {
                        key: result_dict["metadata"][key]
                        for key in ["title", "selfLink"]
                        if key in result_dict["metadata"]
                    },
                }
                for item in self.input_value
                if hasattr(item, "data") and "value" in item.data
                for result_dict in item.data["value"]
            ]
        )
