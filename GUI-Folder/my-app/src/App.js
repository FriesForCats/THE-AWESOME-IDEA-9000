
/**
 * In this file, we are bringing together all of the
 * components we built to piece together the display.
 * 
 * The logic for the arming of the system is also 
 * handled in this file.
 */

import './App.css';
import { useState } from 'react';
import Camera , {toggleCamera} from './components/Camera.js'
import InventoryHeader from './components/Inventory-Header.js';
import InventoryList from './components/Inventory.js';
import Shoppers from './components/Shoppers-List.js';
import ArmingHeader from './components/Arming-Header.js';
import ArmingButton from './components/Arming-Button.js';
import ShoppersHeader from './components/Shoppers-Header.js';
import disco from "./components/disco.gif"

function App() {
  const [isArmed , setIsArmed] = useState(false);
  
  return (
    <div className="App">
        {isArmed && (
          <div className = "Status-Indicator">
            <img src = {disco}/>
          </div>
        )}
      <div className = "Camera">
        <Camera/>
      </div>
      <div className = "Current-Shoppers">
        <ShoppersHeader/>
        <Shoppers/>
      </div>
      <div className = "Inventory-List">
        <InventoryHeader/>
        <InventoryList/>
        </div>
      <div className = "Arming-Button">
        <ArmingHeader/>
        <pre
        style= {{
          padding : "20px"
        }}
        >
          Green = Armed{"\t"}Red = Disarmed
        </pre>
        <ArmingButton isArmed={isArmed} setIsArmed={setIsArmed}/>
      </div>
    </div>
  );
}

export default App;
