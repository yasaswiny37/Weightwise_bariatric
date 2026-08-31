# WeightWise Bariatric Program — Patient Portal

A Django web app for the WeightWise Bariatric Program. Patients sign up,
log in, and see a dashboard with their program's learning modules
(currently PowerPoint slide decks, with video support already built in
for later).

## What it does

- **Sign up / Log in** — patients create their own account (no dashboard
  access without an account).
- **Dashboard** — only visible after login. Shows the patient's ID,
  overall progress, and a card for each module.
- **6 Modules** — pre-loaded and editable from the admin panel. Each
  module can hold a PowerPoint (`.ppt`/`.pptx`) file today, and a video
  file later — no code changes needed to add video, just upload it.
- **Progress tracking** — each patient's "viewed" / "completed" status
  per module is tracked separately, like a real hospital LMS.
- **Admin panel** — hospital staff log in at `/admin/` to add/edit
  modules, upload slide decks, and see the list of registered patients.

## 1. One-time setup (on the hospital computer/server)

You need **Python 3.10+** installed. Then, from inside this project
folder:

```bash
# Create an isolated environment (recommended)
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install Django
pip install -r requirements.txt

# Create the database and tables (also loads the 6 default modules)
python manage.py migrate

# Create a staff/admin login for whoever manages the modules
python manage.py createsuperuser
```

## 2. Running the site

```bash
python manage.py runserver 0.0.0.0:8000
```

- On the same computer, open: `http://127.0.0.1:8000/`
- From another computer on the **same hospital network**, open:
  `http://<this-computer's-IP-address>:8000/` (find the IP with
  `ipconfig` on Windows or `ifconfig`/`ip a` on Mac/Linux).

Leave this terminal window open while the site is in use — closing it
stops the site. (For a permanent setup that survives reboots, this can
later be deployed with a proper web server like gunicorn/IIS — happy to
help with that step when you're ready.)

## 3. Adding/editing the 6 modules

1. Go to `http://<address>:8000/admin/`
2. Log in with the superuser account created above.
3. Click **Modules** → open one → upload the `.pptx` file under
   "Slide deck", edit the title/description, save.
4. To add video later: same screen, upload the file under "Video" —
   the patient view automatically switches to showing the video
   instead of the slide download link once one is present.
5. To add a 7th+ module later: click **Add Module**, give it the next
   order number, and fill in the fields.

## 4. How the patient side works

1. Patient visits the site → sent to **Login**.
2. New patient clicks **"Create an account to get started"**, fills in
   name/email/username/password/phone/DOB.
3. On successful signup they're logged in immediately and land on the
   **Dashboard**.
4. Dashboard lists all active modules with a status pill (Not
   started / In progress / Completed) and an overall progress bar.
5. Opening a module shows the slide deck (download link) or, once
   uploaded, the video — plus a **"Mark as Complete"** button.

No one can reach `/dashboard/` or any module without logging in first —
Django redirects them to the login page automatically.

## 5. Project structure

```
weightwise_project/   # Django project settings & top-level URLs
accounts/             # Patient signup/login (Patient model extends the built-in User)
modules/              # Module content + per-patient progress tracking
templates/            # All HTML pages (base layout, login, signup, dashboard, module view)
static/                # CSS + the WeightWise logo
media/                 # Uploaded slide decks / videos (created automatically)
```

## 6. Notes on going live in the hospital

- The default database is SQLite (a single `db.sqlite3` file) — fine for
  a single-server setup with a modest number of patients. If usage grows
  or multiple staff need concurrent write access, this can be swapped
  for PostgreSQL/MySQL with a small settings change.
- `DEBUG = True` and `ALLOWED_HOSTS = ['*']` in `settings.py` are set
  for easy internal testing. Before this touches real patient data
  long-term, we should switch `DEBUG` to `False`, lock `ALLOWED_HOSTS`
  down to the actual machine name/IP, and move the `SECRET_KEY` out of
  the source file — standard Django production hardening. Happy to do
  this pass whenever you're ready to go live.
