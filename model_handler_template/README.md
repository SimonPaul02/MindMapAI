# Model handler documentation

This module serves as a handler that manages the connection between multiple models and tasks components. This documentation is for your information only. 

## Model Handler Messages

There are eight types of messages, which are all defined by the `model_handler.proto` file.
The messages along with their fields are:

- Incoming Messages
  - `modelRequirements`: A message that indicates, what the model needs to be able to handle for this session of this task
    - `needs_text`: A Bool indicating whether the model needs text for processing
    - `needs_image`: A Bool indicating whether the model needs an image for processing
    - `sessionID`: The ID for these requirements
  - `taskMetrics`:
    - `metrics`: A String that is alredy formatted and just needs to be put into the models log, so that it can be interpreted by AIBuilder for the leaderboard
    - `sessionID`: The session for which these metrics were generated
  - `modelAnswer`:
    - `answer` : A string represnting a json object with the following fields:
      - `text` : The text of the answer of the model
      - `image`: a base64 encoded image.
    - `sessionID`: An ID of the session that prompted this response
  - `taskRequest`:
    - `request` : A string represnting a json object with the following fields:
      - `text` : An array of messages with a syntax resembling OpenAI messages. Each message has a field `role` and a field `content` where role can be either `"assistant"` or `"user"`
      - `image`: a base64 encoded image.
      - `system`: A String representing a system message to the model (i.e. the task description)
    - `sessionID`: An ID of the session that generated this resource
  - `modelDefinition`:
    - `needs_text`: A Bool indicating whether the model needs text for processing
    - `needs_image`: A Bool indicating whether the model needs an image for processing
    - `can_text`: A Bool indicating whether the model can handle text
    - `can_image`: A Bool indicating whether the model can handle images
    - `modelID`: The ID of this model
- Outgoing Messages:
  - `modelRequest`:
    - `request` : A string represnting a json object with the following fields:
      - `text` : An array of messages with a syntax resembling OpenAI messages. Each message has a field `role` and a field `content` where role can be either `"assistant"` or `"user"`
      - `image`: a base64 encoded image.f
      - `system`: A String representing a system message to the model (i.e. the task description)
    - `modelID`: A string representing which model this request is for
    - `sessionID`: An ID of the session that generated this resource
  - `metricsJson`:
    - `metrics`: A String that is alredy formatted and just needs to be put into the models log, so that it can be interpreted by AIBuilder for the leaderboard
    - `modelID`: A string representing which model this request is for
  - `modelAnswer`:
    - `answer` : A string represnting a json object with the following fields:
      - `text` : The text of the answer of the model
      - `image`: a base64 encoded image.
    - `sessionID`: An ID of the session that prompted this response

## Model Handler Services

There are five services detailed in the model_handler.proto file. Those contain:
- `startTask`: A service which is called when a modelRequirements message is sent from a task component. The request gives the handler the information so that it can choose the suitable model for the task. The condition for choosing the suitable model is as follow:
  - If the modelRequirements message has "needs_text", choose models that have "can_text" and don't have "needs_image".
  - If the modelRequirements message has "needs_image", choose models that have "can_image" and don't have "needs_text".
  - If the modelRequirements message has both "needs_image" and "needs_text", choose models that have both "can_image" and "can_text"
If there are multiple models that sastisfy the condition, choose a random model and then store the sessionID-modelID connection in a dictionary. The idea here is to assign a single session to a single model only. Finally, the service returns an Empty message.

- `finishTask`: a service which is called when a taskMetrics message is sent from a task component (whenever the task is demdemned completed by the user). After that, the model handler retrieves the modelID from the modelID-sessionID dictionary, and severes the connection between the sessionID and the modelID. Finally, the response of the service is a metricsJson message, which is then sent to the correct model component to store the metrics in the model logs.

- `sendToModel`: a service which is called when a taskRequest message is sent from a task component to the model handler. After that, the model handler retrieves the modelID from from the modelID-sessionID dictionary. Finally, the service returns a modelRequest message, which is then sent to the corresponding model component.

- `returnToTask`: a service which basically serves as a gateway to forward the model answer from a model component to a task component. It receives a modelAnswer message and returns the exact same modelAnswer message.

- `registerModel`: a service which is called when a modelDefinition message is sent from a model component. The request gives the necessary details (the capabilities of the model and the ID)of that model so that the handler can store them in a list for future use. The service returns an Empty message.
