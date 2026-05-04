import React, { useState, useEffect } from 'react';
import './App.css';
import Camera from './components/Camera.js'
import Accordion from './components/Shoppers_List.js';

function App() {
  // 1. Setup state to hold your database logs
  const [logs, setLogs] = useState([]);

  // 2. Function to fetch data from your Flask server
  const fetchInventory = () => {
    // Replace with your Pi's IP address if accessing from your PC
    fetch('http://127.0.0.1:5000/logs')
      .then(response => response.json())
      .then(data => {
        setLogs(data); 
      })
      .catch(err => console.error("Database connection error:", err));
  };

  // 3. Automatically fetch data every 3 seconds
  useEffect(() => {
    fetchInventory(); // Initial fetch
    const interval = setInterval(fetchInventory, 3000); 
    return () => clearInterval(interval); // Cleanup on close
  }, []);

  return (
    <div className="App">
      <div className="Camera">
        <Camera/>
        <button className='Change-Camera'>
          Change Cameras
        </button>
      </div>

      <div className="Current-Shoppers">
        <Accordion/>
      </div>

      <div className="Arming-Button">
        {/* Placeholder for your toggle logic */}
        <button className="toggle-btn">Arm System</button>
      </div>

      <div className="Inventory-List">
        <h3>Actively Updating Inventory</h3>
        {/* 4. Mapping the database logs to the UI */}
        <div className="log-container">
          {logs.length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>Item</th>
                  <th>Status</th>
                  <th>Time</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log) => (
                  <tr key={log.id}>
                    <td>{log.label}</td>
                    <td>{log.status}</td>
                    <td>{new Date(log.timestamp).toLocaleTimeString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>Scanning for items...</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;