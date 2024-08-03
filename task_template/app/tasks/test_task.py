import json

tangramData = """
{
  "Big Triangle 1": [
    "(512, 320)",
    0,
    1,
    1
  ],
  "Big Triangle 2": [
    "(916, 236)",
    180,
    1,
    1
  ],
  "Medium Triangle": [
    "(672, 416)",
    0,
    1,
    1
  ],
  "Parallelogram": [
    "(544, 416)",
    0,
    1,
    1
  ],
  "Small Triangle 1": [
    "(680, 256)",
    0,
    1,
    1
  ],
  "Small Triangle 2": [
    "(576, 352)",
    0,
    1,
    1
  ],
  "Square": [
    "(640, 320)",
    0,
    1,
    1
  ]
}
"""
import os

data = json.loads(tangramData)
os.environ["TASK_NAME"] = "tangram"
from tasks.task import task as testTask
from models import (
    TaskDataRequest,
)

print(type(data))
print(data)
request = TaskDataRequest(inputData=data, objective="A House")
print(request.inputData)
print(type(request.inputData))
modelRequest = testTask.generate_model_request(request)
print(modelRequest)
