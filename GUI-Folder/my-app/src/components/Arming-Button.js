
import { useState } from "react";

export default function ArmingButton () {
    const [armed , setArm] = useState(false);

    return (
        <button 
        onClick = {() => setArm(!armed)}
        style = {{
            backgroundColor : armed ? "green" : "red",
            color : "white"
        }}
        >
            Click here to arm/disarm system
        </button>
    )
}