# Production Deployment Guide for Stranger Chat

This guide will help you deploy your Django chat application to Render.com with all the necessary configurations.

## 🚀 Prerequisites

- A Render.com account
- Git repository with your code
- Basic understanding of Django deployment

## 📋 Environment Variables

Set these environment variables in your Render dashboard:

### Required Variables:
```
SECRET_KEY=your-generated-secret-key
DEBUG=false
ALLOWED_HOSTS=.onrender.com
```

### Database Variables (Auto-configured):
- `DATABASE_URL` - Automatically set by Render
- `REDIS_URL` - Automatically set by Render

## 🗄️ Database Setup

1. **PostgreSQL Database**: Render will automatically create a PostgreSQL database
2. **Redis Instance**: Render will create a Redis instance for WebSocket support
3. **Migrations**: The build script will automatically run migrations

## 🔧 Build Process

The build script (`build.sh`) will:
1. Install all Python dependencies
2. Collect static files
3. Run database migrations
4. Set up the production environment

## 🌐 WebSocket Configuration

- **ASGI Server**: Using Daphne for WebSocket support
- **Redis Backend**: For production WebSocket scaling
- **Port Configuration**: Automatically handled by Render

## 📁 Static Files

- **WhiteNoise**: Handles static file serving
- **Compression**: Static files are automatically compressed
- **CDN Ready**: Configured for production use

## 🔒 Security Features

- **HTTPS**: Automatically enforced
- **HSTS**: HTTP Strict Transport Security enabled
- **Secure Cookies**: All cookies are secure in production
- **CSRF Protection**: Enabled by default

## 🚀 Deployment Steps

1. **Connect Repository**: Link your Git repository to Render
2. **Auto-Deploy**: Enable automatic deployments on push
3. **Environment Variables**: Set the required environment variables
4. **Deploy**: Render will automatically build and deploy

## 📊 Monitoring

- **Health Check**: `/health/` endpoint for monitoring
- **Logs**: Available in Render dashboard
- **Metrics**: Built-in performance monitoring

## 🔄 Updates

To update your application:
1. Push changes to your Git repository
2. Render will automatically rebuild and deploy
3. Database migrations run automatically
4. Zero-downtime deployments

## 🐛 Troubleshooting

### Common Issues:

1. **Build Failures**: Check the build logs in Render dashboard
2. **Database Connection**: Verify DATABASE_URL is set correctly
3. **WebSocket Issues**: Ensure Redis is running and accessible
4. **Static Files**: Check if collectstatic ran successfully

### Debug Mode:

If you need to debug in production:
1. Set `DEBUG=true` temporarily
2. Check logs in Render dashboard
3. Remember to set back to `false`

## 📈 Scaling

- **Auto-scaling**: Available on higher plans
- **Load Balancing**: Built-in with Render
- **Database Scaling**: PostgreSQL plans can be upgraded

## 💰 Cost Optimization

- **Starter Plan**: Sufficient for most applications
- **Auto-sleep**: Services sleep when not in use
- **Resource Limits**: Monitor usage in dashboard

## 🔗 Useful Links

- [Render Documentation](https://render.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [Channels Documentation](https://channels.readthedocs.io/)

## ✅ Deployment Checklist

- [ ] Environment variables configured
- [ ] Database migrations ready
- [ ] Static files collected
- [ ] WebSocket endpoints working
- [ ] Health check endpoint responding
- [ ] SSL certificate active
- [ ] Monitoring configured
- [ ] Backup strategy in place

## 🎉 Success!

Once deployed, your application will be available at:
`https://your-app-name.onrender.com`

The chat functionality will work with WebSockets, user authentication, and location tracking (IP-based) all configured for production use.
