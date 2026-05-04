import './App.css';
import Camera from './components/Camera.js'
import InventoryHeader from './components/Inventory-Header.js';
import InventoryList from './components/Inventory.js';
import Shoppers from './components/Shoppers_List.js';
import ArmingHeader from './components/Arming-Header.js';
import ArmingButton from './components/Arming-Button.js';

function App() {
  

  return (
    <div className="App">
      <div className = "Camera">
        <Camera/>
        <button 
        className= 'Change-Camera'
        style= {{
          backgroundColor : "black",
          color : "white"
        }}
        >
          Change Cameras
        </button>
      </div>
      <div className = "Current-Shoppers">
        <Shoppers/>
      </div>
      <div className = "Inventory-List">
        <InventoryHeader/>
        <InventoryList/>
        </div>
      <div className = "Arming-Button">
        <ArmingHeader/>
        <div
        style= {{
          padding : "20px"
        }}
        >
          Green = Armed Red = Disarmed
        </div>
        <ArmingButton/>
      </div>
    </div>
  );
}

export default App;
