# OneCampus TrustPass

A campus digital-identity prototype: password + authenticator-code sign-in, a signed 30-second single-use identity pass, per-service consent with attribute minimization, session management, a hash-chained audit log, account recovery and an admin console.

```text
frontend/   Static site (HTML, CSS, JavaScript)
backend/    Python API (standard library + psycopg for Postgres)
api/        Vercel entry point for the backend
supabase/   SQL that creates the database tables
```

## Host it on Vercel + Supabase

You need a free [Supabase](https://supabase.com) project, a free [Vercel](https://vercel.com) account and this folder in a GitHub repository.

1. **Create the tables.** In Supabase open **SQL Editor**, paste the contents of `supabase/app_store.sql` and run it. Run it once per Supabase project.
2. **Copy the database URL.** In Supabase click **Connect** and copy the **Transaction pooler** connection string (port `6543`). Replace the password placeholder with your database password. URL-encode special characters in the password (`@` becomes `%40`, and so on).
3. **Make a signing key.** Run `python -c "import secrets; print(secrets.token_urlsafe(48))"` and keep the output. Use the same value on every deployment, because changing it invalidates passes that are in flight.
4. **Import the repository in Vercel.** Keep the project root at the repository root and leave the framework preset on **Other**. Do not set a build command.
5. **Add environment variables** (Production and Preview):

   | Name | Value |
   | --- | --- |
   | `DATABASE_URL` | the pooler URL from step 2 |
   | `TRUSTPASS_SIGNING_KEY` | the key from step 3 |

6. **Deploy.** The first request creates the two demo accounts in your database. Open the Vercel URL and sign in.

The API refuses to start on Vercel without both variables, so a missing value shows up as an error rather than as weak security. Never put either value in the code or commit a `.env` file.

## Run it locally (optional)

Python 3.10 or newer, no packages needed:

```bash
python backend/server.py
```

Open <http://localhost:8000>. Data is kept in `backend/data/trustpass.sqlite3`. To use Supabase locally, copy `.env.example` to `.env`, fill in the two values and run `python -m pip install -r requirements.txt`.

## Demo accounts

The sign-in page shows a fresh authenticator code for each account.

| Role | Email | Password |
| --- | --- | --- |
| Student | `aarav.sharma@northfield.edu` | `CampusDemo!26` |
| Security Admin | `admin@northfield.edu` | `CampusAdmin!26` |

Sample student backup codes for the recovery flow: `A7KP-94QX`, `M3DV-18TZ`, `R6WB-52JN`, `H8LC-37PF`.

## Before real people use it

This is a demo. Anyone who opens the public site can see these credentials and the live authenticator codes and sign in, including as the admin. The recovery flow also displays its email code on screen. Use only fictional data until you:

- remove the demo accounts and the demo panel on the sign-in page (`demo` block in `/api/bootstrap`, `backend/server.py`),
- send recovery codes by real email,
- put real accounts behind Supabase Auth or your campus identity provider.

It does not implement OIDC/PKCE, passkeys, a roster import or scannable QR codes. The rotating pass is a signed token checked by the in-app verifier.
