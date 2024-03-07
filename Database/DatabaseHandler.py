import sqlite3

# Dictionary for caching query results for each table
users_cache = {}
friends_cache = {}
achievements_cache = {}
stats_cache = {}
games_cache = {}
recently_played_cache = {}
global_achievement_cache = {}
app_details_cache = {}
inventory_cache = {}
groups_cache = {}
level_cache = {}
badges_cache = {}

def execute_query(query, params=None, fetchone=False, cache=None):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check if cache is provided and if the query exists in cache
    if cache and query in cache:
        result = cache[query]
    else:
        # Execute the query
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetchone:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()

        # Add the result to the cache if cache is provided
        if cache:
            cache[query] = result

    conn.commit()
    conn.close()

    return result


def create_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            steamid TEXT PRIMARY KEY,
            communityvisibilitystate INTEGER,
            profilestate INTEGER,
            personaname TEXT,
            commentpermission INTEGER,
            profile_url TEXT,
            avatar TEXT,
            avatar_medium TEXT,
            avatar_full TEXT,
            avatar_hash TEXT,
            last_logoff INTEGER,
            persona_state INTEGER,
            primary_clanid TEXT,
            time_created INTEGER,
            personastateflags INTEGER,
            game_extra_info TEXT,
            game_id TEXT,
            lobby_steamid TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS friends (
            id INTEGER PRIMARY KEY,
            steamid TEXT,
            friend_steamid TEXT,
            friend_username TEXT,
            FOREIGN KEY (steamid) REFERENCES users(steamid)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY,
            steamid TEXT,
            appid INTEGER,
            name TEXT,
            playtime INTEGER DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_achievements (
            id INTEGER PRIMARY KEY,
            steamid TEXT,
            appid INTEGER,
            achievements_data TEXT,
            FOREIGN KEY (steamid) REFERENCES users(steamid)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_stats (
            id INTEGER PRIMARY KEY,
            steamid TEXT,
            appid INTEGER,
            stats_data TEXT,
            FOREIGN KEY (steamid) REFERENCES users(steamid)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_recently_played (
            id INTEGER PRIMARY KEY,
            steamid TEXT,
            appid INTEGER,
            playtime INTEGER,
            FOREIGN KEY (steamid) REFERENCES users(steamid)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_global_achievement (
            id INTEGER PRIMARY KEY,
            appid INTEGER,
            achievement_percentage REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS app_details (
            id INTEGER PRIMARY KEY,
            appid INTEGER,
            app_details_data TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_inventory (
            id INTEGER PRIMARY KEY,
            steamid TEXT,
            inventory_data TEXT,
            FOREIGN KEY (steamid) REFERENCES users(steamid)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            steamid TEXT NOT NULL,
            group_id TEXT NOT NULL,
            group_name TEXT NOT NULL,
            group_url TEXT NOT NULL,
            group_avatar TEXT,
            group_description TEXT,
            group_member_count INTEGER,
            group_visibility TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_level (
            id INTEGER PRIMARY KEY,
            steamid TEXT,
            level INTEGER,
            FOREIGN KEY (steamid) REFERENCES users(steamid)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_badges (
            id INTEGER PRIMARY KEY,
            steamid TEXT,
            badges_data TEXT,
            FOREIGN KEY (steamid) REFERENCES users(steamid)
        )
    ''')

    conn.commit()
    conn.close()


def execute_query(query, params=None, fetchone=False, cache=None):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check if cache is provided and if the query exists in cache
    if cache and query in cache:
        result = cache[query]
    else:
        # Execute the query
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetchone:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()

        # Add the result to the cache if cache is provided
        if cache:
            cache[query] = result

    conn.commit()
    conn.close()

    return result

def insert_friend_list(steamid, friends):
    query = 'SELECT COUNT(*) FROM friends WHERE steamid = ?'
    existing_friends_count = execute_query(query, (steamid,), fetchone=True, cache=friends_cache)[0]

    if existing_friends_count == 0:
        for friend in friends:
            query = 'INSERT INTO friends (steamid, friend_steamid, friend_username) VALUES (?, ?, ?)'
            execute_query(query, (steamid, friend['steamid'], friend['personaname']))


def insert_user_summary(user_summary):
    steamid = user_summary['steamid']
    
    # Check if the user already exists in the database
    existing_user = fetch_user(steamid)
    if existing_user:
        return  # User already exists, no need to insert again

    # Extract user summary data
    personaname = user_summary['personaname'] if 'personaname' in user_summary else ''
    communityvisibilitystate = user_summary['communityvisibilitystate'] if 'communityvisibilitystate' in user_summary else 0
    profilestate = user_summary['profilestate'] if 'profilestate' in user_summary else 0
    commentpermission = user_summary['commentpermission'] if 'commentpermission' in user_summary else 0
    profile_url = user_summary['profileurl'] if 'profileurl' in user_summary else ''
    avatar = user_summary['avatar'] if 'avatar' in user_summary else ''
    avatar_medium = user_summary['avatarmedium'] if 'avatarmedium' in user_summary else ''
    avatar_full = user_summary['avatarfull'] if 'avatarfull' in user_summary else ''
    avatar_hash = user_summary['avatarhash'] if 'avatarhash' in user_summary else ''
    last_logoff = user_summary['lastlogoff'] if 'lastlogoff' in user_summary else 0
    persona_state = user_summary['personastate'] if 'personastate' in user_summary else 0
    primaryclanid = user_summary['primaryclanid'] if 'primaryclanid' in user_summary else ''
    time_created = user_summary['timecreated'] if 'timecreated' in user_summary else 0
    personastateflags = user_summary['personastateflags'] if 'personastateflags' in user_summary else 0
    game_extra_info = user_summary['gameextrainfo'] if 'gameextrainfo' in user_summary else ''
    game_id = user_summary['gameid'] if 'gameid' in user_summary else ''
    lobby_steamid = user_summary['lobbysteamid'] if 'lobbysteamid' in user_summary else ''

    # Insert user summary data into the database
    query = '''
        INSERT INTO users (
            steamid, 
            personaname, 
            communityvisibilitystate, 
            profilestate, 
            commentpermission, 
            profile_url, 
            avatar, 
            avatar_medium, 
            avatar_full, 
            avatar_hash, 
            last_logoff, 
            persona_state, 
            primary_clanid, 
            time_created, 
            personastateflags, 
            game_extra_info, 
            game_id, 
            lobby_steamid
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    execute_query(query, (
    steamid,
    personaname,
    communityvisibilitystate,
    profilestate,
    commentpermission,
    profile_url,
    avatar,
    avatar_medium,
    avatar_full,
    avatar_hash,
    last_logoff,
    persona_state,
    primaryclanid,
    time_created,
    personastateflags,
    game_extra_info,
    game_id,
    lobby_steamid
))
    
def insert_user_owned_games(steamid, games):
    query = 'SELECT COUNT(*) FROM games WHERE steamid = ?'
    existing_games_count = execute_query(query, (steamid,), fetchone=True, cache=games_cache)[0]

    if existing_games_count == 0:
        for game in games:
            query = 'INSERT INTO games (steamid, appid, name, playtime) VALUES (?, ?, ?, ?)'
            execute_query(query, (steamid, game['appid'], game['name'], game.get('playtime_forever', 0)), cache=games_cache)


def insert_user_achievements(steamid, appid, achievements_data):
    query = 'SELECT COUNT(*) FROM user_achievements WHERE steamid = ? AND appid = ?'
    existing_achievements_count = execute_query(query, (steamid, appid), fetchone=True, cache=achievements_cache)[0]

    if existing_achievements_count == 0:
        query = 'INSERT INTO user_achievements (steamid, appid, achievements_data) VALUES (?, ?, ?)'
        execute_query(query, (steamid, appid, achievements_data), cache=achievements_cache)

def insert_user_stats(steamid, appid, stats_data):
    query = 'SELECT COUNT(*) FROM user_stats WHERE steamid = ? AND appid = ?'
    existing_stats_count = execute_query(query, (steamid, appid), fetchone=True, cache=stats_cache)[0]

    if existing_stats_count == 0:
        query = 'INSERT INTO user_stats (steamid, appid, stats_data) VALUES (?, ?, ?)'
        execute_query(query, (steamid, appid, stats_data), cache=stats_cache)

def insert_user_recently_played(steamid, appid, playtime):
    query = 'SELECT COUNT(*) FROM user_recently_played WHERE steamid = ? AND appid = ?'
    existing_recently_played_count = execute_query(query, (steamid, appid), fetchone=True, cache=recently_played_cache)[0]

    if existing_recently_played_count == 0:
        query = 'INSERT INTO user_recently_played (steamid, appid, playtime) VALUES (?, ?, ?)'
        execute_query(query, (steamid, appid, playtime), cache=recently_played_cache)

def insert_game_global_achievement(appid, achievement_percentage):
    query = 'SELECT COUNT(*) FROM game_global_achievement WHERE appid = ?'
    existing_global_achievement_count = execute_query(query, (appid,), fetchone=True, cache=global_achievement_cache)[0]

    if existing_global_achievement_count == 0:
        query = 'INSERT INTO game_global_achievement (appid, achievement_percentage) VALUES (?, ?)'
        execute_query(query, (appid, achievement_percentage), cache=global_achievement_cache)

def insert_app_details(appid, app_details_data):
    query = 'SELECT COUNT(*) FROM app_details WHERE appid = ?'
    existing_app_details_count = execute_query(query, (appid,), fetchone=True, cache=app_details_cache)[0]

    if existing_app_details_count == 0:
        query = 'INSERT INTO app_details (appid, app_details_data) VALUES (?, ?)'
        execute_query(query, (appid, app_details_data), cache=app_details_cache)

def insert_user_inventory(steamid, inventory_data):
    query = 'SELECT COUNT(*) FROM user_inventory WHERE steamid = ?'
    existing_inventory_count = execute_query(query, (steamid,), fetchone=True, cache=inventory_cache)[0]

    if existing_inventory_count == 0:
        query = 'INSERT INTO user_inventory (steamid, inventory_data) VALUES (?, ?)'
        execute_query(query, (steamid, inventory_data), cache=inventory_cache)

def insert_user_groups(steamid, group_data):
    for group_id, group_info in group_data:
        query = 'SELECT COUNT(*) FROM user_groups WHERE steamid = ? AND group_id = ?'
        existing_group_count = execute_query(query, (steamid, group_id), fetchone=True, cache=groups_cache)[0]

        if existing_group_count == 0:
            query = 'INSERT INTO user_groups (steamid, group_id, group_name, group_url, group_avatar, \
                group_description, group_member_count, group_visibility) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
            execute_query(query, (steamid, group_id, group_info['group_name'], group_info['group_url'], \
                group_info['group_avatar'], group_info['group_description'], group_info['group_member_count'], \
                    group_info['group_visibility']), cache=groups_cache)
    

def insert_user_level(steamid, level):
    query = 'SELECT COUNT(*) FROM user_level WHERE steamid = ?'
    existing_level_count = execute_query(query, (steamid,), fetchone=True, cache=level_cache)[0]

    if existing_level_count == 0:
        query = 'INSERT INTO user_level (steamid, level) VALUES (?, ?)'
        execute_query(query, (steamid, level), cache=level_cache)

def insert_user_badges(steamid, badges_data):
    query = 'SELECT COUNT(*) FROM user_badges WHERE steamid = ?'
    existing_badges_count = execute_query(query, (steamid,), fetchone=True, cache=badges_cache)[0]

    if existing_badges_count == 0:
        query = 'INSERT INTO user_badges (steamid, badges_data) VALUES (?, ?)'
        execute_query(query, (steamid, badges_data), cache=badges_cache)
    
def fetch_user(steamid):      
    query = 'SELECT * FROM users WHERE steamid = ?'
    result = execute_query(query, (steamid,), fetchone=True, cache=users_cache)
    return result

# def fetch_existing_user_count(steamid):
#     query = 'SELECT COUNT(*) FROM users WHERE steamid = ?'
#     result = execute_query(query, (steamid,), fetchone=True, cache=users_cache)
#     return result[0] if result else 0

# def fetch_existing_friends_count(steamid):
#     query = 'SELECT COUNT(*) FROM friends WHERE steamid = ?'
#     result = execute_query(query, (steamid,), fetchone=True, cache=friends_cache)
#     return result[0] if result else 0

# def fetch_existing_user_achievements_count(steamid, appid):
#     query = 'SELECT COUNT(*) FROM user_achievements WHERE steamid = ? AND appid = ?'
#     result = execute_query(query, (steamid, appid), fetchone=True, cache=achievements_cache)
#     return result[0] if result else 0

# def fetch_existing_user_stats_count(steamid, appid):
#     query = 'SELECT COUNT(*) FROM user_stats WHERE steamid = ? AND appid = ?'
#     result = execute_query(query, (steamid, appid), fetchone=True, cache=stats_cache)
#     return result[0] if result else 0

# def fetch_existing_game_count(steamid):
#     query = 'SELECT COUNT(*) FROM games WHERE steamid = ?'
#     result = execute_query(query, (steamid,), fetchone=True, cache=games_cache)
#     return result[0] if result else 0

# def fetch_existing_recently_played_count(steamid, appid):
#     query = 'SELECT COUNT(*) FROM user_recently_played WHERE steamid = ? AND appid = ?'
#     result = execute_query(query, (steamid, appid), fetchone=True, cache=recently_played_cache)
#     return result[0] if result else 0

# def fetch_existing_global_achievement_count(appid):
#     query = 'SELECT COUNT(*) FROM game_global_achievement WHERE appid = ?'
#     result = execute_query(query, (appid,), fetchone=True, cache=global_achievement_cache)
#     return result[0] if result else 0

# def fetch_existing_app_details_count(appid):
#     query = 'SELECT COUNT(*) FROM app_details WHERE appid = ?'
#     result = execute_query(query, (appid,), fetchone=True, cache=app_details_cache)
#     return result[0] if result else 0

# def fetch_existing_inventory_count(steamid):
#     query = 'SELECT COUNT(*) FROM user_inventory WHERE steamid = ?'
#     result = execute_query(query, (steamid,), fetchone=True, cache=inventory_cache)
#     return result[0] if result else 0

# def fetch_existing_groups_count(steamid):
#     query = 'SELECT COUNT(*) FROM user_groups WHERE steamid = ?'
#     result = execute_query(query, (steamid,), fetchone=True, cache=groups_cache)
#     return result[0] if result else 0

# def fetch_existing_level_count(steamid):
#     query = 'SELECT COUNT(*) FROM user_level WHERE steamid = ?'
#     result = execute_query(query, (steamid,), fetchone=True, cache=level_cache)
#     return result[0] if result else 0

# def fetch_existing_badges_count(steamid):
#     query = 'SELECT COUNT(*) FROM user_badges WHERE steamid = ?'
#     result = execute_query(query, (steamid,), fetchone=True, cache=badges_cache)
#     return result[0] if result else 0

# def fetch_existing_user_count(steamid):
#     query = 'SELECT COUNT(*) FROM users WHERE steamid = ?'
#     result = execute_query(query, (steamid,), fetchone=True, cache=users_cache)
#     return result[0] if result else 0

# def fetch_existing_game_count(steamid):
#     query = 'SELECT COUNT(*) FROM games WHERE steamid = ?'
#     result = execute_query(query, (steamid,), fetchone=True, cache=games_cache)
#     return result[0] if result else 0