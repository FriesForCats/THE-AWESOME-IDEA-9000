/**
 * This is the file that handles both the camera feed and 
 * the change camera button
 * 
 * To start, we import some functions for later use 
 */

import {useEffect , useRef , useState} from "react";

export default function Camera() {
    const videoRef = useRef(null);
    const [devices , setDevices] = useState([]);
    const [activeDeviceIdx , setActiveDeviceIdx] = useState(0)

    /** Creates a list of all camera outputs to assign
     * to the change camera button. If it doesn't detect
     * a camera, it prints an error to the console and 
     * the button doesn't display.
    */
   
    useEffect(() => {
        const getCameras = async () => {
            try {
                await navigator.mediaDevices.getUserMedia({ video : true});
                const allDevices = await navigator.mediaDevices.enumerateDevices();
                const videoDevices = allDevices.filter(device => device.kind === "videoinput");
                setDevices(videoDevices);
            } catch (err) {
                console.error("Error listing cameras:" , err)
            }
        };
        getCameras();
    } , []);

    /** 
     * Takes the list of devices produced from the above
     * section and displays the corresponding feed. If
     * there is an error when attempting to display
     * the feed, it prints an error to the console.
     */

    useEffect(() => {
        if (devices.length === 0) return;

        let stream;
        const constraints = {
            video : {
                deviceId : {exact : devices[activeDeviceIdx].deviceId},
                aspectRatio : 1.333
            }
        }

        navigator.mediaDevices.getUserMedia(constraints)
            .then(s => {
                stream = s;
                if (videoRef.current) {
                    videoRef.current.srcObject = stream;
                }
            })
            .catch(err => console.error("Error starting stream:" , err))
        
        return () => {
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
            }
        };
    } , [activeDeviceIdx , devices])

    /**
     * This variable takes the current/previous
     * index of the camera feed list and increments
     * it by one when called. 
     * 
     * (prevIdx +1) % devices.length handles the logic
     * for looping over the index values.
     */
    const toggleCamera = () => {
        setActiveDeviceIdx((prevIdx) => (prevIdx + 1) % devices.length);
    };

    /**
     * This returns the assembled camera component 
     * for the DOM to display
     */
    return (
        <div>
            <video 
                ref={videoRef} 
                autoPlay 
                playsInline 
                style={{width: "100%", height: "100%", objectFit: "cover"}}
            />
            {devices.length > 1 && (
                <button 
                className= 'Change-Camera'
                onClick = {toggleCamera}
                >
                    Change Cameras
                </button>
            )}
        </div>
    );
}