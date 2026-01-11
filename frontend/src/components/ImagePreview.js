import React from 'react';
import './ImagePreview.css';

const ImagePreview = ({ imageUrl, onReset }) => {
  return (
    <div className="image-preview-container">
      <div className="preview-header">
        <h3>Selected Image</h3>
        <button className="reset-button" onClick={onReset}>
          Choose Different Image
        </button>
      </div>
      <div className="preview-image-wrapper">
        <img 
          src={imageUrl} 
          alt="Preview" 
          className="preview-image"
        />
      </div>
    </div>
  );
};

export default ImagePreview;

