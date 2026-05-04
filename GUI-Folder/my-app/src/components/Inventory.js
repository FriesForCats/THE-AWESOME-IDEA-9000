
const Item = ({name , stock}) => {

    return (
        <div
        style = {{
            border: "1px solid #ccc" , 
            width: "100%" ,
            minWidth: 0
        }}
        >
            <div
            style = {{
                background : "#4f535d" ,
                padding : "10px",
            }}
            >
                {name}: {stock}
            </div>
        </div>
    )
}

export default function InventoryList () {

    const food = [
        {name : "Apple" , stock : 2 }
    ]

    return (
        <div className="Inventory-List">
            {food.map((item , index) => (
                <Item
                key = {index}
                name = {item.name}
                stock = {item.stock}
                />
            ))}
        </div>
    );
}