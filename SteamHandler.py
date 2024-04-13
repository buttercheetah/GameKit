import requests
from urllib.parse import urlencode
import Database.DatabaseHandler as Database
from xml.etree import ElementTree
import xmltodict

class Steam:
    def __init__(self, key):
        self.STEAM_KEY = key
        self.cache = {
            #'user_summeries': {},
            #'user_friend_list': {},
            #'user_achievements_per_game': {},
            #'user_stats_for_game': {},
            #'user_owned_games': {},
            #'user_recently_played': {},
            #'game_global_achievement': {},
            'user_inventory': {}, # will need to be addressed 
            #'user_groups': {},
            #'user_level': {},
            #'user_badges': {} # to be implemented
        }
        self.db_manager = Database.DatabaseManager('db/database.db')
        self.db_manager.create_tables()
    # OpenID
    def get_openid_url(self,web_url):
        steam_openid_url = 'https://steamcommunity.com/openid/login'
        params = {
        'openid.ns': "http://specs.openid.net/auth/2.0",
        'openid.identity': "http://specs.openid.net/auth/2.0/identifier_select",
        'openid.claimed_id': "http://specs.openid.net/auth/2.0/identifier_select",
        'openid.mode': 'checkid_setup',
        'openid.return_to': f'{web_url}/authorize',
        'openid.realm': f'{web_url}'
        }

        query_string = urlencode(params)
        auth_url = steam_openid_url + "?" + query_string
        return(auth_url)

    # User API Calls
    def get_user_summeries(self, steamids):
        result = {}

        # Identify which steamids are not in the cache
        not_cached_steamids = [steamid for steamid in steamids if steamid not in self.db_manager.fetch_user_summaries(steamid)]
        if not_cached_steamids:
            # Make one request for all not cached steamids
            response = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={self.STEAM_KEY}&steamids={','.join(not_cached_steamids)}")
            if response.status_code in range(200,299):
                data = response.json()
                self.db_manager.insert_user_summary(data)
            
        # Retrieve data from cache for all steamids
        for steamid in steamids:
            result[steamid] = self.db_manager.fetch_user(steamid)
        
        return result

    def get_user_friend_list(self, steamid):
        friend_ids = self.db_manager.fetch_friends(steamid)
        if friend_ids == []:
            response = requests.get(f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={self.STEAM_KEY}&steamid={steamid}&relationship=friend")
            if not "friendslist" in response.json():
                #print(response.json(), "Error getting friends data")
                return False
            friend_ids = [i['steamid'] for i in response.json()["friendslist"]["friends"]]
            self.db_manager.insert_friend_list(steamid, friend_ids)
        data = self.get_user_summeries(friend_ids)
        return data

    def get_user_achievements_per_game(self, steamid, appid):
        achievements = self.db_manager.fetch_user_achievements(steamid, appid)
        if achievements == []:
            request_url = f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={appid}&key={self.STEAM_KEY}&steamid={steamid}"
            response = requests.get(request_url)
            if response.status_code not in range(200,299):
                return []
            try:
                data = response.json()  
                schema_request_url = f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={self.STEAM_KEY}&appid={appid}"
                schema_response = requests.get(schema_request_url)
                schemma = schema_response.json()
                self.db_manager.insert_achievements(steamid, appid, data, schemma)
            except KeyError:
                return "Profile is not public"
            achievements = self.db_manager.fetch_user_achievements(steamid, appid)
            return achievements
        
        return achievements

    def get_user_stats_for_game(self, steamid ,appid):
        stats_for_game = self.db_manager.fetch_user_achieved_achievements(steamid, appid)
        stats_for_game = []
        if stats_for_game == []:
            # this api call may no longer be necessary as data is similar to user achievements beside not displaying
            # unlock time, some name changes, and some other information that I can leave out from a fetch call
            response = requests.get(f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={appid}&key={self.STEAM_KEY}&steamid={steamid}")
            if response.status_code not in range(200,299):
                return []
            data = response.json()
            self.get_user_achievements_per_game(steamid, appid) 
            stats_for_game = self.db_manager.fetch_user_achieved_achievements(steamid, appid)
            if data == stats_for_game:
                print("succes stats for game")
            else:
                print("failure stats for game")
        return stats_for_game

    def get_user_owned_games(self, steamid):
        games = self.db_manager.fetch_user_owned_games(steamid)
        if games == []:
            response = requests.get(f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={self.STEAM_KEY}&steamid={steamid}&include_appinfo=true&format=json")
            if response.status_code not in range(200,299):
                return []
            try:
                data = response.json()['response']
                self.db_manager.insert_user_owned_games(steamid, data)
            
            except:
                return "Profile is not public"
            games = self.db_manager.fetch_user_owned_games(steamid)
        return games

    def get_user_recently_played(self, steamid,count):
        recently_played = self.db_manager.fetch_recently_played_games(steamid, count)
        if recently_played == []:
            self.get_user_owned_games(steamid)
            recently_played = self.db_manager.fetch_recently_played_games(steamid, count)
        # api call is no longer need, can retrieve same data from database user games table
        # response = requests.get(f"http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={self.STEAM_KEY}&steamid={steamid}&count={count}&format=json")
        # data = response.json()['response']
        return recently_played

    def get_global_achievement_percentage(self, appid):
        global_percentage = self.db_manager.fetch_achievement_percentages(appid)
        if global_percentage == []:
            response = requests.get(f"http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={appid}&format=json")
            if response.status_code not in range(200,299):
                return []
            data = response.json()
            self.db_manager.insert_global_achievements(appid, data)
            global_percentage = self.db_manager.fetch_achievement_percentages(appid)
            if data == global_percentage:
                print("success global percentage")
            else:
                print("failure global")
        return global_percentage
    
    def resolve_vanity_url(self, vanityurl):
        vanityurl = str(vanityurl).replace("https://steamcommunity.com/id/", "").replace("/", "")
        response = requests.get(f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={self.STEAM_KEY}&vanityurl={vanityurl}")
        if response.status_code not in range(200,299):
                return 0
        return response.json()["response"]

    
    # This function should be removed, there doesnt seem to be documentation on this
    # def get_app_details(self, appids):
    #     result = {}

    #     # Identify which steamids are not in the cache
    #     not_cached_appids = [appid for appid in appids if appid not in self.cache['app_details']]

    #     if not_cached_appids:
    #         # Make one request for all not cached steamids
    #         response = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={self.STEAM_KEY}&steamids={','.join(not_cached_appids)}")
    #         data = response.json()

    #         # Update the cache with the new data
    #         for app in data:
    #                 if app['success']:
    #                     self.cache['app_details'][app['data']["steam_appid"]] = app

    #     # Retrieve data from cache for all steamids
    #     for app in appids:
    #         result[app] = self.cache['app_details'][app]

    #     print(result)
    #     return result

    # Game API Calls
    # Removed caching for app news
    def get_app_news(self, appid,count=3,maxlength=300):
        response = requests.get(f"http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={appid}&count={count}&maxlength={maxlength}&format=json")
        # data = response.json()['response']
        if response.status_code not in range(200,299):
                return []
        data = response.json()['appnews']
        return data

    # This function has some sort of bug
    def get_user_inventory(self, steamid, appid):
        # if appid in self.cache['user_inventory']:
        #     return self.cache['user_inventory'][steamid]
        
        response = requests.get(f"https://steamcommunity.com/inventory/{steamid}/{appid}/2")
        if response.status_code not in range(200,299):
                return []
        data = response.json()
        #data = response.json()['response']
        self.cache['user_inventory'][steamid] = data
        #print(data)
        return data

    def get_user_group_list(self, steamid):
        groups = self.db_manager.fetch_user_groups(steamid)
        if groups == []:
            response = requests.get(f"https://api.steampowered.com/ISteamUser/GetUserGroupList/v1?steamid={steamid}&key={self.STEAM_KEY}")
            if response.status_code not in range(200,299):
                return []
            data = response.json()['response']
            self.db_manager.insert_user_groups(steamid, data['groups'])
            groups = self.db_manager.fetch_user_groups(steamid)
        newgroups = []
        if 'groups' not in groups:
            return []
        for group in groups['groups']:
            if 'gid' in group: 
                newgroups.append(self.get_group_data(group['gid']))
            else:
                newgroups.append(group)
        groups['groups'] = newgroups
        return groups
    

    def get_group_data(self, groupids):
        totalresponse = []
        if type(groupids) != list:
            groupids = [groupids]
        for groupid in groupids:
            #print('obtaining groupdata for', groupid)
            db_result = self.db_manager.fetch_group(groupid)
            if db_result != []:
                totalresponse.append({groupid:db_result})
                continue
            response = requests.get(f"https://steamcommunity.com/gid/{groupid}/memberslistxml/?xml=1")
            if response.status_code not in range(200,299):
                    totalresponse.append({groupid:[]})
            data = xmltodict.parse(response.content)
            groupName = data.get('memberList', {}).get('groupDetails', {}).get('groupName', None)
            groupURL = data.get('memberList', {}).get('groupDetails', {}).get('groupURL', None)
            headline = data.get('memberList', {}).get('groupDetails', {}).get('headline', None)
            summary = data.get('memberList', {}).get('groupDetails', {}).get('summary', None)
            avatarFull = data.get('memberList', {}).get('groupDetails', {}).get('avatarFull', None)
            memberCount = data.get('memberList', {}).get('memberCount', None)

            self.db_manager.insert_group(groupid, groupName=groupName,groupURL=groupURL,headline=headline, summary=summary,avatarFull=avatarFull, memberCount=memberCount)
            db_result = self.db_manager.fetch_group(groupid)
            totalresponse.append({groupid:db_result})
        return totalresponse
    def __link_group_to_user(self, groupid, userids):
        for user in userids:
            self.db_manager.insert_user_groups(user,[{'gid':groupid}])

    def get_number_of_players_in_game(self, appid):
        response = requests.get(f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1?appid={appid}")
        if response.status_code not in range(200,299):
                return []
        data = response.json()['response']
        return data

    def get_user_steam_level(self, steamid):
        level = self.db_manager.fetch_user_level(steamid)
        if level == []:
            self.get_user_badges(steamid)
            level = self.db_manager.fetch_user_level(steamid)
        return level
    
    def get_user_badges(self, steamid):
        user_badges = self.db_manager.fetch_user_badges(steamid)
        if user_badges == []:
            response = requests.get(f"https://api.steampowered.com/IPlayerService/GetBadges/v1?steamid={steamid}&key={self.STEAM_KEY}")
            #print(response.json())
            if response.status_code not in range(200,299):
                return []
            try:
                data = response.json()['response']
                self.db_manager.insert_user_badges(steamid, data)
                self.db_manager.insert_user_level(steamid, data)
            except:
                return "Profile is not public"
            user_badges = self.db_manager.fetch_user_badges(steamid)
        return user_badges

    def clear_cache(self):
        for cache_key in self.cache:
            self.cache[cache_key] = {}
            
            
