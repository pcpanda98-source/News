# Render Deployment Fix

## Issues Fixed

1. **Fixed render.yaml** - Changed `startCommand` from `news_app:app` to `app:app`
2. **Fixed render_deploy.py** - Corrected import paths to use `news_app.Backend.*`

## Deploy to Render

### Option 1: Push to Git and Redeploy

```bash
git add .
git commit -m "Fix Render deployment - correct import paths"
git push origin main
```

Then in Render dashboard, click "Manual Deploy" → "Clear build cache & deploy"

### Option 2: Manual Deploy via Render Dashboard

1. Go to your Render dashboard
2. Select your web service
3. Click "Manual Deploy"
4. Select "Clear build cache & deploy"

## Environment Variables on Render

Make sure these are set in Render dashboard:

- `NEWS_API_KEY` - Your NewsAPI key (set as secret)
- `FLASK_ENV` - Set to `production`
- `SECRET_KEY` - Random secret key for Flask sessions

## Verify Deployment

After deployment, check:

1. Service logs for any errors
2. Visit your app URL
3. Check that articles and categories load
4. Test the "Read Full Article" and "Share" buttons on Live News page

## Files Changed

- `render.yaml` - Fixed startCommand
- `render_deploy.py` - Fixed import paths
- `live_news.html` - Fixed button functionality

## If Still Getting Errors

Check Render logs:
1. Go to Render dashboard
2. Click on your service
3. Click "Logs" tab
4. Look for Python errors or import errors

Common issues:
- Missing environment variables
- Import path errors (should be fixed now)
- Database initialization errors
