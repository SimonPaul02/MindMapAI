const ConversationalItem = ({ message }) => {
  const messageClass = message.sender === "user" ? "user-message" : "ai-message";
  const avatarClass = message.sender === "user" ? "avatar-user" : "avatar-ai";
  const avatarText = message.sender === "user" ? "You" : "AI";

  return (
    <>
      <div className={`message ${messageClass}`}>
        {message.sender === "user" ? (
          <>
            {message.comment}
            <div className={`avatar ${avatarClass}`}> {avatarText} </div>
          </>
        ) : (
          <>
            <div className={`avatar ${avatarClass}`}> {avatarText} </div>
            {message.comment}
          </>
        )}
      </div>
    </>
    
  );
};

export default ConversationalItem;
