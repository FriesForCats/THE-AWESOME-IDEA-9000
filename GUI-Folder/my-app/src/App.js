import './App.css';
import Camera from './components/Camera.js'
import Accordion from './components/Shoppers_List.js';

function App() {
  return (
    <div className="App">
      <div className = "Camera">
        <Camera/>
        <button className= 'Change-Camera'>
          Change Cameras
        </button>
      </div>
      <div className = "Current-Shoppers">
        <Accordion/>
      </div>
      <div className = "Arming-Button">
        This is where the toggle to arm the system will be
        </div>
      <div className = "Inventory-List">
        This is where the actively updating inventory will be
        </div>
    </div>
  );
}

export default App;
