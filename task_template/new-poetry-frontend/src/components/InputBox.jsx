import React, { useState } from "react";

const InputBox = ({ onSubmit }) => {
  const [input, setInput] = useState("");

  const handleChange = (event) => {
    setInput(event.target.value);
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      event.preventDefault(); // Prevent the default behavior of the Enter key
      if (input.trim()) {
        onSubmit(input); // Call the onSubmit function with the input value
      }
      setInput(""); // Clear the input field
    }
  };

  return (
    <textarea
      className="input-box"
      value={input}
      onChange={handleChange}
      onKeyDown={handleKeyDown}
      placeholder="Type your message here and press Enter to submit"
    />
  );
};

export default InputBox;
