
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured")
    return psycopg2.connect(database_url)


def initialize_database():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS chats (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id BIGSERIAL PRIMARY KEY,
                    chat_id TEXT NOT NULL REFERENCES chats(id)
                        ON DELETE CASCADE,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS query_logs (
                    id BIGSERIAL PRIMARY KEY,
                    chat_id TEXT,
                    query TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)


def create_chat(chat_id, title):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO chats (id, title)
                VALUES (%s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (chat_id, title))


def list_chats():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, title
                FROM chats
                ORDER BY updated_at DESC
            """)
            return cur.fetchall()


def load_messages(chat_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT role, content
                FROM messages
                WHERE chat_id = %s
                ORDER BY id
            """, (chat_id,))
            return [
                {"role": role, "content": content}
                for role, content in cur.fetchall()
            ]


def save_message(chat_id, role, content):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO messages (chat_id, role, content)
                VALUES (%s, %s, %s)
            """, (chat_id, role, content))
            cur.execute("""
                UPDATE chats
                SET updated_at = NOW()
                WHERE id = %s
            """, (chat_id,))


def log_query(chat_id, query):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO query_logs (chat_id, query)
                VALUES (%s, %s)
            """, (chat_id, query))
if __name__ == "__main__":
    try:
        initialize_database()
        print("PostgreSQL connection successful!")
    except Exception as e:
        print("Database connection failed:", e)