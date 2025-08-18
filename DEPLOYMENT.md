# Deployment Checklist for Render

## Pre-Deployment Checklist

### 1. Code Preparation
- [ ] All code is committed to Git repository
- [ ] `.gitignore` is properly configured
- [ ] `requirements.txt` is up to date
- [ ] `build.sh` is executable (`chmod +x build.sh` on Unix systems)

### 2. Configuration Files
- [ ] `render.yaml` is configured
- [ ] `backend/settings.py` has production settings
- [ ] Environment variables are documented

### 3. Testing
- [ ] Local development server runs without errors
- [ ] WebSocket connections work locally
- [ ] Health check endpoint responds correctly

## Deployment Steps

### Step 1: Prepare Repository
```bash
# Make sure all files are committed
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Step 2: Deploy to Render
1. Go to https://render.com
2. Sign up/Login
3. Click "New +" → "Web Service"
4. Connect your Git repository
5. Configure the service:
   - **Name**: `stranger-chat-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn backend.asgi:application -k uvicorn.workers.UvicornWorker`
   - **Plan**: Free (for testing)

### Step 3: Environment Variables
Render will automatically generate:
- `SECRET_KEY`: Auto-generated
- `RENDER`: Set to `true` automatically

Optional (for production):
- `REDIS_URL`: If using Redis

### Step 4: Deploy
Click "Create Web Service" and wait for deployment to complete.

### Step 5: Test Deployment
1. Check the health endpoint: `https://your-app-name.onrender.com/health/`
2. Test WebSocket connection
3. Update Flutter app with new WebSocket URL

## Post-Deployment

### Update Flutter App
Change the WebSocket URL in `main.dart`:
```dart
static const String WS_URL = 'wss://your-app-name.onrender.com/ws/chat/';
```

### Monitor Deployment
- Check Render dashboard for logs
- Monitor health endpoint
- Test WebSocket functionality

## Troubleshooting

### Common Issues
1. **Build fails**: Check `build.sh` permissions and requirements.txt
2. **WebSocket not working**: Verify ASGI configuration
3. **Static files not loading**: Check STATIC_ROOT and collectstatic
4. **Database errors**: Ensure migrations are running

### Logs
- Check Render dashboard logs
- Use `python manage.py runserver` locally for debugging
- Test health endpoint: `/health/`

## Production Considerations

### Performance
- Upgrade to paid Render plan for better performance
- Add Redis for WebSocket scaling
- Use PostgreSQL instead of SQLite

### Security
- Keep SECRET_KEY secure
- Use HTTPS (automatic on Render)
- Consider adding authentication

### Monitoring
- Set up health checks
- Monitor WebSocket connections
- Track error rates
