import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import ImageUpload from './components/ImageUpload';
import ImagePreview from './components/ImagePreview';
import ResultsDisplay from './components/ResultsDisplay';
import LoadingSpinner from './components/LoadingSpinner';
import CameraCapture from './components/CameraCapture';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://rotation-augmentation-1.onrender.com';

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showCamera, setShowCamera] = useState(false);

  const handleImageSelect = (file) => {
    if (file) {
      setSelectedImage(file);
      setResults(null);
      setError(null);
      
      // Create preview URL
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewUrl(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handlePredict = async () => {
    if (!selectedImage) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedImage);

      const response = await axios.post(`${API_BASE_URL}/predict`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResults(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail || 
        err.message || 
        'Failed to process image. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setPreviewUrl(null);
    setResults(null);
    setError(null);
  };

  const handleCameraCapture = (file) => {
    setShowCamera(false);
    handleImageSelect(file);
  };

  const handleCameraClose = () => {
    setShowCamera(false);
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1 className="title">Dark Circles Detection</h1>
          <p className="subtitle">AI-powered analysis of dark circles under your eyes</p>
        </header>

        <main className="main-content">
          {!previewUrl ? (
            <ImageUpload 
              onImageSelect={handleImageSelect}
              onCameraClick={() => setShowCamera(true)}
            />
          ) : (
            <div className="content-wrapper">
              <ImagePreview 
                imageUrl={previewUrl} 
                onReset={handleReset}
              />
              
              {!results && !loading && (
                <div className="action-section">
                  <button 
                    className="predict-button"
                    onClick={handlePredict}
                  >
                    Analyze Image
                  </button>
                </div>
              )}

              {loading && <LoadingSpinner />}

              {error && (
                <div className="error-message">
                  <p>⚠️ {error}</p>
                </div>
              )}

              {results && <ResultsDisplay results={results} />}
            </div>
          )}
        </main>

        <footer className="footer">
          <p>Powered by YOLO AI Model</p>
        </footer>
      </div>

      {showCamera && (
        <CameraCapture
          onCapture={handleCameraCapture}
          onClose={handleCameraClose}
        />
      )}
    </div>
  );
}

export default App;

