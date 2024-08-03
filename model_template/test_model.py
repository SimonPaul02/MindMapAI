import model
from data_models import TaskInput, TaskMessage
import asyncio

history_messages = [
    TaskMessage(role="user", content="Hello"),
    TaskMessage(role="assistant", content="Hi! How can I help you today?"),
    TaskMessage(role="user", content="I'm fine, could you tell me what 2 + 2 is?"),
]
input = TaskInput(text=history_messages, system="You are a chatbot helping people")


async def run():
    res = await model.get_response(input)
    print(type(res.text))
    print(res)
    assert type(res.text) == type("str")
    assert len(res.text) > 0


if __name__ == "__main__":
    asyncio.run(run())
