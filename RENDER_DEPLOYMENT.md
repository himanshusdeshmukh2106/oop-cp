# Deploy to Render

This guide will help you deploy the Heart Disease Prediction System to Render.

## Prerequisites
- A GitHub account
- A Render account (sign up at https://render.com)
- Your code pushed to a GitHub repository

## Deployment Steps

### 1. Push Your Code to GitHub
```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### 2. Create a New Web Service on Render
1. Go to https://dashboard.render.com
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Render will auto-detect the `render.yaml` configuration

### 3. Configure Environment Variables
Render will automatically set most variables from `render.yaml`, but you need to set:

- **ALLOWED_HOSTS**: Set this to your Render URL (e.g., `your-app-name.onrender.com`)
  - After deployment, update this in the Render dashboard under Environment

### 4. Deploy
- Click "Create Web Service"
- Render will automatically run the build script and deploy your app
- First deployment takes 5-10 minutes

## Post-Deployment

### Update ALLOWED_HOSTS
After your first deployment:
1. Go to your service in Render dashboard
2. Click "Environment" in the left sidebar
3. Update `ALLOWED_HOSTS` to your actual Render URL
4. Save changes (this will trigger a redeploy)

### Create Superuser (Admin Account)
To access the Django admin panel:
1. Go to your service in Render dashboard
2. Click "Shell" in the left sidebar
3. Run:
```bash
cd Heart-Disease-Prediction-System
python manage.py createsuperuser
```
4. Follow the prompts to create your admin account

## Important Notes

- **Database**: This app uses SQLite, which works for small projects but data will reset on each deployment. For production, consider upgrading to PostgreSQL.
- **Static Files**: Handled by WhiteNoise automatically
- **ML Models**: The trained models in `trained_models/` folder will be included in the deployment
- **Free Tier**: Render's free tier spins down after 15 minutes of inactivity, so first request may be slow

## Troubleshooting

### Build Fails
- Check the build logs in Render dashboard
- Ensure all dependencies are in `requirements.txt`

### App Crashes
- Check the logs in Render dashboard
- Verify `ALLOWED_HOSTS` is set correctly
- Ensure `SECRET_KEY` environment variable is set

### Static Files Not Loading
- Run `python manage.py collectstatic` manually in Render shell
- Check that WhiteNoise middleware is properly configured

## URLs After Deployment
- **Main App**: `https://your-app-name.onrender.com`
- **Admin Panel**: `https://your-app-name.onrender.com/admin`

## Support
For issues specific to Render deployment, check:
- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com
