# 🚀 Vercel Deployment Guide for Library Seat Booking Backend

## 📋 Prerequisites
- Vercel Account
- GitHub Repository
- PostgreSQL Database (recommended for production)
- Domain name (optional)

## 🔧 Environment Variables Setup

### 1. Go to Vercel Dashboard
1. Login to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to **Settings** → **Environment Variables**

### 2. Add Required Environment Variables

#### 🔐 Security Variables
```
SECRET_KEY=your-super-secret-key-here-change-this
JWT_SECRET_KEY=your-jwt-secret-key-different-from-django-secret
```

#### 🌐 Production URLs
```
DJANGO_SETTINGS_MODULE=library_seat_booking.production_settings
ALLOWED_HOSTS=your-vercel-app-url.vercel.app
DEBUG=False
```

#### 🗄️ Database (PostgreSQL)
```
DATABASE_URL=postgresql://username:password@host:port/database_name
```

#### 🌍 CORS Settings
```
CORS_ALLOWED_ORIGINS=https://your-frontend-url.vercel.app,https://your-domain.com
CORS_ALLOW_ALL_ORIGINS=False
```

#### 📧 Email Settings (Optional)
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

#### 🔥 Firebase (Optional)
```
FIREBASE_PROJECT_ID=your-firebase-project-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYour-Private-Key\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@your-project.iam.gserviceaccount.com
```

## 📁 File Structure
```
BackendPanel/
├── backend/
│   ├── library_seat_booking/
│   │   ├── settings.py
│   │   ├── production_settings.py
│   │   ├── wsgi.py
│   │   └── urls.py
│   ├── manage.py
│   └── requirements.txt
├── vercel.json
└── .env.example
```

## 🚀 Deployment Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Setup for Vercel deployment"
git push origin main
```

### 2. Connect to Vercel
1. Go to [Vercel](https://vercel.com)
2. Click **Add New...** → **Project**
3. Import your GitHub repository
4. Select the `BackendPanel` folder

### 3. Configure Build Settings
Vercel will automatically detect the `vercel.json` configuration:
- **Build Command**: `pip install -r backend/requirements.txt`
- **Output Directory**: `.vercel/output`
- **Install Command**: `pip install -r backend/requirements.txt`

### 4. Deploy
1. Click **Deploy**
2. Wait for deployment to complete
3. Your API will be available at: `https://your-app-name.vercel.app`

## 🔧 Post-Deployment Setup

### 1. Test API Endpoints
```bash
# Test health check
curl https://your-app.vercel.app/api/

# Test authentication
curl -X POST https://your-app.vercel.app/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"email_or_phone":"test@example.com","password":"password"}'
```

### 2. Update Frontend URLs
Update your Angular frontend to use the new Vercel URL:
```typescript
// In your services
private apiUrl = 'https://your-app.vercel.app/api';
```

### 3. Configure Custom Domain (Optional)
1. Go to **Settings** → **Domains**
2. Add your custom domain
3. Update DNS records as instructed

## 🐛 Common Issues & Solutions

### Issue 1: 500 Internal Server Error
**Solution**: Check environment variables in Vercel dashboard

### Issue 2: CORS Errors
**Solution**: Update `CORS_ALLOWED_ORIGINS` with your frontend URL

### Issue 3: Database Connection Error
**Solution**: Verify `DATABASE_URL` is correct and accessible

### Issue 4: Static Files Not Loading
**Solution**: Ensure `STATIC_ROOT` and `MEDIA_ROOT` are set to `/tmp/`

## 📊 Monitoring

### 1. Vercel Logs
- Go to **Functions** → **Logs**
- Check for any runtime errors

### 2. Django Admin
- Access at: `https://your-app.vercel.app/admin/`
- Create superuser locally first if needed

### 3. Database
- Monitor PostgreSQL performance
- Set up backups

## 🔒 Security Checklist

- ✅ Change default `SECRET_KEY`
- ✅ Set `DEBUG=False`
- ✅ Configure proper `ALLOWED_HOSTS`
- ✅ Use HTTPS URLs in CORS
- ✅ Set up database connection properly
- ✅ Configure email for notifications
- ✅ Monitor logs regularly

## 📞 Support

If you face any issues:
1. Check Vercel deployment logs
2. Verify all environment variables
3. Test locally with production settings
4. Check this guide for common solutions

---

**🎉 Your Library Seat Booking Backend is now ready for production!**
