# Dark Circles Detection - React Frontend

A modern, responsive React frontend for the Dark Circles Detection API.

## Features

- 🖼️ **Image Upload**: Drag-and-drop or click to upload images
- 🔍 **Real-time Analysis**: Get instant AI-powered dark circles detection
- 📊 **Detailed Results**: View prediction severity, causes, and remedies
- 🎨 **Modern UI**: Beautiful, responsive design with smooth animations
- 📱 **Mobile Friendly**: Works seamlessly on all devices

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- The FastAPI backend running on `http://localhost:8000`

## Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Configuration

The frontend is configured to connect to the FastAPI backend at `http://localhost:8000` by default.

To change the API URL, create a `.env` file in the `frontend` directory:
```
REACT_APP_API_URL=http://your-api-url:8000
```

## Running the Application

1. Make sure your FastAPI backend is running on port 8000.

2. Start the React development server:
```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Building for Production

To create a production build:

```bash
npm run build
```

This creates an optimized build in the `build` folder that can be served by any static file server.

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── ImageUpload.js
│   │   ├── ImageUpload.css
│   │   ├── ImagePreview.js
│   │   ├── ImagePreview.css
│   │   ├── ResultsDisplay.js
│   │   ├── ResultsDisplay.css
│   │   ├── LoadingSpinner.js
│   │   └── LoadingSpinner.css
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   └── index.css
├── package.json
└── README.md
```

## Usage

1. Click or drag and drop an image to upload
2. Click "Analyze Image" to process the image
3. View the results including:
   - Prediction severity (High, Moderate, Low, or No dark circles)
   - Possible causes
   - Recommended remedies

## Technologies Used

- React 18
- Axios for API calls
- CSS3 for styling
- Modern ES6+ JavaScript

