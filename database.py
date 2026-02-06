import aiosqlite

async def init_db():
    async with aiosqlite.connect("users.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, lang TEXT DEFAULT 'ru', balance INTEGER DEFAULT 1000)")
        await db.commit()

async def get_user_data(user_id):
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT lang, balance FROM users WHERE id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            if not row:
                await db.execute("INSERT INTO users (id) VALUES (?)", (user_id,))
                await db.commit()
                return 'ru', 1000
            return row

async def update_lang(user_id, lang):
    async with aiosqlite.connect("users.db") as db:
        await db.execute("UPDATE users SET lang = ? WHERE id = ?", (lang, user_id))
        await db.commit()
      
