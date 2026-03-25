# Deployment Guide - Render & CI/CD Pipeline

This guide walks you through deploying the Mechanic Shop API to Render with a complete CI/CD pipeline.

## Prerequisites

- GitHub account with your repository
- Render account (free tier available at [render.com](https://render.com))
- Your code pushed to GitHub

## Part 1: Database Setup on Render

### Step 1: Create PostgreSQL Database

1. Log in to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"PostgreSQL"**
3. Configure your database:
   - **Name**: `mechanic-shop-db` (or your preferred name)
   - **Database**: `mechanic_shop`
   - **User**: (auto-generated)
   - **Region**: Choose closest to your location
   - **PostgreSQL Version**: 16 (or latest)
   - **Plan**: Free (or paid for production)
4. Click **"Create Database"**
5. **Important**: Save the **Internal Database URL** (starts with `postgresql://`)
   - You'll find this in the database's "Info" section
   - Example: `postgresql://user:pass@hostname/database`

## Part 2: Deploy Web Service on Render

### Step 2: Create Web Service

1. From Render Dashboard, click **"New +"** → **"Web Service"**
2. Connect your GitHub repository:
   - Click **"Connect a repository"**
   - Authorize Render to access your GitHub
   - Select your `Mechanic-Shop` repository
3. Configure the service:
   - **Name**: `mechanic-shop-api` (or your preferred name)
   - **Region**: Same as your database
   - **Branch**: `main`
   - **Root Directory**: (leave blank)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT flask_app:app`
   - **Plan**: Free (or paid for production)

### Step 3: Add Environment Variables

In the **Environment Variables** section of your web service, add:

| Key            | Value                                                     |
| -------------- | --------------------------------------------------------- |
| `FLASK_ENV`    | `production`                                              |
| `DATABASE_URI` | (Paste your PostgreSQL Internal Database URL from Step 1) |
| `SECRET_KEY`   | (Generate a secure key - see below)                       |
| `BASE_URL`     | (Your Render app URL without `https://`)                  |

**To generate a secure SECRET_KEY:**

```python
python -c "import secrets; print(secrets.token_hex(32))"
```

**For BASE_URL:**

- After creating the service, Render will give you a URL like: `https://mechanic-shop-api-xyz.onrender.com`
- Set `BASE_URL` to: `mechanic-shop-api-xyz.onrender.com` (without https://)

4. Click **"Create Web Service"**

### Step 4: Wait for Deployment

- Render will automatically build and deploy your application
- First deployment takes 5-10 minutes
- Check the logs for any errors
- Once complete, your API will be live at your Render URL!

## Part 3: Set Up CI/CD Pipeline

### Step 5: Get Render API Credentials

1. Go to Render Dashboard → **Account Settings**
2. Scroll to **API Keys**
3. Click **"Create API Key"**
4. Copy the key (you won't see it again!)
5. Go to your web service page
6. Copy the **Service ID** from the URL:
   - URL format: `https://dashboard.render.com/web/srv-XXXXXXXXXXXXX`
   - Service ID is the `srv-XXXXXXXXXXXXX` part

### Step 6: Add GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"** and add:

| Name             | Value                                |
| ---------------- | ------------------------------------ |
| `RENDER_API_KEY` | (Your Render API key from Step 5)    |
| `SERVICE_ID`     | (Your Render service ID from Step 5) |

### Step 7: Test CI/CD Pipeline

The pipeline is already configured in `.github/workflows/main.yaml` and will:

1. **Build**: Check Python syntax
2. **Test**: Run all 71 unit tests
3. **Deploy**: Auto-deploy to Render (only on push to main)

**To test it:**

1. Make a small change (like a comment in README.md)
2. Commit and push to main:
   ```bash
   git add .
   git commit -m "Test CI/CD pipeline"
   git push origin main
   ```
3. Go to your GitHub repository → **Actions** tab
4. Watch the workflow run!
5. If all tests pass, deployment will automatically trigger

## Part 4: Verify Deployment

### Step 8: Test Your Live API

1. **Access Swagger UI**:
   - Go to: `https://your-render-url/api-docs/`
   - You should see your API documentation!

2. **Test an endpoint**:

   ```bash
   curl https://your-render-url/customers/
   ```

3. **Create a customer** (test POST):
   ```bash
   curl -X POST https://your-render-url/customers/ \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Test User",
       "email": "test@example.com",
       "phone": "555-1234",
       "address": "123 Test St",
       "password": "test123"
     }'
   ```

## Part 5: Update Swagger Configuration

Your Swagger is already configured to automatically use:

- **https** scheme in production
- **http** scheme in development
- The incoming request host by default
- Your `BASE_URL` environment variable only when you want to override the advertised host explicitly

The configuration in `app/__init__.py` handles this dynamically based on the `FLASK_ENV` setting.

## Troubleshooting

### Database Connection Errors

**Problem**: `DATABASE_URI environment variable must be set`

**Solution**:

- Check that `DATABASE_URI` is set in Render environment variables
- Verify the PostgreSQL URL is correct
- Make sure the database is running

### Import Errors

**Problem**: `ModuleNotFoundError`

**Solution**:

- Check that all dependencies are in `requirements.txt`
- Verify the build command ran successfully
- Check Render build logs

### Tests Failing in CI/CD

**Problem**: Tests pass locally but fail in GitHub Actions

**Solution**:

- Check that test database credentials match in `.github/workflows/main.yaml`
- Ensure all test dependencies are installed
- Review GitHub Actions logs for specific errors

### Deployment Not Triggered

**Problem**: Code pushed but Render doesn't deploy

**Solution**:

- Check GitHub Actions logs - did the test job pass?
- Verify `RENDER_API_KEY` and `SERVICE_ID` secrets are correct
- Ensure the deploy job ran (check Actions tab)

## CI/CD Workflow Explained

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]      # Trigger on push to main
  pull_request:
    branches: [ main ]      # Trigger on PR to main

jobs:
  build:                    # Job 1: Check syntax
    - Checkout code
    - Install Python & dependencies
    - Validate Python files

  test:                     # Job 2: Run tests
    needs: build            # Runs after build succeeds
    - Set up MySQL service
    - Run all 71 unit tests
    - Verify code quality

  deploy:                   # Job 3: Deploy to Render
    needs: test             # Runs after tests pass
    if: github.ref == 'refs/heads/main'  # Only on main branch
    - Trigger Render deployment via API
    - Notify success
```

## Environment Variables Summary

### Local Development (.env)

```
FLASK_ENV=development
DATABASE_URI=mysql+mysqlconnector://root:password@localhost/mechanic_shop
SECRET_KEY=dev-secret-key
```

### Production (Render)

```
FLASK_ENV=production
DATABASE_URI=postgresql://user:pass@host/mechanic_shop
SECRET_KEY=<generated-secure-key>
BASE_URL=your-app.onrender.com
```

### GitHub Actions (Secrets)

```
RENDER_API_KEY=<your-render-api-key>
SERVICE_ID=srv-xxxxxxxxxxxxx
```

## Best Practices

1. **Never commit .env file** - It's in .gitignore for security
2. **Use strong SECRET_KEY** - Generate with `secrets.token_hex(32)`
3. **Monitor Render logs** - Check for errors after deployment
4. **Test locally first** - Always test before pushing to main
5. **Review failed actions** - Fix CI/CD failures before merging

## Useful Commands

### Local Development

```bash
# Run development server
python run.py

# Run tests
python -m unittest discover tests -v

# Generate secret key
python -c "import secrets; print(secrets.token_hex(32))"
```

### Production Management

```bash
# View Render logs
# (Use Render Dashboard → Your Service → Logs)

# Manual deploy
# (Use Render Dashboard → Your Service → Manual Deploy)

# Rollback
# (Use Render Dashboard → Your Service → Events → Rollback)
```

## Next Steps

1. ✅ Database hosted on Render
2. ✅ Web Service deployed
3. ✅ Environment variables configured
4. ✅ CI/CD pipeline active
5. ✅ Swagger documentation live
6. 🎉 **Your API is production-ready!**

## Support Resources

- [Render Documentation](https://render.com/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/latest/deploying/)
- Your API Documentation: `https://your-render-url/api-docs/`

---

**Congratulations!** Your Mechanic Shop API is now deployed with a complete CI/CD pipeline. Every push to main will automatically test and deploy your application! 🚀
