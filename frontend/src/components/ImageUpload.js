import React, { useRef } from 'react';
import './ImageUpload.css';

const ImageUpload = ({ onImageSelect, onCameraClick }) => {
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validate file type
      if (!file.type.startsWith('image/')) {
        alert('Please select a valid image file');
        return;
      }
      // Validate file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        alert('Image size should be less than 10MB');
        return;
      }
      onImageSelect(file);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      if (file.size > 10 * 1024 * 1024) {
        alert('Image size should be less than 10MB');
        return;
      }
      onImageSelect(file);
    }
  };

  return (
    <div 
      className="image-upload-container"
      onDragOver={handleDragOver}
      onDrop={handleDrop}
    >
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        style={{ display: 'none' }}
      />
      
      <div className="upload-area" onClick={handleClick}>
        <div className="upload-icon">
          <svg 
            width="64" 
            height="64" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            strokeWidth="2"
          >
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="17 8 12 3 7 8" />
            <line x1="12" y1="3" x2="12" y2="15" />
          </svg>
        </div>
        <h3 className="upload-title">Upload an Image</h3>
        <p className="upload-text">
          Click to browse or drag and drop your image here
        </p>
        <p className="upload-hint">
          Supported formats: JPG, PNG, GIF, WEBP (Max 10MB)
        </p>
      </div>

      <div className="upload-divider">
        <span>OR</span>
      </div>

      <button className="camera-button" onClick={onCameraClick}>
        <span className="camera-icon">📷</span>
        Use Camera
      </button>
    </div>
  );
};

export default ImageUpload;

