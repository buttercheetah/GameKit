import sqlite3

class DatabaseManager:
    def __init__(self, database):
        self.database = database
        self.cache = {
            'user_summaries': {},
            'friends': {},
            'user_games': {},
            'user_achievements': {},
            'user_achieved_achievements': {},
            'recently_played': {},
            'user_groups': {},
            'game_global_achievement': {},
            'user_level': {},
            'user_badges': {},
            'user_inventory': {}
            }

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                steamid TEXT PRIMARY KEY,
                communityvisibilitystate INTEGER,
                profilestate INTEGER,
                personaname TEXT,
                commentpermission INTEGER,
                profileurl TEXT,
                avatar TEXT,
                avatarmedium TEXT,
                avatarfull TEXT,
                avatarhash TEXT,
                lastlogoff INTEGER,
                personastate INTEGER,
                realname TEXT,
                primaryclanid TEXT,
                timecreated INTEGER,
                personastateflags INTEGER,
                gameextrainfo TEXT,
                gameid TEXT,
                lobbysteamid TEXT,
                loccountrycode TEXT,
                locstatecode TEXT,
                loccityid INTEGER
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Friends (
                id INTEGER PRIMARY KEY,
                steamid TEXT,
                friend_steamid TEXT,
                FOREIGN KEY (steamid) REFERENCES users(steamid)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS SteamGroupData (
                groupid INTEGER PRIMARY KEY,
                groupName TEXT,
                groupURL TEXT,
                headline TEXT,
                summary TEXT,
                avatarFull TEXT,
                memberCount INT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS UserGames (
                id INTEGER PRIMARY KEY,
                steamid TEXT,
                appid INTEGER,
                name TEXT,
                playtime_2weeks INTEGER,
                playtime_forever INTEGER,
                img_icon_url TEXT,
                has_community_visible_stats BOOLEAN,
                playtime_windows_forever INTEGER,
                playtime_mac_forever INTEGER,
                playtime_linux_forever INTEGER,
                playtime_deck_forever INTEGER,
                rtime_last_played INTEGER,
                has_leaderboards BOOLEAN,
                content_descriptorids TEXT,
                playtime_disconnected INTEGER,
                FOREIGN KEY (steamid) REFERENCES users(steamid)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS UserGroups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                steamid TEXT,
                groupid TEXT,
                FOREIGN KEY (steamid) REFERENCES users(steamid)
                FOREIGN KEY (groupid) REFERENCES SteamGroupData(groupid)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS UserLevel (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                steamid TEXT,
                player_xp INTEGER,
                player_level INTEGER,
                player_xp_needed_to_level_up INTEGER,
                player_xp_needed_current_level INTEGER,
                FOREIGN KEY (steamid) REFERENCES users(steamid)

            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Badges (
                id INTEGER PRIMARY KEY,
                steamid TEXT,
                badgeid INTEGER,
                level INTEGER,
                completion_time INTEGER,
                xp INTEGER,
                scarcity INTEGER,
                FOREIGN KEY (steamid) REFERENCES users(steamid)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS AchievementPercentages (
                id INTEGER PRIMARY KEY,
                appid INTEGER,
                name TEXT UNIQUE,
                percent REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Achievements (
                id INTEGER PRIMARY KEY,
                steamid TEXT,
                appid INTEGER,
                gameName TEXT,
                apiname TEXT,
                displayName TEXT,
                description TEXT,
                achieved INTEGER,
                unlocktime INTEGER,
                FOREIGN KEY (steamid) REFERENCES users(steamid),
                FOREIGN KEY (apiname) REFERENCES AchievementPercentages(name)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ContactUs (
                id INTEGER PRIMARY KEY,
                steamid TEXT,
                name TEXT,
                subject TEXT,
                info TEXT,
                FOREIGN KEY (steamid) REFERENCES users(steamid)
            )
        ''')
        
        conn.commit()
        conn.close()
       
    def execute_query(self, query, values):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        conn.close()

    def insert_user_summary(self, reponse):
        for data in reponse["response"]["players"]:
            steamid = data['steamid']
            existing_user = self.fetch_user_summaries(steamid)
            if existing_user != []:
                return
            else:
                values = [
                    data['steamid'],
                    data['communityvisibilitystate'] if 'communityvisibilitystate' in data else '',
                    data['profilestate'] if 'profilestate' in data else '',
                    data['personaname'] if 'personaname' in data else '',
                    data['commentpermission'] if 'commentpermission' in data else '',
                    data['profileurl'] if 'profileurl' in data else '',
                    data['avatar'] if 'avatar' in data else '',
                    data['avatarmedium'] if 'avatarmedium' in data else '',
                    data['avatarfull'] if 'avatarfull' in data else '',
                    data['avatarhash'] if 'avatarhash' in data else '',
                    data['lastlogoff'] if 'lastlogoff' in data else '',
                    data['personastate'] if 'personastate' in data else '',
                    data['realname'] if 'realname' in data else '',
                    data['primaryclanid'] if 'primaryclanid' in data else '',
                    data['timecreated'] if 'timecreated' in data else '',
                    data['personastateflags'] if 'personastateflags' in data else '',
                    data['gameextrainfo'] if 'gameextrainfo' in data else '',
                    data['gameid'] if 'gameid' in data else '',
                    data['lobbysteamid'] if 'lobbysteamid' in data else '',
                    data['loccountrycode'] if 'loccountrycode' in data else '',
                    data['locstatecode'] if 'locstatecode' in data else '',
                    data['loccityid'] if 'loccityid' in data else ''
                ]

                # Insert user summary data into the database
                query = '''
                    INSERT INTO Users (
                        steamid,  
                        communityvisibilitystate, 
                        profilestate, 
                        personaname,
                        commentpermission, 
                        profileurl, 
                        avatar, 
                        avatarmedium, 
                        avatarfull, 
                        avatarhash, 
                        lastlogoff, 
                        personastate, 
                        realname,
                        primaryclanid, 
                        timecreated, 
                        personastateflags,
                        gameextrainfo,
                        gameid,
                        lobbysteamid,
                        loccountrycode,
                        locstatecode,
                        loccityid
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
                self.execute_query(query, values)

    def fetch_user_summaries(self, steamid):
        if steamid in self.cache['user_summaries']:
            return self.cache['user_summaries'][steamid]

        query = "SELECT * FROM Users WHERE steamid = ?"
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, (steamid,))
        user = cursor.fetchone()
        conn.close()

        if user:
            user = dict(user)
            user = {column_name: value for column_name, value in user.items() if value != ''}
            self.cache['user_summaries'][steamid] = user
            return user
        else:
            return []
        
    def insert_friend_list(self, steamid, friends):
        existing_friends = self.fetch_friends(steamid)
        if existing_friends != []:
            return
        else:
            query = 'INSERT INTO Friends (steamid, friend_steamid) VALUES (?, ?)'
            for friend in friends:
                self.execute_query(query, (steamid, friend))
    
    def fetch_friends(self, steamid):
        if steamid in self.cache['friends']:
            return self.cache['friends'][steamid]

        query = "SELECT friend_steamid FROM Friends WHERE steamid = ?"
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute(query, (steamid,))
        results = cursor.fetchall()
        conn.close()
        if results:
            friends = [result[0] for result in results]  # Extract friend steamids from the results
            self.cache['friends'][steamid] = friends  # Cache the results
            return friends
        else:
            return []

    def insert_user_owned_games(self, steamid, games):
        existing_games = self.fetch_user_owned_games(steamid)
        if existing_games != []:
            return
        for game in games['games']:
            values = [
                steamid,
                game['appid'],
                game['name'] if 'name' in game else '',
                game['playtime_2weeks'] if 'playtime_2weeks' in game else 0,
                game['playtime_forever'] if 'playtime_forever' in game else 0,
                game['img_icon_url'] if 'img_icon_url' in game else '',
                game['has_community_visible_stats'] if 'has_community_visible_stats' in game else False,
                game['playtime_windows_forever'] if 'playtime_windows_forever' in game else 0,
                game['playtime_mac_forever'] if 'playtime_mac_forever' in game else 0,
                game['playtime_linux_forever'] if 'playtime_linux_forever' in game else 0,
                game['playtime_deck_forever'] if 'playtime_deck_forever' in game else 0, 
                game['rtime_last_played'] if 'rtime_last_played' in game else 0,
                game['has_leaderboards'] if 'has_leaderboards' in game else False,
                ','.join(str(desc) for desc in game['content_descriptorids']) if 'content_descriptorids' in game else '',
                game['playtime_disconnected'] if 'playtime_disconnected' in game else 0
            ]

            query = '''
                INSERT INTO UserGames (
                    steamid,
                    appid,
                    name,
                    playtime_2weeks,
                    playtime_forever,
                    img_icon_url,
                    has_community_visible_stats,
                    playtime_windows_forever,
                    playtime_mac_forever,
                    playtime_linux_forever,
                    playtime_deck_forever,
                    rtime_last_played,
                    has_leaderboards,
                    content_descriptorids,
                    playtime_disconnected
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            self.execute_query(query, values)
                
    def clean_game_query(self,result,steamid):
        games_data = []
        for row in result:
            game = dict(row)
            if game.get('content_descriptorids') == '':
                game.pop('content_descriptorids')
            else:   
                content_descrip = game.get('content_descriptorids')
                integer_list = [int(x) for x in content_descrip.split(',')]
                game.update({'content_descriptorids': integer_list})
            
            if game.get('playtime_2weeks') == 0:
                game.pop('playtime_2weeks')
            
            if game.get('has_community_visible_stats') == 0:
                game.pop('has_community_visible_stats')
            else:
                game.update({'has_community_visible_stats': True})
            
            if game.get('has_leaderboards') == 0:
                game.pop('has_leaderboards')
            else:
                game.update({'has_leaderboards': True})
            
            game.pop('id')
            game.pop('steamid')
            games_data.append(game)
        
        return games_data

    def fetch_user_owned_games(self, steamid):
        if steamid in self.cache['user_games']:
            return self.cache['user_games'][steamid]

        query = "SELECT * FROM UserGames WHERE steamid = ?"
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, (steamid,))
        result = cursor.fetchall()
        conn.close()

        if result:
            data = self.clean_game_query(result,steamid)
            self.cache['user_games'][steamid] = {'game_count': len(data), 'games': data}
            return self.cache['user_games'][steamid]
        else:
            return []
    
    def fetch_specif_game_data(self, steamid, appid):
        query = "SELECT * FROM UserGames WHERE steamid = ? and appid = ?"
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        cursor.execute(query, (steamid,appid))
        result = cursor.fetchall()
        conn.close()

        games_data = []
        if result:
            tmpgamedata = self.clean_game_query(result,steamid)
            tgamedata = {'game_count': len(tmpgamedata), 'games': tmpgamedata}
            gamedata = tgamedata['games'][0]
            gamedata['Achievments'] = self.fetch_user_achieved_achievements(steamid, appid)
            return gamedata
        else:
            return []
    
    def fetch_recently_played_games(self, steamid, count):
        if steamid in self.cache['recently_played']:
            return self.cache['recently_played'][steamid]

        query = "SELECT * FROM UserGames WHERE steamid = ? AND playtime_2weeks != 0 ORDER BY playtime_2weeks DESC"
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, (steamid,))
        result = cursor.fetchall()
        conn.close()

        games_data = []
        if result:
            for i, row in enumerate(result):
                if i >= count or not row:
                    break
                game = dict(row)
                game.pop('playtime_linux_forever')
                game.pop('playtime_deck_forever')
                game.pop('rtime_last_played')
                game.pop('playtime_disconnected')
                game.pop('playtime_mac_forever')
                game.pop('playtime_windows_forever')
                game.pop('has_community_visible_stats')
                game.pop('content_descriptorids')
                game.pop('has_leaderboards')
                game.pop('id')
                game.pop('steamid')
                games_data.append(game)

            self.cache['recently_played'][steamid] = {'total_count': len(games_data), 'games': games_data}
            return self.cache['recently_played'][steamid]
        else:
            return []
        
    def insert_global_achievements(self, appid, achievements):
        existing_achievements = self.fetch_achievement_percentages(appid)
        if existing_achievements != []:
            return
        else:
            for achievement in achievements['achievementpercentages']['achievements']:
                name = achievement['name']
                percent = achievement['percent']
                values = [appid, name, percent]
                query = '''
                    INSERT INTO AchievementPercentages (appid, name, percent)
                    VALUES (?, ?, ?)
                '''
                self.execute_query(query, values)
        
    def fetch_achievement_percentages(self, appid):
        if appid in self.cache['game_global_achievement']:
            return self.cache['game_global_achievement'][appid]
        else:
            query = '''
                SELECT name, percent FROM AchievementPercentages WHERE appid = ?
            '''
            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()
            cursor.execute(query, (appid,))
            results = cursor.fetchall()
            conn.close()
            if results:
                achievements = [{'name': result[0], 'percent': result[1]} for result in results]
                self.cache['game_global_achievement'][appid] = {'achievementpercentages': {'achievements': achievements}}
                return self.cache['game_global_achievement'][appid]
            else:
                return []
        
    def insert_achievements(self, steamid, appid, achievements, schema):
        def search_achievement_by_name(schema_achievements, name):
            found_achievements = []
            for schema_achievement in schema_achievements:
                if name.lower() in schema_achievement["name"].lower():
                    found_achievements.append(schema_achievement)
            return found_achievements

        exisiting_achievemnts = self.fetch_user_achievements(steamid, appid)
        if exisiting_achievemnts != []:
            return
        try:
            gameName = achievements['playerstats']['gameName']
        except:
            print("game name not found!")
            return
        for achievement in achievements['playerstats']['achievements']:
            found_achievements = search_achievement_by_name(schema['game']['availableGameStats']['achievements'], achievement['apiname'])[0]
            values = [
                steamid,
                appid,
                gameName,
                achievement['apiname'],
                found_achievements['displayName'],
                found_achievements['description'] if 'description' in found_achievements else 'Achievement description is hidden',
                achievement['achieved'],
                achievement['unlocktime'],

            ]
            query = '''
                INSERT INTO Achievements (
                    steamid,
                    appid,
                    gameName,
                    apiname,
                    displayName,
                    description,
                    achieved,
                    unlocktime
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''
            self.execute_query(query, values)

    # Groups do not return value in json, so there is no need to follow a specific return format
    def fetch_group(self, groupid):
        query = '''
            SELECT * FROM SteamGroupData WHERE groupid = ?
        '''
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute(query, (groupid,))
        results = cursor.fetchall()
        result = []
        if cursor.description:
            column_names = [desc[0] for desc in cursor.description]

            # Create a list of dictionaries with column names as keys
            for row in results:
                result.append(dict(zip(column_names, row)))
        conn.close()
        return result

    def insert_group(self, groupid, groupName, groupURL, headline, summary, avatarFull, memberCount):
        exisiting_group = self.fetch_group(groupid)
        if exisiting_group != []:
            return
        values = [
            groupid,
            groupName,
            groupURL,
            headline,
            summary,
            avatarFull,
            memberCount
        ]
        query = '''
            INSERT INTO SteamGroupData (
                groupid,
                groupName,
                groupURL,
                headline,
                summary,
                avatarFull,
                memberCount
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        self.execute_query(query, values)
        
    def fetch_user_achievements(self, steamid, appid):
        cache_key = f"achievements_{steamid}_{appid}"
        if cache_key in self.cache['user_achievements']:
            return self.cache['user_achievements'][cache_key]

        query = "SELECT gameName, apiname AS name, description, displayName, achieved, unlocktime \
            FROM Achievements WHERE steamid = ? AND appid = ?"
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, (steamid, appid))
        result = cursor.fetchall()
        conn.close()

        if result:
            achievements = [dict(row) for row in result]
            gameName = achievements[0]['gameName']
            for achievement in achievements:
                achievement.pop('gameName', None)
            achievements = {
                'playerstats': {
                    'steamID': steamid,
                    'gameName': gameName,
                    'achievements': achievements,
                    'success': True
                }
            }
            
            self.cache['user_achievements'][cache_key] = achievements
            return achievements
        else:
            return []
    
    def fetch_user_achieved_achievements(self, steamid, appid):
        cache_key = f"achieved_achievements_{steamid}_{appid}"
        if cache_key in self.cache['user_achieved_achievements']:
            return self.cache['user_achieved_achievements'][cache_key]

        query = "SELECT gameName, apiname AS name, description, displayName, achieved, unlocktime \
            FROM Achievements WHERE steamid = ? AND appid = ? AND achieved = 1"
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, (steamid, appid))
        result = cursor.fetchall()
        conn.close()

        if result:
            achievements = [dict(row) for row in result]
            gameName = achievements[0]['gameName']
            for achievement in achievements:
                achievement.pop('gameName', None)
            achievements = {
                'playerstats': {
                    'steamID': steamid,
                    'gameName': gameName,
                    'achievements': achievements
                }
            }
            self.cache['user_achieved_achievements'][cache_key] = achievements
            return achievements
        else:
            return []
    
    def insert_user_groups(self, steamid, groups):
        existing_group = self.fetch_user_groups(steamid)
        if existing_group != []:
            return
        for group in groups:
            values = [
                steamid,
                group['gid']
            ]
            query = '''
                INSERT INTO UserGroups (
                    steamid,
                    groupid
                ) VALUES (?, ?)
            '''
            self.execute_query(query, values)
        
    def fetch_user_groups(self, steamid):
        if steamid in self.cache['user_groups']:
            return self.cache['user_groups'][steamid]
        
        query = "SELECT groupid FROM UserGroups WHERE steamid = ?"
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute(query, (steamid,))
        results = cursor.fetchall()
        conn.close()
        if results:
            group_ids = [result[0] for result in results]
            groups = {'success': True, 'groups': [{'gid': gid} for gid in group_ids]}
            self.cache['user_groups'][steamid] = groups
            return groups
        else:
            return []
        
    def insert_user_level(self, steamid, data):
        existing_level = self.fetch_user_level(steamid)
        if existing_level != []:
            return

        values = [
            steamid, 
            data['player_xp'] if 'player_xp' in data else 0,
            data['player_level'] if 'player_level' in data else 0,
            data['player_xp_needed_to_level_up'] if 'player_xp_needed_to_level_up' in data else 0,
            data['player_xp_needed_current_level'] if 'player_xp_needed_current_level' in data else 0
            ]
        
        query = '''
                INSERT INTO UserLevel (
                    steamid,
                    player_xp,
                    player_level,
                    player_xp_needed_to_level_up,
                    player_xp_needed_current_level
                ) VALUES (?, ?, ?, ?, ?)
            '''
        self.execute_query(query, values)
        
    def fetch_user_level(self, steamid):
        steamid = int(steamid)
        if steamid in self.cache['user_level']:
            return self.cache['user_level'][steamid]
        
        query = "SELECT player_xp,player_level,player_xp_needed_to_level_up,player_xp_needed_current_level FROM UserLevel WHERE steamid = ?"
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, (steamid,))
        results = cursor.fetchone()
        conn.close()
        if results:
            results = dict(results)
            self.cache['user_level'][steamid] = results
            return self.cache['user_level'][steamid]
        else:
            return []

    def insert_user_badges(self, steamid, data):
        exisiting_badges = self.fetch_user_badges(steamid) 
        if exisiting_badges != []:
            return
        
        for badge in data['badges']:
            badgeid = badge['badgeid']
            level = badge['level']
            completion_time = badge['completion_time']
            xp = badge['xp']
            scarcity = badge['scarcity']
            values = (steamid, badgeid, level, completion_time, xp, scarcity)
            query = '''
                INSERT INTO Badges (steamid, badgeid, level, completion_time, xp, scarcity)
                VALUES (?, ?, ?, ?, ?, ?)
            '''
            self.execute_query(query, values)
            
    def fetch_user_badges(self, steamid):
        if steamid in self.cache['user_badges']:
            return self.cache['user_badges'][steamid]
        
        query = "SELECT * FROM Badges WHERE steamid = ?"
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute(query, (steamid,))
        results = cursor.fetchall()
        query = "SELECT * FROM UserLevel WHERE steamid = ?"
        conn.row_factory = sqlite3.Row
        cursor.execute(query, (steamid,))
        # information represents additional info from user level table to be added to return and cache
        information = cursor.fetchall()
        conn.close()
        badges = []
        if results and information:
            for result in results:
                badge = {
                    'badgeid': result[2],
                    'level': result[3],
                    'completion_time': result[4],
                    'xp': result[5],
                    'scarcity': result[6]
                }
                badges.append(badge)
            info = []
            for player_info in information:
                for xp in player_info:
                    info.append(xp)
            
            user_badges = {'badges': badges, 'player_xp': info[1], 'player_level': info[2], \
                'player_xp_needed_to_level_up': info[3], 'player_xp_needed_current_level': info[4]}
            self.cache['user_badges'][steamid] = user_badges
            return self.cache['user_badges'][steamid]
        else:
            return []
    
    def cache_user_inventory(self, steamid, data):
        self.cache['user_inventory'][steamid] = data
        
    def fetch_user_inventory_cache(self, steamid, appid):
        if appid in self.cache['user_inventory']:
            return self.cache['user_inventory'][steamid]
        else:
            return []
        
    def insert_contact_us(self, steamid, name, subject, info):
        query = ''' 
            INSERT INTO ContactUS (steamid, name, subject, info)
            VALUES (?, ?, ?, ?)
            '''
        values = (steamid, name, subject, info)
        self.execute_query(query, values)
        
    def clear_users_table(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        query = "DELETE FROM Users"
        cursor.execute(query)
        conn.commit()
        conn.close()

    def clear_friends_table(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        query = "DELETE FROM Friends"
        cursor.execute(query)
        conn.commit()
        conn.close()

    def clear_SteamGroupData_table(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        query = "DELETE FROM SteamGroupData"
        cursor.execute(query)
        conn.commit()
        conn.close()
        
    def clear_user_games_table(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        query = "DELETE FROM UserGames"
        cursor.execute(query)
        conn.commit()
        conn.close()

    def clear_user_groups_table(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        query = "DELETE FROM UserGroups"
        cursor.execute(query)
        conn.commit()
        conn.close()

    def clear_user_level_table(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        query = "DELETE FROM UserLevel"
        cursor.execute(query)
        conn.commit()
        conn.close()

    def clear_badges_table(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        query = "DELETE FROM Badges"
        cursor.execute(query)
        conn.commit()
        conn.close()

    def clear_achievement_percentages_table(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        query = "DELETE FROM AchievementPercentages"
        cursor.execute(query)
        conn.commit()
        conn.close()

    def clear_achievements_table(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        query = "DELETE FROM Achievements"
        cursor.execute(query)
        conn.commit()
        conn.close()
    
    def clear_contactUs_table(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        query = "DELETE FROM ContactUs"
        cursor.execute(query)
        conn.commit()
        conn.close()

    def clear_all_tables(self):
        self.clear_users_table()
        self.clear_friends_table()
        self.clear_SteamGroupData_table()
        self.clear_user_games_table()
        self.clear_user_groups_table()
        self.clear_user_level_table()
        self.clear_badges_table()
        self.clear_achievement_percentages_table()
        self.clear_achievements_table()
        self.clear_users_table()
        self.clear_friends_table()
        self.clear_user_games_table()
        self.clear_user_groups_table()
        self.clear_user_level_table()
        self.clear_badges_table()
        self.clear_contactUs_table()
        
    def clear_cache(self):
        print("Clearing Cache")
        for cache_key in self.cache:
            self.cache[cache_key] = {}