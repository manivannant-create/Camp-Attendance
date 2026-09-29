# Deploying the camp attendance dashboard to Render (free tier)

This folder has everything Render needs: `server.py` (serves the page and
proxies the attendance API, avoiding CORS), `teacher_attendance_dashboard.html`
(the dashboard itself), and `render.yaml` (Render's config, so it deploys
with the right settings automatically).

## Steps

1. **Put this folder in a GitHub repo.**
   Create a new repo (public or private) and push these three files
   (`server.py`, `teacher_attendance_dashboard.html`, `render.yaml`) to it.
   Render's free tier deploys from a GitHub repo — there's no drag-and-drop
   option for Python services.

2. **Create the Render service.**
   - Go to https://render.com and sign up (free, no card needed for the free tier).
   - Click **New +** → **Blueprint**, and connect the GitHub repo you just made.
   - Render reads `render.yaml` automatically and sets everything up:
     runtime, start command, free plan. Click **Apply**.
   - If you'd rather set it up by hand instead of using the blueprint:
     **New +** → **Web Service** → pick the repo → Runtime: **Python 3** →
     Build command: leave blank → Start command: `python3 server.py` →
     Instance type: **Free**.

3. **Wait for the first deploy** (a minute or two). Render gives you a URL
   like `https://camp-attendance-dashboard.onrender.com`. Open it — the
   dashboard loads, and **Fetch live data** works immediately, since the
   proxy runs server-side.

## Good to know about Render's free tier

- **Spins down when idle.** After ~15 minutes with no traffic, the service
  sleeps. The next visit takes 30–60 seconds to wake up — the page will
  look like it's not loading for a bit, then it will.
- **750 free instance-hours/month** — plenty for a dashboard a small team
  checks periodically.
- To update the dashboard later, edit the HTML or Python file, push to
  GitHub, and Render redeploys automatically.

## If you don't want to use GitHub

Render's free web services require a Git repo (unlike Netlify's drag-and-drop
for static sites). If you'd rather avoid GitHub entirely, Netlify or Vercel
with a serverless function is the alternative — let me know and I'll set
that up instead.
