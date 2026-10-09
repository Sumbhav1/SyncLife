# SyncLife

A React (Vite) frontend in `client/` and a Flask + PostgreSQL backend in `backend-py/`.

## Database

Create a PostgreSQL database and load the schema:

```
psql -d <your_db> -f server/schema.sql
```

## Backend

```
cd backend-py
python -m venv venv
source venv/bin/activate        # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

Create `backend-py/.env`:

```
DB_HOST=localhost
DB_NAME=<your_db>
DB_USER=<db_user>
DB_PASSWORD=<db_password>
JWT_SECRET=<long random string>
SPOONACULAR_KEY=<spoonacular api key>
# Optional
CORS_ORIGINS=http://localhost:5173
FLASK_DEBUG=1
```

Run the server with `python app.py` (port 5001) and the tests with `pytest`.

## Frontend

```
cd client
npm install
npm run dev
```

The client talks to `http://localhost:5001` by default; set `VITE_API_URL` in `client/.env` to change it.

## `server/`

An earlier Express version of the backend, kept for reference. It is not used by the client.
`server/schema.sql` is the database schema used by `backend-py`.
