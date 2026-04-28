import {useEffect , useRef} from "react";

function Camera() {
    const videoRef = useRef(null);

    useEffect(() => {
        //Make a variable to hold the video stream from the camera
        let stream;

        //Ask for camera permissions, if so display it, if not give an error
        navigator.mediaDevices.getUserMedia({video: true})
            .then(s => {
                stream = s;
                videoRef.current.srcObject = stream;
            })
            .catch(err => {
                console.error("Error accessing webcam:" , err);
            });

        //If access to video is lost for whatever reason, cleanup the stream
        return () => {
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
            }
        };
    } , []);

    return (
        <div>
            <video 
            ref={videoRef} 
            autoPlay 
            playsInline 
            style={{width: "100%", height: "100%", objectFit: "cover"}}
            />
        </div>
    );
}

export default Camera;