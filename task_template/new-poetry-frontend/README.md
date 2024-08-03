# The ReactJS frontend

In here, you will find the explanation of the task's frontend, all its components and what you should keep in mind while using this as a baseline for creating your own task.

## 1. Root component: 
The root component of this frontend is [App.jsx](src/App.jsx) which serves as the entrypoint for the application. 

Inside it are the initial states:
- `messages`: represents the conversation between the user and the model as a list.
- `isFinished`: indicates if the conversation is finished or not. 

## 2. Child components: 
All the child components are located [here](src/components).

### 1. ConversationDisplay [link](src/components/ConversationDisplay.jsx):
This component represents the Conversation section of the frontend (the part under "Discussion with AI"). This component receive the `messages` state from the App component, and then maps each message to a different `ConversationItem` component.

This is the most important component of this frontend functionality-wise since it dictates how the interaction should be. Here is a quick rundown of the component:

- `useEffect()`:
This line checks if the length limit is reached or not by using the lengthLimit constant imported from the [config file](src/utils/config.jsx)
- `parsePoetryAndComment(input)`:
This function processes and parses the output of the model based on square brackets. You can change it based on which output form of the model you want to have. Currently, it works based on how the output of the model is set, which is to have the generated poem line wrapped inside a square bracket.
- `checkAndAddMessage(sender, text, comment, type)`:
This function serves as a way to validate a message before it is added to the `messages` state.
- `handleSubmit`:
This function handles the submission of an user's message
- `chooseTheme`:
This function set the theme/objective for the task, which is then sent to the prompt.
- `toggleFinishButton`:
This function handles the interaction of the Finish button. If the button is clicked, it set the `isFinished` state of the App component to true and the `FeedbackForm` component will appear as the result.
### 2. ConversationItem [link](src/components/ConversationItem.jsx):
This component represents a single Conversation entry.

### 3. Dialogue [link](src/components/Dialogue.jsx):
This component represents the Dialogue section of the frontend (the part under "Your joint poem"). 
This component receive the `messages` state from the App component, and then maps each message to a different `DialogueItem` component. 

**Note**: the `style` variable inside the file decides the type of the dialogue, which is the `dialogueType` imported from the [config file](src/utils/config.jsx).

### 4. DialogueItem [link](src/components/DialogueItem.jsx):
This component represents a single Dialogue entry. Each dialogue line can be clicked to open its own edit form, which give the user the ability to freely modify the dialogue.

### 5. FeedbackForm [link](src/components/FeedbackForm.jsx):
This component represents the feedback form, which appears When the `Finish` button is clicked. When the rating is submitted, it calls the `finishTask` function inside the file [task.js](src/services/task.js), which at the moment only logs the rating into the console. When the reset button is clicked, the application resets.

### 6. Footer [link](src/components/Footer.jsx):
This component serves as the Footer for this web application. Modify the content as you see fit.

### 7. Header [link](src/components/Header.jsx):
This component serves as the Header for this web application. Modify the content as you see fit.

### 8. TaskDescription [link](src/components/TaskDescription.jsx):
This component serves as a description of your task. You can change it to tell the user how to use it step-by-step.


## 3. API calls:
The API call function `submitUserInput` are located in the file [task.js](src/services/task.js). It receives the user's message as parameter, sends it to the model through a post request to the `/api/v1/task/process` endpoint, and returns the model's response.

## 4. Config file:
There are two constants that you need to change based on what you need in the config file [config.jsx](src/utils/config.jsx)
- `lengthLimit`: 
This is the length limit of the final generated text. When this limit is reached, the task is deemed finished.

- `dialogueType`: 
You can change its value between `"poem"` and `"paragraph"`. The browser will change how it renders the texts based on this value.
