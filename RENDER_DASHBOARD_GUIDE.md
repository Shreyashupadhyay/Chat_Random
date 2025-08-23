# 🎯 Render Dashboard Visual Guide

## 📱 Dashboard Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    RENDER DASHBOARD                        │
├─────────────────────────────────────────────────────────────┤
│  [New +]  [Search]  [Settings]  [Help]                    │
├─────────────────────────────────────────────────────────────┤
│  Services: 3  |  Databases: 2  |  Static Sites: 0         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │ Web Service     │  │ PostgreSQL      │  │ Redis       │ │
│  │ stranger-chat   │  │ stranger-chat   │  │ stranger-   │ │
│  │ ● Running       │  │ ● Running       │  │ chat-redis  │ │
│  │                 │  │                 │  │ ● Running   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Creating Services Step-by-Step

### Step 1: Create PostgreSQL Database

```
┌─────────────────────────────────────────────────────────────┐
│                    NEW SERVICE                             │
├─────────────────────────────────────────────────────────────┤
│  Select Service Type:                                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │ ● PostgreSQL   │  │   Redis         │  │ Web Service │ │
│  │   Database     │  │   In-Memory     │  │   Django    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  Name: stranger-chat-db                                    │
│  Database: stranger_chat                                   │
│  User: stranger_chat_user                                  │
│  Plan: ● Starter (Free)  ○ Standard  ○ Pro                │
│  Region: ● Oregon (US West)                                │
├─────────────────────────────────────────────────────────────┤
│  [Create Database]                                         │
└─────────────────────────────────────────────────────────────┘
```

### Step 2: Create Redis Service

```
┌─────────────────────────────────────────────────────────────┐
│                    NEW SERVICE                             │
├─────────────────────────────────────────────────────────────┤
│  Select Service Type:                                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   PostgreSQL   │  │ ● Redis         │  │ Web Service │ │
│  │   Database     │  │   In-Memory     │  │   Django    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  Name: stranger-chat-redis                                 │
│  Plan: ● Starter (Free)  ○ Standard  ○ Pro                │
│  Region: ● Oregon (US West)                                │
│  Max Memory Policy: allkeys-lru                            │
├─────────────────────────────────────────────────────────────┤
│  [Create Redis]                                            │
└─────────────────────────────────────────────────────────────┘
```

### Step 3: Create Web Service

```
┌─────────────────────────────────────────────────────────────┐
│                    NEW SERVICE                             │
├─────────────────────────────────────────────────────────────┤
│  Select Service Type:                                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   PostgreSQL   │  │   Redis         │  │ ● Web       │ │
│  │   Database     │  │   In-Memory     │  │   Service   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  Connect Repository:                                       │
│  [Connect Account] [GitHub] [GitLab] [Bitbucket]           │
│  Repository: your-username/stranger-chat                   │
│  Branch: main                                              │
├─────────────────────────────────────────────────────────────┤
│  Name: stranger-chat-backend                               │
│  Environment: Python                                       │
│  Plan: ● Starter (Free)  ○ Standard  ○ Pro                │
│  Region: ● Oregon (US West)                                │
├─────────────────────────────────────────────────────────────┤
│  Build Command: chmod +x build.sh && ./build.sh            │
│  Start Command: daphne backend.asgi:application -b 0.0.0.0 -p $PORT │
├─────────────────────────────────────────────────────────────┤
│  [Create Web Service]                                      │
└─────────────────────────────────────────────────────────────┘
```

## 🔗 Linking Services

### Environment Variables Setup

```
┌─────────────────────────────────────────────────────────────┐
│              ENVIRONMENT VARIABLES                         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┬─────────────────┬─────────────────┐  │
│  │ Key            │ Value           │ Actions         │  │
│  ├─────────────────┼─────────────────┼─────────────────┤  │
│  │ SECRET_KEY     │ [Generate]      │ [Edit] [Delete] │  │
│  │ DEBUG          │ false           │ [Edit] [Delete] │  │
│  │ ALLOWED_HOSTS  │ .onrender.com   │ [Edit] [Delete] │  │
│  │ DATABASE_URL   │ [Link Database] │ [Edit] [Delete] │  │
│  │ REDIS_URL      │ [Link Redis]    │ [Edit] [Delete] │  │
│  └─────────────────┴─────────────────┴─────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  [Add Variable]                                            │
└─────────────────────────────────────────────────────────────┘
```

### Linking Database

```
┌─────────────────────────────────────────────────────────────┐
│                    LINK DATABASE                           │
├─────────────────────────────────────────────────────────────┤
│  Select Database to Link:                                  │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ ● stranger-chat-db                                      │ │
│  │   PostgreSQL • Oregon (US West)                         │ │
│  │   Status: Running                                       │ │
│  └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  Environment Variable Name: DATABASE_URL                   │
│  [Link Database]                                           │
└─────────────────────────────────────────────────────────────┘
```

### Linking Redis

```
┌─────────────────────────────────────────────────────────────┐
│                     LINK REDIS                             │
├─────────────────────────────────────────────────────────────┤
│  Select Redis Service to Link:                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ ● stranger-chat-redis                                   │ │
│  │   Redis • Oregon (US West)                              │ │
│  │   Status: Running                                       │ │
│  └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  Environment Variable Name: REDIS_URL                      │
│  [Link Redis]                                              │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Monitoring Dashboard

### Service Status Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    SERVICE STATUS                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │ Web Service     │  │ PostgreSQL      │  │ Redis       │ │
│  │ ● Running       │  │ ● Running       │  │ ● Running   │ │
│  │ Uptime: 2h 15m │  │ Size: 45MB      │  │ Memory: 12%│ │
│  │ Requests: 1.2k  │  │ Connections: 8  │  │ Commands: 5k│ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  Health Check: ✅ /health/ endpoint responding             │
│  Last Deploy: 2 hours ago                                 │
│  Build Status: ✅ Success                                  │
└─────────────────────────────────────────────────────────────┘
```

### Build Logs

```
┌─────────────────────────────────────────────────────────────┐
│                      BUILD LOGS                            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ [INFO] Installing dependencies...                       │ │
│  │ [INFO] Collecting static files...                       │ │
│  │ [INFO] Running database migrations...                   │ │
│  │ [SUCCESS] Build completed successfully!                 │ │
│  │ [INFO] Starting daphne server...                        │ │
│  │ [INFO] Server running on port 10000                     │ │
│  └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  [Download Logs] [View Full Logs]                          │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Configuration Tips

### 1. Service Naming Convention
```
stranger-chat-backend    (Web Service)
stranger-chat-db         (PostgreSQL)
stranger-chat-redis      (Redis)
```

### 2. Region Selection
- **Choose the same region** for all services
- **Oregon (US West)** is recommended for US users
- **Frankfurt (EU Central)** for European users

### 3. Plan Selection
- **Start with Starter plans** (Free tier)
- **Upgrade when needed** based on usage
- **Monitor resource usage** in dashboard

### 4. Environment Variables Priority
```
1. Linked Services (DATABASE_URL, REDIS_URL)
2. Manual Environment Variables (SECRET_KEY, DEBUG)
3. Default Values (from Django settings)
```

## ✅ Success Checklist

- [ ] **All services created** in same region
- [ ] **Services linked** via environment variables
- [ ] **Build command** set correctly
- [ ] **Start command** configured for ASGI
- **Health check endpoint** responding
- **Database migrations** completed
- **WebSocket connections** working
- **Static files** served correctly

---

**🎯 Follow this visual guide to set up your Render services successfully!**
