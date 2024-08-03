import { useState } from "react";
import taskService from '../services/task'

const colors = ["#b71c1c", "#f44336", "#ff9800", "#ffeb3b", "#009688", "#81c784", "#4caf50"];

const FeedbackForm = ({ }) => {
  const [ratingSubmitted, setRatingSubmitted] = useState(false);

  const handleRatingSubmitted = (rating) => {
    //Add finish call here
    setRatingSubmitted(true);
    taskService.finishTask(rating)
  }

  return (
    <div className="feedback-container">
      <h2>Please rate your experience based on the below metric</h2>
      <h3>"Me and the AI collaborated well in this task"</h3>
      <div className="rating-container">
        {[0, 1, 2, 3, 4, 5, 6].map(rating => (
          <div
            key={rating}
            className={"rating-circle"}
            style={{
              "background-color": colors[rating]
            }}
            onClick={() => handleRatingSubmitted(rating+1)}
          >
            {rating + 1}
          </div>
        ))}
      </div>
      {ratingSubmitted && 
        <div className="after-rating-submitted">
          <h4>Thank you! The model that you worked with was XXX.</h4>
          <button type="submit" className="reset-button" onClick={() => window.location.reload()}> Reset </button>
        </div>
      }
    </div>
  );
};

export default FeedbackForm;
