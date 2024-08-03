import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import logging
import model_pb2
from data_models import *
from models.basemodel import AIModel

logger = logging.getLogger("app")

# NOTE: This needs to be defined in the environment this model is running in.
default_headers = {"Ocp-Apim-Subscription-Key": os.environ["OPENAI_API_KEY"]}


ChatOpenAI(
    base_url="https://aalto-openai-apigw.azure-api.net/v1/openai/gpt4-1106-preview/",
    default_headers=default_headers,
)

model_definition = model_pb2.modelDefinition()
model_definition.needs_text = True
model_definition.needs_image = False
model_definition.can_text = True
model_definition.can_image = False
model_definition.modelID = "GPT4_turbo"


class AaltoModel(AIModel):
    def get_model_definition(self) -> model_pb2.modelDefinition:
        return model_definition

    def publish_metrics(self, metrics_json: str) -> None:
        logger.info(metrics_json)

    async def get_response(self, message: TaskInput) -> TaskOutput:
        model = ChatOpenAI(
            base_url="https://aalto-openai-apigw.azure-api.net/v1/openai/gpt4-1106-preview/",
            default_headers=default_headers,
        )

        history_template = ChatPromptTemplate.from_messages(
            [
                # replace single curly brackets by double, since otherwise they they are interpreted as variables, which they are not
                ("system", message.system.replace("{", "{{").replace("}", "}}")),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )

        history = []
        if len(message.text) > 1:
            for i in range(len(message.text) - 1):
                inputMessage = message.text[i]
                if inputMessage.role == "user":
                    history.append(HumanMessage(inputMessage.content))
                else:
                    history.append(AIMessage(inputMessage.content))
        AIresponse = model.invoke(
            history_template.format_prompt(chat_history=history, input=message.text[-1])
        )
        print(f"AIresponse: {AIresponse.content}")
        taskResponse = TaskOutput()
        taskResponse.text = AIresponse.content
        return taskResponse


ai_model = AIModel()
