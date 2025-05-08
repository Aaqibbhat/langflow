import os

from dotenv import load_dotenv
from langchain_community.chat_message_histories import CosmosDBChatMessageHistory

from langflow.base.memory.model import LCChatMemoryComponent
from langflow.field_typing.constants import Memory
from langflow.inputs import MessageTextInput

load_dotenv()


class CosmosDBChatMemory(LCChatMemoryComponent):
    display_name = "Cosmos DB Chat Memory"
    description = "Retrieves and stores chat messages in Azure Cosmos DB."
    name = "CosmosDBChatMemory"
    icon = "Azure"

    inputs = [
        MessageTextInput(
            name="cosmos_database",
            display_name="Database Name",
            info="The name of the database to use within Cosmos DB.",
            required=True,
        ),
        MessageTextInput(
            name="cosmos_container",
            display_name="Container Name",
            info="The name of the container where chat messages will be stored.",
            required=True,
        ),
        MessageTextInput(
            name="user_id",
            display_name="User ID",
            info="The user ID to use, can be overwritten while loading.",
            required=True,
        ),
        MessageTextInput(
            name="session_id",
            display_name="Session ID",
            info="The session ID of the chat. If empty, the current session ID parameter will be used.",
            advanced=True,
        ),
    ]

    def build_message_history(self) -> Memory:
        cosmos_endpoint = os.getenv("COSMOS_ENDPOINT", "")
        cosmos_key = os.getenv("COSMOS_KEY")
        if not cosmos_endpoint or not cosmos_key:
            msg = "COSMOS_ENDPOINT and COSMOS_KEY environment variables must be set."
            raise OSError(msg)

        return CosmosDBChatMessageHistory(
            cosmos_endpoint=cosmos_endpoint,
            credential=cosmos_key,
            cosmos_database=self.cosmos_database,
            cosmos_container=self.cosmos_container,
            session_id=getattr(self, "session_id", None),
            user_id=self.user_id,
        ).prepare_cosmos()
