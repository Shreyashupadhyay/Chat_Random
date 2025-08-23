# 🚀 Quick Deployment Checklist for Render

## Before Deploying

- [ ] **Code is committed** to Git repository
- [ ] **All migrations** are created and tested locally
- [ ] **Static files** are properly configured
- [ ] **Environment variables** are ready

## Render Dashboard Setup

### 1. Create New Web Service
- [ ] Connect your Git repository
- [ ] Choose Python environment
- [ ] Set build command: `chmod +x build.sh && ./build.sh`
- [ ] Set start command: `daphne backend.asgi:application -b 0.0.0.0 -p $PORT`

### 2. Environment Variables
- [ ] `SECRET_KEY` - Generate a new one
- [ ] `DEBUG` - Set to `false`
- [ ] `ALLOWED_HOSTS` - Set to `.onrender.com`

### 3. Create Redis Service
- [ ] Add Redis service (Starter plan)
- [ ] Note the Redis URL for environment variables

### 4. Create PostgreSQL Database
- [ ] Add PostgreSQL database (Starter plan)
- [ ] Note the database URL for environment variables

## Post-Deployment

- [ ] **Health check** endpoint responds (`/health/`)
- [ ] **Static files** are served correctly
- [ ] **WebSocket connections** work
- [ ] **Database migrations** completed
- [ ] **Admin interface** accessible
- [ ] **Chat functionality** working

## Monitoring

- [ ] Check **build logs** for any errors
- [ ] Monitor **application logs** for runtime issues
- [ ] Verify **WebSocket connections** in browser console
- [ ] Test **user registration** and **login**

## Common Issues & Solutions

### Build Failures
- Check Python version compatibility
- Verify all dependencies in requirements.txt
- Check build script permissions

### WebSocket Issues
- Ensure Redis service is running
- Check REDIS_URL environment variable
- Verify channels configuration

### Database Issues
- Check DATABASE_URL environment variable
- Ensure migrations ran successfully
- Verify database permissions

## Success Indicators

✅ Application loads without errors  
✅ WebSocket connections establish  
✅ Users can register and login  
✅ Chat rooms create and function  
✅ Admin dashboard accessible  
✅ Static files load correctly  
✅ Health check endpoint responds  

## Next Steps

1. **Monitor** application performance
2. **Set up** custom domain (optional)
3. **Configure** SSL certificates (auto-handled)
4. **Scale** resources as needed
5. **Backup** database regularly

---

**🎉 Your Stranger Chat app is now live on Render!**
