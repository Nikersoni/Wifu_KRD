import os

TOKEN = os.getenv("BOT_TOKEN")
DB_URL = os.getenv("DATABASE_URL")

ADMINS = [123456789]


# ⚠️ Проверки (очень важно)
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN не задан")

if not DB_URL:
    raise ValueError("❌ DATABASE_URL не задан")


# 🔥 Фикс для Railway (asyncpg)
if DB_URL.startswith("postgres://"):
    DB_URL = DB_URL.replace("postgres://", "postgresql+asyncpg://", 1)

if DB_URL.startswith("postgresql://"):
    DB_URL = DB_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
