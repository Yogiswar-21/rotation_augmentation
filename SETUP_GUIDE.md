# Setup and Testing Guide

This guide will help you set up and test both the backend and frontend of the Dark Circles Detection application.

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher (and npm)
- A webcam (for camera feature testing)
- A test image file (for file upload testing)

---

## Step 1: Backend Setup

### 1.1 Install Python Dependencies

Open a terminal in the project root directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI
- Uvicorn (ASGI server)
- Ultralytics (YOLO)
- Pillow (image processing)
- OpenCV (for camera features)
- NumPy

### 1.2 Verify Model File

Make sure you have a model file (e.g., `best (7).pt`) in the project root directory. The backend will automatically find and load it.

### 1.3 Start the Backend Server

Run the FastAPI server:

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
Attempting to load model from: /path/to/best (7).pt
Model loaded successfully from: /path/to/best (7).pt
INFO:     Application startup complete.
```

### 1.4 Test Backend Endpoints

Open your browser and visit:

1. **API Root**: http://localhost:8000
   - Should show API information and available endpoints

2. **Health Check**: http://localhost:8000/health
   - Should return: `{"status": "healthy", "model_loaded": true, ...}`

3. **API Documentation**: http://localhost:8000/docs
   - FastAPI automatically generates interactive API documentation
   - You can test the `/predict` endpoint directly from here

**Keep the backend server running** - don't close this terminal!

---

## Step 2: Frontend Setup

### 2.1 Install Node Dependencies

Open a **new terminal** (keep the backend running) and navigate to the frontend directory:

```bash
cd frontend
npm install
```

This will install:
- React
- React DOM
- React Scripts
- Axios (for API calls)

### 2.2 Start the Frontend Development Server

```bash
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view dark-circles-detection-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000

Note that the development build is not optimized.
To create a production build, use npm run build.
```

The React app should automatically open in your browser at `http://localhost:3000`

---

## Step 3: Testing the Application

### 3.1 Test File Upload Feature

1. **Upload an Image:**
   - Click on the upload area or drag and drop an image
   - Supported formats: JPG, PNG, GIF, WEBP (Max 10MB)

2. **Preview:**
   - After selecting an image, you should see a preview
   - Click "Choose Different Image" to go back

3. **Analyze:**
   - Click the "Analyze Image" button
   - Wait for the analysis (you'll see a loading spinner)
   - Results should appear showing:
     - Prediction severity (High/Moderate/Low/No)
     - Possible causes
     - Recommended remedies
     - Confidence score

### 3.2 Test Camera Feature

1. **Open Camera:**
   - Click the "Use Camera" button
   - Allow camera permissions when prompted by your browser

2. **Capture Photo:**
   - Position your face in the camera frame
   - Click "Capture Photo" button
   - The camera will close and show the captured image

3. **Analyze:**
   - Click "Analyze Image" to process the captured photo
   - View the results

### 3.3 Verify Backend Connection

Check the browser's Developer Console (F12):
- **Network Tab**: Should show successful API calls to `http://localhost:8000/predict`
- **Console Tab**: Should not show any CORS errors

---

## Step 4: Troubleshooting

### Backend Issues

**Problem: Model not loading**
- Check if the `.pt` model file exists in the project root
- Verify the model file name contains "best" (case-insensitive)
- Check the console output for error messages

**Problem: Port 8000 already in use**
- Change the port in `main.py`: `uvicorn.run(app, host="0.0.0.0", port=8001)`
- Update frontend `.env` file: `REACT_APP_API_URL=http://localhost:8001`

**Problem: Module not found errors**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check if you're using the correct Python environment

### Frontend Issues

**Problem: CORS errors**
- Make sure the backend is running
- Verify CORS middleware is added in `main.py`
- Check that the backend URL matches in `App.js`

**Problem: Camera not working**
- Check browser permissions (Settings → Privacy → Camera)
- Try a different browser (Chrome/Firefox recommended)
- Make sure you're using HTTPS or localhost (required for camera access)

**Problem: npm install fails**
- Clear cache: `npm cache clean --force`
- Delete `node_modules` and `package-lock.json`, then run `npm install` again
- Check Node.js version: `node --version` (should be 14+)

**Problem: Page not loading**
- Check if port 3000 is available
- Look for errors in the terminal where `npm start` is running
- Check browser console for errors

### Connection Issues

**Problem: Cannot connect to backend**
- Verify backend is running on port 8000
- Test backend directly: http://localhost:8000/health
- Check firewall settings
- Verify `API_BASE_URL` in `App.js` matches your backend URL

---

## Step 5: Quick Test Checklist

- [ ] Backend server starts without errors
- [ ] Model loads successfully (check console output)
- [ ] Backend health endpoint returns `"model_loaded": true`
- [ ] Frontend starts and opens in browser
- [ ] File upload works (drag & drop or click)
- [ ] Image preview displays correctly
- [ ] Analysis returns results
- [ ] Camera opens and requests permission
- [ ] Camera capture works
- [ ] No CORS errors in browser console
- [ ] Results display correctly with causes and remedies

---

## Running Both Servers

You need **two terminal windows**:

**Terminal 1 - Backend:**
```bash
cd "/home/rguktrkvalley/Downloads/Rotation  Augmentation/25 epochs"
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd "/home/rguktrkvalley/Downloads/Rotation  Augmentation/25 epochs/frontend"
npm start
```

Both should be running simultaneously for the app to work!

---

## Production Build (Optional)

To create a production build of the frontend:

```bash
cd frontend
npm run build
```

This creates an optimized build in the `frontend/build` directory that can be served by any web server.

---

## Need Help?

- Check the browser console (F12) for JavaScript errors
- Check the backend terminal for Python errors
- Verify all dependencies are installed correctly
- Make sure both servers are running on the correct ports

