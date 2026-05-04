import {useState} from 'react';

const Dropdown = ({title , content}) => {
    const [open , setOpen] = useState(false);

    return (
        <div 
        style = {{border: "1px solid #ccc" , 
        marginBottom: "8px"
        }}>
            <div
            onClick = {() => setOpen(!open)}
            style = {{
                padding : "10px",
                cursor : "pointer",
                background : "#000000",
            }}
            >
                {title}
            </div>
            {open && (
                <div style = {{padding : "10px" , background : "#000000"}}>
                    {content}
                </div>
            )}
        </div>
    );
};

export default function Accordion() {
    const data = [
        { title: "Item 1" , content: "Info about Item 1"},
        { title: "Item 2" , content: "Info about Item 2"},
        { title: "Item 3" , content: "Info about Item 3"},
    ];

    return (
        <div>
            {data.map((item , index) => (
                <Dropdown 
                key = {index}
                title = {item.title}
                content = {item.content}
                />
            ))}
        </div>
    );
}