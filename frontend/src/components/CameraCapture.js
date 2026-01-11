import React, { useRef, useState, useEffect } from 'react';
import './CameraCapture.css';

const CameraCapture = ({ onCapture, onClose }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [error, setError] = useState(null);
  const [isCapturing, setIsCapturing] = useState(false);

  useEffect(() => {
    startCamera();
    return () => {
      stopCamera();
    };
  }, []);

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: 'user', // Front-facing camera
          width: { ideal: 1280 },
          height: { ideal: 720 }
        }
      });
      
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
      setError(null);
    } catch (err) {
      console.error('Error accessing camera:', err);
      setError(
        err.name === 'NotAllowedError'
          ? 'Camera access denied. Please allow camera permissions and try again.'
          : err.name === 'NotFoundError'
          ? 'No camera found. Please connect a camera and try again.'
          : 'Failed to access camera. Please check your camera settings.'
      );
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
  };

  const capturePhoto = () => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');

    // Set canvas dimensions to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw the current video frame to canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert canvas to blob
    canvas.toBlob((blob) => {
      if (blob) {
        // Create a File object from the blob
        const file = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' });
        onCapture(file);
        stopCamera();
      }
    }, 'image/jpeg', 0.95);
  };

  const handleClose = () => {
    stopCamera();
    onClose();
  };

  return (
    <div className="camera-capture-overlay">
      <div className="camera-capture-container">
        <div className="camera-header">
          <h3>Camera Capture</h3>
          <button className="close-button" onClick={handleClose}>
            ✕
          </button>
        </div>

        {error ? (
          <div className="camera-error">
            <p>⚠️ {error}</p>
            <button className="retry-button" onClick={startCamera}>
              Try Again
            </button>
          </div>
        ) : (
          <>
            <div className="video-container">
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className="camera-video"
              />
              <canvas ref={canvasRef} style={{ display: 'none' }} />
            </div>

            <div className="camera-controls">
              <button
                className="capture-button"
                onClick={capturePhoto}
                disabled={!stream}
              >
                <span className="capture-icon">📷</span>
                Capture Photo
              </button>
            </div>

            <div className="camera-hint">
              <p>Position your face in the frame and click "Capture Photo"</p>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default CameraCapture;

