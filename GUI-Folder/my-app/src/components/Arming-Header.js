
/** 
 * This is the component for the header of the Arming Button section
 * 
 * All this file does is return a header object with 10 pixels of padding 
 * on top and bottom
 */

export default function ArmingHeader () {

    return (
        <header 
        className="Arming-Header"
        style = {{
            padding : "10px"
        }}
        >
            System Arm:
        </header>
    )
}