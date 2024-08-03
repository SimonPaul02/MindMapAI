import React, { useEffect, useRef, useState } from 'react';
import * as go from 'gojs';

const MindMapBox = ({ data }) => {
  const diagramRef = useRef(null);
  const diagram = useRef(null);
  const [nodes, setNodes] = useState(data || []);
  const [selectedNodes, setSelectedNodes] = useState([]);
  const [newNodeText, setNewNodeText] = useState('');

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === 'Enter') {
        addNode();
      } else if (event.key === 'Delete') {
        deleteNodes();
      }
    };

    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [newNodeText, selectedNodes]);

  useEffect(() => {
    if (diagram.current === null) {
      const $ = go.GraphObject.make;

      diagram.current = $(go.Diagram, diagramRef.current, {
        'undoManager.isEnabled': true,
        layout: $(go.TreeLayout, { angle: 90, layerSpacing: 35 }),
        'allowDelete': true,
        'allowCopy': true,
        'allowTextEdit': true,
        'initialContentAlignment': go.Spot.Center,
      });

      // Set the theme to dark mode
      diagram.current.themeManager.currentTheme = 'dark';
      diagram.current.themeManager.changesDivBackground = true;

      diagram.current.nodeTemplate = $(
        go.Node,
        'Auto',
        {
          click: (e, obj) => {
            const selected = diagram.current.selection.toArray().map(part => part.data);
            setSelectedNodes(selected);
          }
        },
        $(
          go.Shape,
          'RoundedRectangle',
          { strokeWidth: 0 }
        ).theme('fill', 'group'),  // Use themed color
        $(
          go.TextBlock,
          { margin: 8, editable: true }
        ).bind('text').theme('stroke', 'text')  // Use themed text color
      );

      diagram.current.linkTemplate = $(
        go.Link,
        $(go.Shape).theme('stroke', 'link'), // Use themed link color
        $(go.Shape, { toArrow: 'OpenTriangle' }).theme('fill', 'link') // Use themed arrow color
      );

      diagram.current.model = new go.TreeModel(nodes);

      // Manually set the background color of the diagram div
      diagramRef.current.style.backgroundColor = '#1e1e1e';
    }
  }, []);

  useEffect(() => {
    if (diagram.current) {
      const model = diagram.current.model;
      model.startTransaction('update');
      model.nodeDataArray = nodes;
      model.commitTransaction('update');
    }
  }, [nodes]);

  useEffect(() => {
    setNodes(data);
  }, [data]);

  const addNode = () => {
    if (selectedNodes.length === 1 && newNodeText.trim()) {
      const newNodeKey = (nodes.length + 1).toString();
      setNodes([...nodes, { key: newNodeKey, parent: selectedNodes[0].key, text: newNodeText }]);
      setNewNodeText(''); // Clear the input field after adding the node
    }
  };

  const deleteNodes = () => {
    if (selectedNodes.length > 0) {
      const selectedKeys = selectedNodes.map(node => node.key);
      setNodes(nodes.filter(node => !selectedKeys.includes(node.key)));
      setSelectedNodes([]);
    }
  };

  const importJson = (jsonData) => {
    setNodes(jsonData);
    setSelectedNodes([]);
  };

  const exportJson = () => {
    const json = JSON.stringify(nodes, null, 2);
    console.log(json);
  };

  return (
    <div className="mindmap-box">
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginBottom: '20px' }}>
        <input 
          type="text" 
          value={newNodeText} 
          onChange={(e) => setNewNodeText(e.target.value)} 
          placeholder="Enter new node text"
          disabled={selectedNodes.length !== 1}
          style={{ 
            width: '400px', 
            height: '40px', 
            fontSize: '16px', 
            padding: '10px', 
            borderRadius: '20px',
            backgroundColor: '#1e1e1e', // Dark background
            color: 'white', // White text
            border: '1px solid #555', // Border color
          }}
        />
        <button 
          onClick={addNode} 
          disabled={selectedNodes.length !== 1 || !newNodeText.trim()}
          style={{ display: 'none' }}
        >AddNode</button>
        <button 
          onClick={deleteNodes} 
          disabled={selectedNodes.length === 0}
          style={{ display: 'none' }}
        >DeleteNode</button>
      </div>
      <div
        ref={diagramRef}
        style={{ width: '100%', height: '600px' }}
      />
    </div>
  );
};

export default MindMapBox;
