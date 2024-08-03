import { useState, useEffect } from 'react';
import ConversationItem from "./ConversationItem";
import taskService from '../services/task';
import { lengthLimit } from '../utils/config';

const ConversationDisplay = ({ toggleFinish, messages, addMessage }) => {
  const [newLine, setNewLine] = useState("");
  const [newComment, setNewComment] = useState("");
  const [isFinishClicked, setIsFinishClicked] = useState(false);
  const [isDisabled, setIsDisabled] = useState(false);
  const [theme, setTheme] = useState("");
  const [isLengthReached, setIsLengthReached] = useState(false);

  // Check if the length of the text has reached the line limit yet
  useEffect(() => {
    setIsLengthReached(messages.filter(msg => msg.text !== "" && msg.text !== null).length === lengthLimit);
  }, [messages]);

  function parsePoetryAndComment(input) {
    let poetryLine = "";
    let comment = "";

    input = input.trim();

    if (input.startsWith('[')) {
        let endBracketIndex = input.indexOf(']');
        
        if (endBracketIndex !== -1) {
            poetryLine = input.substring(1, endBracketIndex).trim();
            
            if (endBracketIndex + 1 < input.length) {
                comment = input.substring(endBracketIndex + 1).trim();
            }
        }
    } else {
        comment = input;
    }

    console.log("Parsed: ", poetryLine, ", ", comment);

    return { poetryLine, comment };
  }

  function checkAndAddMessage(sender, text, comment, type) {
    text = (typeof text === 'string' && text.trim()) ? text : null;
    comment = (typeof comment === 'string' && comment.trim()) ? comment : null;

    if (text === null && comment === null) {
      console.log("no message");
    } else {
      addMessage({ sender: sender, text: text, comment: comment, type: "dialogue" }); 
    }
  }

  const handleSubmit = (event) => {
    event.preventDefault();

    if (isLengthReached) {
      setNewComment((prevComment) => prevComment + " The poem is finished. Do NOT add a new poetry line.");
    }

    checkAndAddMessage("user", newLine, newComment, "dialogue");

    taskService
        .submitUserInput({inputData: { commentData: newComment }, text: newLine, objective: theme})
        .then((returnedResponse) => {
          let parsed = parsePoetryAndComment(returnedResponse.text);
          checkAndAddMessage("ai", parsed.poetryLine, parsed.comment, "dialogue");
        })
        .catch((error) => {
          console.log(error);
        });
    
    setNewLine("");
    setNewComment("");
  };

  const chooseTheme = (event) => {
    if (!theme.trim()) {
      alert("Please enter a theme");
      return;
    }
    event.preventDefault();
    setIsDisabled(true);
    
    taskService
      .submitUserInput({
        inputData: { commentData: "" },
        text: "",
        objective: theme
      })
      .then((returnedResponse) => {
        let parsed = parsePoetryAndComment(returnedResponse.text);
        checkAndAddMessage("ai", parsed.poetryLine, parsed.comment, "dialogue");
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const toggleFinishButton = () => {
    toggleFinish();
    setIsFinishClicked(!isFinishClicked);
  }

  return (
    <div className="chat-space-wrapper">
      <h2>Discussion with AI</h2>
      <div className="chat-space">
        <div>
          <form onSubmit={chooseTheme} className="theme-input">
            <input 
                  type="text" 
                  disabled={isDisabled}
                  placeholder="Set a theme for the poem"
                  value={theme}
                  className={isDisabled ? "disabled" : ""}
                  onChange={(event) => setTheme(event.target.value)}
            />
            <button 
                type="button"
                disabled={isDisabled}
                className={isDisabled ? "disabled" : ""}
                onClick={chooseTheme}
                style={{
                  backgroundColor: "#4caf50"
                }}>
                Submit 
            </button>
          </form>
        </div>
        <div className="messages">
          {messages
            .filter(msg => msg.comment !== "" && msg.comment !== null)
            .map((msg, index) => (
              <ConversationItem key={index} message={msg} /> 
            ))
          }
        </div>
        {isLengthReached && 
        <span 
          style={{
            color : "#FF0000"
          }}>
          Thank you. Here is our final poem. Please click Finish to rate it!
        </span>
        }
        <div className="form-wrapper">
          <form onSubmit={handleSubmit}>
            <div className="input-form">  
              <textarea 
                value={newLine}
                disabled={isLengthReached}
                className={isLengthReached ? "disabled" : ""}
                onChange={(event) => setNewLine(event.target.value)}
                placeholder="Add a line to the poem" 
              />
              <textarea 
                value={newComment}
                disabled={isLengthReached}
                className={isLengthReached ? "disabled" : ""}
                onChange={(event) => setNewComment(event.target.value)} 
                placeholder="Send a message to the AI" 
              />
            </div>
          </form>
          <div className="button-group">
              <button type="submit" 
                style={{
                  backgroundColor: "#4caf50"
                }}
                disabled={isLengthReached}
                className={isLengthReached ? "disabled" : ""}
                onClick={handleSubmit}> 
                Submit
              </button>
              <button type="submit" className="finish-button" 
                style={{
                  backgroundColor: isFinishClicked ? "#f44336" : "#6eb4ff",
                  cursor: isFinishClicked ? "not-allowed" : "pointer"
                }}
                onClick={toggleFinishButton}> 
                {isFinishClicked ? "Cancel" : "Finish"}
              </button>
            </div>
        </div>
      </div>
    </div>
  );
};

export default ConversationDisplay;
