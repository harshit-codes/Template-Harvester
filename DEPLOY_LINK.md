# Streamlit Cloud Deployment

## 🚀 One-Click Deploy

Click this link to deploy directly to Streamlit Cloud:

**[Deploy Template Harvester Dashboard](https://share.streamlit.io/deploy?repository=harshit-codes/Template-Harvester&branch=master&mainModule=dashboard.py)**

Or copy and paste this URL:
```
https://share.streamlit.io/deploy?repository=harshit-codes/Template-Harvester&branch=master&mainModule=dashboard.py
```

---

## If You Get "Access Denied" Error:

### Step 1: Authorize Streamlit on GitHub

1. Go to: **https://github.com/settings/installations**
2. Look for **"Streamlit"** in the list
3. Click **"Configure"**
4. Under **"Repository access"**, choose one:
   - ✅ **All repositories** (recommended)
   - OR select **"Only select repositories"** → Add **"Template-Harvester"**
5. Click **"Save"**

### Step 2: Sign In to Streamlit Cloud

1. Go to: **https://share.streamlit.io/**
2. Click **"Sign out"** if already signed in
3. Click **"Continue with GitHub"**
4. Sign in with: **harshit-codes** account
5. Click **"Authorize Streamlit"** when prompted

### Step 3: Use Direct Deploy Link Again

Click the deploy link above or manually create app with these details:

- **Repository:** `harshit-codes/Template-Harvester`
- **Branch:** `master`
- **Main file:** `dashboard.py`

---

## Expected Result:

After deployment (2-5 minutes), you'll get a public URL like:

```
https://template-harvester.streamlit.app
```

Or:

```
https://harshit-codes-template-harvester-[random].streamlit.app
```

---

## Still Having Issues?

### Alternative: Deploy from Local

You can also use Streamlit CLI to deploy:

```bash
# Install Streamlit CLI
pip install streamlit

# Login to Streamlit Cloud
streamlit login

# Deploy
streamlit deploy dashboard.py
```

This will open a browser window and guide you through the deployment process.

---

## Support

If you continue to have issues:
- **Streamlit Community Forum:** https://discuss.streamlit.io/
- **Streamlit Docs:** https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app
