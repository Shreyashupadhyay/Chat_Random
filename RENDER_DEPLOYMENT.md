# Quick Render Deployment Guide

## ✅ Fixed Configuration

The deployment issue has been resolved! Here's the updated configuration:

### Build Command
```
./build.sh
```

### Start Command
```
daphne backend.asgi:application -b 0.0.0.0 -p $PORT
```

## 🚀 Deployment Steps

1. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Fix ASGI configuration for Render deployment"
   git push origin main
   ```

2. **On Render Dashboard**:
   - Go to your web service
   - Update the **Start Command** to: `daphne backend.asgi:application -b 0.0.0.0 -p $PORT`
   - Click "Save Changes"
   - Wait for automatic redeployment

## 🔧 What Was Fixed

1. **ASGI Configuration**: Added `django.setup()` to properly initialize Django
2. **Start Command**: Changed from Gunicorn to Daphne for better ASGI support
3. **Dependencies**: Ensured all required packages are in `requirements.txt`

## 🌐 Your Endpoints

Once deployed, your app will be available at:
- **WebSocket**: `wss://your-app-name.onrender.com/ws/chat/`
- **Health Check**: `https://your-app-name.onrender.com/health/`
- **Admin**: `https://your-app-name.onrender.com/admin/`

## 📱 Update Flutter App

Change your Flutter app's WebSocket URL to:
```dart
static const String WS_URL = 'wss://your-app-name.onrender.com/ws/chat/';
```

## ✅ Test Deployment

1. Visit the health endpoint in your browser
2. Check Render logs for any errors
3. Test WebSocket connection from Flutter app

Your chat application should now deploy successfully on Render!
