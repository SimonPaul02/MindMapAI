import DialogueItem from "./DialogueItem";
import { dialogueType } from "../utils/config";

const Dialogue = ({ messages, setMessages }) => {
  let style = "none";
  if (dialogueType === "paragraph") {
    style = "dialogue-paragraph";
  } else {
    style = "dialogue-poem";
  }

  const handleEditMessage = (index, newMessage) => {
    if (!newMessage.trim()) {
      alert("Please save a non empty dialogue");
    } else {
      setMessages(messages.map((message, idx) => idx !== index ? message : { ...message, text: newMessage }))
    }
  };

  return (
    <div className="dialogue-wrapper">
      <h2>Your joint poem</h2>
      <div className="dialogue">
        {messages
          .map((msg, idx) => ({ ...msg, originalIndex: idx })) // Preserve original index
          .filter(msg => msg.text !== "" && msg.text !== null)
          .map((msg) => (
            <DialogueItem
              key={msg.originalIndex} // Use original index as key if needed
              idx={msg.originalIndex} // Pass original index as `idx`
              message={msg}
              handleEditMessage={handleEditMessage}
              style={style}
            />
          ))}
      </div>
    </div>
  );
};

export default Dialogue;
