# Ledgerly Accounting

Ledgerly is a small-business accounting PWA built with Django templates, vanilla CSS/JavaScript, and the Django ORM. It is designed for two roles: Admin and Employee. Employees can record their own income and expenses; Admins can review all records, manage staff, export reports, and inspect the audit trail.

## Local setup

Use Python 3.11+.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The local fallback database is SQLite only for development. Production uses `DATABASE_URL` and PostgreSQL.

## Supabase PostgreSQL

Create a Supabase project and copy its PostgreSQL connection string into `DATABASE_URL`. For the Vercel serverless runtime, use Supabase's Shared Pooler in transaction mode (port 6543), disable psycopg prepared statements (already configured with `prepare_threshold=None`), and keep `sslmode=require`. Use a direct database connection for migrations, backups, and other single-session PostgreSQL tooling. Run `python manage.py migrate` from a controlled deployment environment; never migrate on every request. See Supabase's current [connection guidance](https://supabase.com/docs/guides/database/connecting-to-postgres).

## Vercel

Import the repository, keep the included `vercel.json`, and set `DJANGO_SECRET_KEY`, `DATABASE_URL`, `DEBUG=False`, `ALLOWED_HOSTS`, and `CSRF_TRUSTED_ORIGINS`. Run migrations once against the production database before opening the site. Static files are collected with `python manage.py collectstatic --noinput` during deployment when needed.

## PWA and mobile

The manifest uses standalone display mode and includes 192px and 512px maskable SVG icons. The service worker caches only the safe static shell; authenticated accounting pages are network-first and are not cached. In Chrome on Android, open the deployed HTTPS URL, choose “Install app” or “Add to Home screen,” then launch Ledgerly from the icon. Offline operations are not queued and must not be treated as saved.

## Backups and exports

Admins can export currently filtered, active transactions from Reports → Export CSV. For a full database backup, use Supabase's backup tools or `pg_dump` from a trusted machine, storing the resulting backup outside Vercel's ephemeral filesystem.

## Security notes

Authentication uses Django sessions, CSRF protection, password hashing, backend role checks, soft deletion, and audit logging. Secrets are environment-only. The built-in `/admin/` is for superuser maintenance and is not the employee UI.
