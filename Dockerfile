FROM langflowai/langflow:latest
RUN mkdir ./custom_components
RUN mkdir ./custom_components/Commvault
COPY ./src/backend/base/langflow/components/commvault/*.py ./custom_components/Commvault/
RUN uv pip install azure-cosmos
ENV LANGFLOW_COMPONENTS_PATH='./custom_components'
ENV LANGFLOW_HOST=0.0.0.0
ENV LANGFLOW_PORT=80
ENV DO_NOT_TRACK=true