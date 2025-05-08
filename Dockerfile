FROM langflowai/langflow:latest
WORKDIR /app
RUN mkdir -p ./custom_components/Commvault
COPY ./src/backend/base/langflow/components/commvault/*.py ./custom_components/Commvault/
RUN uv pip install azure-cosmos
ENV LANGFLOW_COMPONENTS_PATH='./custom_components'
ENV DO_NOT_TRACK=true
ENV LANGFLOW_HOST=0.0.0.0

# uncommit for PROD Deployment
#ENV LANGFLOW_PORT=80
# Uncommet for loacl testing
ENV LANGFLOW_PORT=7860
