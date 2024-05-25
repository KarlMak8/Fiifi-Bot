import discord
import json
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('userdata.db', check_same_thread=False)
cursor = conn.cursor()
# Create the user table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_data (
        user_id TEXT PRIMARY KEY,
        balance INTEGER,
        profession TEXT,
        level INTEGER,
        experience INTEGER,
        promotion_criteria INTEGER,
        promotion_multiplier INTEGER,
        hunger INTEGER,
        in_game INTEGER,
        bag TEXT
    )
''')
conn.commit()

async def alter_database():
    cursor.execute('''
        PRAGMA table_info(user_data)
    ''')
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]

    if 'bag' not in column_names:
        cursor.execute('''
            ALTER TABLE user_data
            ADD COLUMN bag TEXT
        ''')
        conn.commit()
        print("Database altered: Added 'bag' column")

    if 'hunger' not in column_names:
        cursor.execute('''
            ALTER TABLE user_data
            ADD COLUMN hunger INTEGER AFTER column6
        ''')
        conn.commit()
        print("Database altered: Added 'hunger' column")
        
async def load_user_data():
    cursor.execute('SELECT * FROM user_data')
    rows = cursor.fetchall()
    return {str(row[0]): {
        "balance": row[1],
        "profession": row[2],
        "level": row[3],
        "experience": row[4],
        "promotion_criteria": row[5],
        "promotion_multiplier": row[6],
        "hunger": row[7],
        "in_game": bool(row[8]),
        "bag": json.loads(row[9]) if row[9] else []  # Convert the JSON string to a list
    } for row in rows}

async def save_user_data(data):
    cursor.execute('DELETE FROM user_data')
    for user_id, user_data in data.items():
        cursor.execute('INSERT INTO user_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
            user_id,
            user_data["balance"],
            user_data["profession"],
            user_data["level"],
            user_data["experience"],
            user_data["promotion_criteria"],
            user_data["promotion_multiplier"],
            user_data["hunger"],
            int(user_data["in_game"]),
            json.dumps(user_data["bag"])  # Convert the bag list to a JSON string
        ))
    conn.commit()


async def getCustomPrefixes():
    with open('customprefixes.json', 'r') as f:
        return json.load(f)

async def saveCustomPrefixes(data):
    with open('customprefixes.json', 'w') as f:
        json.dump(data, f)

async def prefix(ctx):
    serverPrefix = await getCustomPrefixes[str(ctx.guild.id)]
    serverPrefix = str(serverPrefix)
    return serverPrefix
    
async def open_account(user):
    user_data = await load_user_data()
    if str(user.id) not in user_data:
        user_data[str(user.id)] = {
            "balance": 2500,
            "profession": "Unemployed",
            "level": 1,
            "experience": 0,
            "promotion_criteria": 1000,
            "promotion_multiplier": 1,
            "hunger": 20,
            "in_game": False,
            "bag": {
                "fish": [],
                "food": []
            }
        }
        print(f"New user added: {user.id} {user}")
        await save_user_data(user_data)

# Get prefix
def get_prefix(client, message):
    with open('customprefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

async def progressbar(user):
    user_data = await load_user_data()
    # Calculate progress bar values
    experience = user_data[str(user.id)]['experience']
    max_experience = user_data[str(user.id)]['promotion_criteria']  # Adjust this value based on your leveling system
    
    # Calculate the percentage of experience progress
    progress = min(experience / max_experience, 1.0)
    
    # Construct the progress bar
    bar_length = 6
    filled_length = int(progress * bar_length)
    
    # Define emoji characters for filled and empty parts of the progress bar
    filled_emoji = ":blue_square:"
    empty_emoji = ":white_large_square:"

    if progress == 1.0:
        filled_emoji = "🟨"

    # Construct the progress bar using emojis
    bar = filled_emoji * filled_length + empty_emoji * (bar_length - filled_length)
    return bar, progress
