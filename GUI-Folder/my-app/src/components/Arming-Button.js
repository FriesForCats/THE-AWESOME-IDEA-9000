/** 
 * This is the component for the arming button in the bottom right of the screen.
 * 
 * All this file does is set up the button to change colors when clicked by 
 * using the useState function to determine if the system is armed or not.
 */

import { useState } from "react";

export default function ArmingButton ({isArmed , setIsArmed}) {
    return (
        <button 
        onClick = {() => setIsArmed(!isArmed)}
        style = {{
            backgroundColor : isArmed ? "green" : "red",
            color : "white"
        }}
        >
            Click here to arm/disarm system
        </button>
    )
}