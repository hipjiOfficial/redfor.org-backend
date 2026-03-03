from fastapi import FastAPI
import psycopg2
import os
from datetime import datetime, timezone
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://redfor.org",
        "https://www.redfor.org",
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/shop")
def get_shop():
    connection_string = os.getenv("DB_CONNECTION_STRING")

    if not connection_string:
        return {"error": "Database connection not configured"}

    conn = psycopg2.connect(connection_string)

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT pc1, pc2, pc3, skin, log_date
                FROM shop_log
                WHERE log_date <= %s
                ORDER BY log_date DESC
                LIMIT 1
            """, (datetime.now(timezone.utc),))

            row = cur.fetchone()

        if not row:
            return {"error": "No shop log found"}

        return {
            "pc1": row[0],
            "pc2": row[1],
            "pc3": row[2],
            "skin": row[3],
            "log_date": row[4].isoformat()
        }

    finally:
        conn.close()
