
/**
 * This is the header for the inventory section.
 * 
 * All this file does is export the header 
 * with 10 pixels of padding on top and bottom.
 */

export default function InventoryHeader () {

    return (
        <header 
        className="Inventory-Header" 
        style = {{
            padding : "10px"
        }}
        >
            Current Inventory:
        </header>
    )
}