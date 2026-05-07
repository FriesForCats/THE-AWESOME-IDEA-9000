import { useState, useEffect } from 'react';

const Dropdown = ({ title, content }) => {
    const [open, setOpen] = useState(false);

    return (
        <div style={{ borderBottom: "1px solid #34495e", width: "100%", minWidth: 0 }}>
            <div
                onClick={() => setOpen(!open)}
                style={{
                    padding: "12px",
                    cursor: "pointer",
                    background: "#1e272e", // Matches your sidebar theme
                    color: "white",
                    display: "flex",
                    justifyContent: "space-between"
                }}
            >
                <span>{title}</span>
                <span>{open ? '▲' : '▼'}</span>
            </div>
            {open && (
                <div style={{ padding: "15px", background: "#161d24", color: "#b2bec3", fontSize: "0.9rem" }}>
                    {content}
                </div>
            )}
        </div>
    );
};

export default function Shoppers() {
    const [logs, setLogs] = useState([]);

    useEffect(() => {
        const fetchLogs = () => {
            fetch('http://127.0.0.1:5000/logs')
                .then(res => res.json())
                .then(data => setLogs(data))
                .catch(err => console.error("Error fetching logs:", err));
        };

        fetchLogs();
        const interval = setInterval(fetchLogs, 2000); // Live updates every 2 seconds
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="Accordion" style={{ borderRadius: '8px', overflow: 'hidden' }}>
            {logs.length > 0 ? (
                logs.map((log) => (
                    <Dropdown 
                        key={log.id}
                        // The Title shows the Action and the Item
                        title={`${log.status}: ${log.label}`}
                        // The Content shows the details when clicked
                        content={
                            <div>
                                <p><strong>Time:</strong> {log.timestamp}</p>
                                <p><strong>Confidence:</strong> {(log.confidence * 100).toFixed(1)}%</p>
                                <p><strong>Database ID:</strong> #{log.id}</p>
                            </div>
                        }
                    />
                ))
            ) : (
                <div style={{ padding: '20px', color: '#636e72', textAlign: 'center' }}>
                    No activity detected yet.
                </div>
            )}
        </div>
    );
}