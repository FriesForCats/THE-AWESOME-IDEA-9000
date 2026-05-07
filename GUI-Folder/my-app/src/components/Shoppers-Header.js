
/**
 * This is the header for the shoppers section in the 
 * top right
 * 
 * All this does is return a header with 10 pixels of 
 * padding on top and bottom
 */

export default function ShoppersHeader () {

    return (
        <header
        className= "Shoppers-Header"
        style = {{
            padding : "10px"
        }}
        >
            Current Carts:
        </header>
    )
}