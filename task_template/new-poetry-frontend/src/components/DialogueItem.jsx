import { useState } from 'react';

const DialogueItem = ({ idx, message, handleEditMessage, style }) => {
  const messageClass = message.sender === "user" ? "user-dialogue" : "ai-dialogue";

  const [isEditing, setIsEditing] = useState(false);
  const [editedMessage, setEditedMessage] = useState(message.text);

  const handleEditClick = () => {
    setIsEditing(!isEditing);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    handleEditMessage(idx, editedMessage);
    setIsEditing(!isEditing);
  };

  /*let newLine = ""
  const poemLine = message.text.match(/\[(.*?)\]/);
  if (poemLine) {
    newLine = poemLine[1];
  } else {
    newLine = message.text
  }*/

  return (
    <>
      {isEditing ? (
        <form onSubmit={handleSubmit} className="edit-form">
          <textarea
            value={editedMessage}
            onChange={(event) => setEditedMessage(event.target.value)}
          />
          <button type="submit" disabled={!editedMessage.trim()}> Save </button>
        </form>
      ) : (
        <div className={`${style} ${messageClass}`} onClick={handleEditClick}>{message.text} <br/> </div>
      )}
    </>
  );
};

export default DialogueItem;
