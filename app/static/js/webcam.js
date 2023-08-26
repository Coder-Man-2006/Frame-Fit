async function openWebcam() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        const webcamVideo = document.getElementById('webcam');
        webcamVideo.srcObject = stream;

        // Start the loop to process webcam frames
        processWebcamFrame();
    } catch (error) {
        console.error('Error accessing webcam:', error);
    }
}

function processWebcamFrame() {
    const webcamVideo = document.getElementById('webcam');
    const processedImageElement = document.getElementById('processedImage');

    if (webcamVideo.readyState === webcamVideo.HAVE_ENOUGH_DATA) {
        const canvas = document.createElement('canvas');
        canvas.width = webcamVideo.videoWidth;
        canvas.height = webcamVideo.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(webcamVideo, 0, 0);

        const formData = new FormData();
        formData.append('frame', canvas.toDataURL('image/png'));

        fetch('/process_frame', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.processed_image) {
                processedImageElement.src = data.processed_image;
            }
        })
        .catch(error => {
            console.error('Error executing Python code:', error);
        });
    }

    // Keep sending frames for processing using requestAnimationFrame for better performance
    requestAnimationFrame(processWebcamFrame);
}

// Initialize the webcam capture
openWebcam();