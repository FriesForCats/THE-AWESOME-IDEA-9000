import React, { useState, useEffect } from 'react'; // Fixes undefined errors in image_a76ae3.png

// 1. The Item Component (Fixes the literal text issue in image_a7673a.png)
// We destructure { name, stock } from props to make the code cleaner.
function Item({ name, stock }) {
    const isLowStock = stock < 5;
    return (
        <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '15px 20px',
            margin: '10px 0',
            backgroundColor: '#2d3436',
            borderRadius: '8px',
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
            color: 'white',
            borderLeft: isLowStock ? '5px solid #ff7675' : '5px solid #55efc4'
        }}>
            <span style={{ fontSize: '1.2rem', textTransform: 'capitalize', fontWeight: '500' }}>
                {name}
            </span>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <span style={{ color: '#b2bec3', fontSize: '0.9rem' }}>Stock:</span>
                <span style={{ 
                    fontSize: '1.4rem', 
                    fontWeight: 'bold',
                    color: isLowStock ? '#ff7675' : '#55efc4' 
                }}>
                    {stock}
                </span>
            </div>
        </div>
    );
}

// 2. The Main InventoryList Component
export default function InventoryList() {
    // Initialize state as an empty array
    const [food, setFood] = useState([]);

    // Fetch data from your Flask endpoint when the component mounts
    useEffect(() => {
    const fetchData = () => {
        fetch('http://127.0.0.1:5000/api/inventory')
            .then(res => res.json())
            .then(data => setFood(data))
            .catch(err => console.error("Fetch error:", err));
    };

    fetchData(); // Initial pull
    const interval = setInterval(fetchData, 3000); // Pull every 3 seconds

    return () => clearInterval(interval); // Cleanup on close
}, []);

    return (
        <div className="Inventory-Container">
            
            <div className="Inventory-List">
                {food.length > 0 ? (
                    food.map((item, index) => (
                        <Item 
                            key={index} 
                            name={item.name} 
                            stock={item.stock} 
                        />
                    ))
                ) : (
                    <p>Loading inventory data...</p>
                )}
            </div>
        </div>
    );
}