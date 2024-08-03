# IMPORTANT: For Hackathon participants
In the hackathon, the 3 main things you need to edit to adjust to your own task are the prompt, the frontend, and the model selection. However, if you want, feel free to explore the other parts of the system as well. We appreciate any feedback and suggestions that you might have for the Collaborative AI arena!

## Prompt:
The prompt for the task is located inside [poetry.py](task_template/app/task_examples/poetry.py) in the `get_system_prompt` function. Currently, the function receives a parameter called `objective`, which serves as the theme/topic for the poem, and returns the prompt. 

Although the current prompt serves as a starting point for your task, it's by no means optimized. Because of that, we highly recommend you to experiment and do some prompt engineering for it to fit whatever task you have in mind.

## Frontend:
The frontend for the hackathon is based on our poetry task, rewritten in ReactJS. The main idea of the task is that the user submits the theme/objective for the poem and then they collaborate with the model to complete it. However, This task is not limited to poem writing only as you can freely switch between a line-by-line rendering (poem) or a continuous rendering (paragraph). For a more detailed explanation, please go [here](task_template/new-poetry-frontend/README.md)

## Model selection:
At the moment, the system supports two models [gpt4-turbo](model_template/models/openAI_model.py) and [gpt4-o](model_template/models/openAI_image_model.py), which is located inside the folder [model_template/models](model_template/models). 

You can change between the two models by changing the value of the variable `ai_model` between `OpenAIImageModel()` and `OpenAIModel()` in the file [model_template/model.py](model_template/model.py).

If you have time and want to add your own models to the system, feel free to do so by following the template located in the file [basemodel.py](model_template/models/basemodel.py) and use the already existing model files as guidance.
<br/> <br />
___

# Collaborative AI Arena

The collaborative AI arena is intended to serve as a basis for evaluation of collaboration between AI and Humans. The idea is to design and evaluate tasks which are performed with input from both sides, and figure out if the collaboration was successful.
Users should be presented with a task that they perform together with the AI and metric should be used to evaluate the different

This repository contains most of the code necessary to add a Model or a Task.

## Templates

The `task_template` and `model_template` folders contain template applications for deployment on the AI Builder infrastructure.
They indicate how to implement a model and a task and supply most infrastructure necessary to minimise the requirements of a user to adopt their code.
Details are provided in the respective README files.

## Local testing

To test things locally and see if they work, we provide a docker compose file along with a simple orchestrator.

To run locally you will need docker installed!

To run, you need docker installed.  
You also need the following environment variables set:

- `OPENAI_API_KEY` - a openAI access key.
- `SSL_KEY` - a valid openssl certficate key
- `SSL_CERTIFICATE` - a valid openssl certificate

The template model currently uses an Aalto specific endpoint for computation.
You will likely need to change the model used in `model_template/model.py` to an OpenAI model and use that for testing.

We provide two tasks that can be used, either a poetry task or a tangram task. To run them call:
`docker compose -f docker-compose_tangram.yaml up --build` for the tangram task and  
`docker compose -f docker-compose_poetry.yaml up --build` for the poetry task respectively
only one of the tasks can be run at the same time.

After that, the frontend should be accessible via https://localhost:8062.
