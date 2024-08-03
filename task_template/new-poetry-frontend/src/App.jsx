import { useState } from 'react';
import TaskDescription from "./components/TaskDescription";
import "./index.css";
import SuggestionBox from './components/SuggestionBox';
import FullTextBox from './components/FullTextBox';
import MindMapBox from './components/MindMapBox';
import InputBox from './components/InputBox';
import axios from 'axios';

const App = () => {
  
  const [suggestionText, setSuggestionText] = useState("");
  const [fullText, setFullText] = useState("");
  const [mindMapData, setMindMapData] = useState([
    { key: '1', text: 'Poem about AI and I Hackathon'},
    { key: '2', parent: '1', text: 'Content'},
    { key: '3', parent: '1', text: 'Structure'},
    { key: '4', parent: '1', text: 'Style'},
    { key: '5', parent: '2', text: 'Hacker'},
    { key: '6', parent: '2', text: 'Location'}
  ]);

  const getObjective = () => {
    const node = mindMapData.find(node => node.key === '1');
    return node ? node.text : '';
  };
  
  const handleInputBoxSubmit = (text) => {
    console.log(text);
    const requestData = {
      text: text,
      objective: getObjective(),
      inputData: {
        mindMap: mindMapData,
        handlerID: 1,
        suggestions: suggestionText
      }
    };
    const request = axios.post('api/v1/task/process', requestData);
    request.then(response => response.data)
    .then(responseData => {
      console.log(responseData);
      // Removing backticks and newline characters from responseData.text
      const cleanResponse = responseData.text.replace(/\\n/g, '').replace(/\\\"/g, '"');
      const parsedResponse = JSON.parse(cleanResponse);
      try {
        setMindMapData(parsedResponse.INSTRUCTIONS);
      } catch (error) {
        setMindMapData(parsedResponse);
      }    })
    .catch(error => {
      console.error('Error parsing response data:', error);
    });
  };

  

  const generateFullText = () => {
    console.log("Started translation of mindmap to text");
    const requestData = {
      objective: getObjective(),
      inputData: {
        handlerID: 2,
        mindMap: mindMapData,
      }
    };
    axios.post('/api/v1/task/process', requestData)
      .then(response => {
        const responseData = response.data;
        console.log(responseData);
        setFullText(responseData.text);
      })
      .catch(error => {
        console.error('Error generating full text:', error);
      });
  };

  const generateSuggestions = () => {
    console.log("Started generating suggestions");
    const requestData = {
      objective: getObjective(),
      inputData: {
        handlerID: 3,
        mindMap: mindMapData,
        suggestions: suggestionText,
      }
    };
    axios.post('/api/v1/task/process', requestData)
      .then(response => {
        const responseData = response.data;
        console.log(responseData);
        setSuggestionText(responseData.text);
      })
      .catch(error => {
        console.error('Error generating suggestions:', error);
      });
  };

  return (
    <>
      <TaskDescription />
      <div className="main-interaction">
        <div className="content-boxes">
          <SuggestionBox text={suggestionText} setText={setSuggestionText} />
          <MindMapBox data={mindMapData} />
          <FullTextBox text={fullText} setText={setFullText} />
        </div>
        <div className="button-group">
          <button className="new-button" onClick={generateSuggestions}>Generate Suggestions</button>
          <InputBox onSubmit={handleInputBoxSubmit} className="input-box"/>
          <button className="new-button" onClick={generateFullText}>Generate Text</button>
        </div>
      </div>
    </>
  );
};

export default App;
