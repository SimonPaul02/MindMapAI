import React, { useState, useEffect } from "react";

const FullTextBox = ({ text, setText, handleInputBoxSubmit }) => {
  const [localText, setLocalText] = useState(text);
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    if (!isEditing) {
      setLocalText(text);
    }
  }, [text, isEditing]);

  const handleSave = () => {
    setText(localText);
    setIsEditing(false);
    handleInputBoxSubmit(localText);
  };

  const handleCancel = () => {
    setLocalText(text);
    setIsEditing(false);
  };

  const handleEdit = () => {
    setIsEditing(true);
  };

  return (
    <div className="fulltext-box">
      <h2 className="box-title">Generated Text</h2>
      <div className={`fulltext-box-content ${text ? "" : "empty"}`} onClick={handleEdit}>
        <div className={`editable-content ${text ? "" : "placeholder-text"}`}>
          {text || "The generated text will appear here"}
        </div>
      </div>
      {isEditing && (
        <div className="overlay">
          <textarea
            className="overlay-textarea"
            value={localText}
            onChange={(e) => setLocalText(e.target.value)}
          />
          <div className="button-group">
            <button onClick={handleSave}>Save</button>
            <button onClick={handleCancel}>Cancel</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default FullTextBox;
