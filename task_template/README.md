# Task template for use with the Collaborative AI Arena

This module serves as a template task (and as a suggestion on how to set up communication pathes)
The aim of this template is to allow concurrent processing of requests and implement the flow for the Task component as detailed in the following diagram:

![A diagram showing the flow of messages from the model perspective](docs/threecomp_layout.svg)

## Task Messages

There are four types of messages, a task will receive or send, which are all defined by the `tasks.proto` file.
The messages along with their fields are:

- Incoming Messages
  - `modelAnswer`:
    - `answer` : A string represnting a json object with the following fields:
      - `text` : The text of the answer of the model
      - `image`: a base64 encoded image.
    - `sessionID`: An ID of the session that this response is for
- Outgoing Messages:
  - `taskRequest`
    - `request` : A string represnting a json object with the following fields:
      - `text` : An array of messages with a syntax resembling OpenAI messages. Each message has a field `role` and a field `content` where role can be either `"assistant"` or `"user"`
      - `image`: a base64 encoded image.
      - `system`: A String representing a system message to the model (i.e. the task description)
    - `sessionID`: An ID of the session that generated this resource
  - `taskMetrics`:
    - `metrics`: A String that is alredy formatted and just needs to be put into the models log, so that it can be interpreted by AIBuilder for the leaderboard
    - `sessionID`: The session for which these metrics were generated
  - `modelRequirements`: A message that indicates, what the model needs to be able to handle for this session of this task
    - `needs_text`: A Bool indicating whether the model needs text for processing
    - `needs_image`: A Bool indicating whether the model needs an image for processing
    - `sessionID`: The ID for these requirements

## Task Services

The task will need to implement the four services detailed in the tasks.proto file.
Those contain:

- `startTask` : A Service which is called with an empty request on startup and needs to inform the model handler, whenever a new session is generated by the task (i.e. for each new run of a task). The message needs to define the `modelRequirements` containing the `sessionID`, which will allow the model handler to select one model for this session. This definition indicates the capabilities of the model required to fullfil the task (i.e. it needs to specify whether the model needs to be able to handle text and images to work with this task).
- `runTask`: This is again a service with an empty request, which needs to provide a sstream of `taskRequest` messages, which will be allocated to the correct model by the model handler.
- `finishTask`: Again a service that needs to provide a stream of `taskMetrics` messages upon completion of the task by the user.
- `getModelResponse`: This service receives the responses by the model, and needs to be able to handle them and assign them to the web-requests that caused their generation.

The logic of the processing is as follows:
When a user sends a request that they want to start the task, the `startTask` service should emit a `modelRequirements` message. This message
is used by the model handler to select a model for the indicated session.
After this message, the `runTask` service can emit several `taskRequest` messages, which will be processed and forwarded by the model handler
to the appropriate model.
Finally, when a session (i.e. running one task) ends, the task needs to emit one `taskMetrics` message from the `finishTask` service to indicate,
that this session is over, and that the association can be removed. After that it can emit a new `modelReqirements` message from the `startTask`
service, if a new session was started etc..

## Implementation

We provide a sample implementation of a Task Server in the `task_server.py` class.
The `main.py` file further implements a FastAPI server which can serve a ready to serve front-end along with three end-points that can be used as
a basis and implementation example for tasks and the communication logic.

### API Models:

For simplicty, we have defined four pydantic models that we use for interaction between the model server and the actual model implementation in the `models.py` module.

- `TaskDataRequest`, this is the incoming data request from the front end and needs to be interpreted by the task code.

  - `text` : An optional field for textual input (for convenience)
  - `image`: An optional field containing an image in base64 representation
  - `objective` : An optional field for a user defined objective to the task (for convenience)
  - `inputData`: A required field containing any JSON formatted data, which the task needs to know about. This can also be empty, if the task only handles the text or image fields, but is a catch all to allow the user to provide their specific data.

- `TaskRequest`, A class that the task needs to provide to the server.

  - `text` : The text (user input) which is provided to the model as the user message. This needs to be generated from the input data.
  - `image` : a string base64 encoded image that the user provided
  - `system` : The system message describing the task to solve

- `ModelResponse`, The response obtained by the model. It contains text and image data, depending on the model and requirements of the task

  - `text` : a String with the model answer
  - `image` : a string base64 encoded image of the model answer (can be None)

- `TaskDataResponse`, The response obtained by the model. It contains text and image data, depending on the model and requirements of the task

  - `text` : a String with the model answer
  - `image` : a string base64 encoded image of the model answer (can be None)
  - `outputData`: as inputdata this is a free form field, which can contain any json encoded data to make it easier for the user to pass data back to the front-end

- `TaskRequirements`, A definition of the requirements for this task
  - `needs_text` : Whether the task needs a model that can handle text
  - `needs_image` : Whether the task needs a model that can handle images

### Interface

The server handles most functionality on the back-end side. It requires the implementation of the class `ActiveTask` in the `tasks/task.py` file which needs to implement the Task interface from `tasks/task_interface.py`. This interface needs to implement the following functions

- Methods:
  - `generate_model_request(request: TaskDataRequest)-> TaskRequest`
    - Generate the model Request from the input data. the request.inputData field is a free-form json, that you can use for front-end back-end communication for any "non standard" data transfer
  - `process_model_answer( answer: ModelResponse) -> TaskDataResponse`
    - process the model response. E.g. if you have given a specific format to the models and need to parse that format for your front-end
  - `get_requirements() -> TaskRequirements`
    - A function that needs to return the requirements of the Task, to be able to select the right model.

#### Front-end

The current docker file assumes a frontend folder which contains builds the `frontend` into it's `dist` folder. The server will serve these files automatically.
This might need to be changed for your front-end but generally any compiled front-end can be used.
If you use a different front-end tech to the one in this project, the compiled frontend needs to be placed into the "dist" folder from which it will be served by the FastAPI server.

#### Frontend-backend interaction

The back-end provides two endpoints at the moment:

- `/api/v1/task/process/`, which expects a `TaskDataRequest` object to be processed.
  This endpoint will respond with a `TaskDataResponse`, with the contents depending on the response of the model and the post-processing done in the `process_model_answer` function of the task.
- `/api/v1/task/finish/` this endpoint indicates that one session has finished, and expects a `TaskMetrics` object that is passed on to the model handler, supplemented with the session ID. This will also clear the session association held by the back end, and the triggered model handler call will clear out the model associated with the current session.

### Front-end templates

Two templates currently exist for the frontend which are roughly similar.
One is for a poetry interaction, where the user and the LLM create a poem together.
The other is for a tangram game, where the user can place pieces and the AI can inform them of where to put pieces.

Th two different tasks have individual docker files (`Dockerfile_poetry` and `Dockerfile_tangram` respectively)
For the tangram task, the template currently available on the front-end is a combination of a godot game (source obtainable on request) which incorporates interaction with the a vue framework.
The poetry task is a simple chat like interface in vue.
This can be replaced by anything which calls the above mentioned backend endpoints and provides an index.html.

We provide an alternative docker file (Dockerfile_godot_only) that shows how to deploy the godot game directly instead of within the vue framework. Note, however, that this game does not currently talk with the back-end as it was intended to be used within the vue framework. But of course, it could be adapted such that it works with the backend.
