import unittest
import sys
import os
# While I am ware that there is a better way of doing this, i simply dont care enough to do it as it would require reformating the entire application.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from SteamHandler import Steam
from unittest.mock import patch, MagicMock

class test_requests(unittest.TestCase):
    @patch('SteamHandler.requests.get')
    def test_get_user_summeries(self, mock_get):
        key = "none"
        mock_data = {
            "response": {
                "players": [
                    {
                        "steamid": "76561198180337238",
                        "communityvisibilitystate": 3,
                        "profilestate": 1,
                        "personaname": "buttercheetah",
                        "profileurl": "https://steamcommunity.com/id/buttercheetah/",
                        "avatar": "https://avatars.steamstatic.com/1fa48f3adeb9594213eb5579244b70f7430ff46e.jpg",
                        "avatarmedium": "https://avatars.steamstatic.com/1fa48f3adeb9594213eb5579244b70f7430ff46e_medium.jpg",
                        "avatarfull": "https://avatars.steamstatic.com/1fa48f3adeb9594213eb5579244b70f7430ff46e_full.jpg",
                        "avatarhash": "1fa48f3adeb9594213eb5579244b70f7430ff46e",
                        "lastlogoff": 1707394872,
                        "personastate": 4,
                        "realname": "Noah",
                        "primaryclanid": "103582791460010420",
                        "timecreated": 1424288420,
                        "personastateflags": 0,
                        "loccountrycode": "US",
                        "locstatecode": "NC"
                    }
                ]
            }
        }
        mock_response = MagicMock()
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response

        # Initialize your class
        steam = Steam(key)

        # Call the method you want to test with a single steamid
        result = steam.get_user_summeries(["76561198180337238"])

        # Assertions
        self.assertIn("76561198180337238", result)  # Check if the steamid is in the result
        user_data = result.get("76561198180337238", {})
        self.assertEqual(user_data["personaname"], "buttercheetah")  # Check specific attribute

        # Verify that requests.get was called with the expected URL
        mock_get.assert_called_once_with(
            f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids=76561198180337238"
        )
    
    @patch('SteamHandler.requests.get')
    def test_get_user_friend_list(self, mock_get):
        key = "none"
        mock_data = {
            "friendslist":{
                "friends":[
                    {"steamid":"76561197964773256","relationship":"friend","friend_since":1471561501},
                    {"steamid":"76561197990263870","relationship":"friend","friend_since":1476928133},
                    {"steamid":"76561198272061600","relationship":"friend","friend_since":1554698097},
                    {"steamid":"76561198278434789","relationship":"friend","friend_since":1503944105},
                    {"steamid":"76561198280900990","relationship":"friend","friend_since":1511831680},
                    {"steamid":"76561198306179806","relationship":"friend","friend_since":1482800816},
                    {"steamid":"76561198394501250","relationship":"friend","friend_since":1570815866},
                    {"steamid":"76561198408373202","relationship":"friend","friend_since":1503092464},
                    {"steamid":"76561198419992215","relationship":"friend","friend_since":1698110155},
                    {"steamid":"76561198826680174","relationship":"friend","friend_since":1522419675},
                    {"steamid":"76561198838907887","relationship":"friend","friend_since":1699836616},
                    {"steamid":"76561199206927268","relationship":"friend","friend_since":1698105384},
                    {"steamid":"76561199423499981","relationship":"friend","friend_since":1667158445},
                    {"steamid":"76561199570226247","relationship":"friend","friend_since":1699740840}
                    ]
                }
            }
        mock_response = MagicMock()
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response

        steam = Steam(key)

        with patch.object(steam, 'get_user_summeries') as mock_get_user_summaries:
            mock_data_user_summaries = {
            "response": {
                "players": [
                    {
                        "steamid": "76561198180337238",
                        "communityvisibilitystate": 3,
                        "profilestate": 1,
                        "personaname": "buttercheetah",
                        "profileurl": "https://steamcommunity.com/id/buttercheetah/",
                        "avatar": "https://avatars.steamstatic.com/1fa48f3adeb9594213eb5579244b70f7430ff46e.jpg",
                        "avatarmedium": "https://avatars.steamstatic.com/1fa48f3adeb9594213eb5579244b70f7430ff46e_medium.jpg",
                        "avatarfull": "https://avatars.steamstatic.com/1fa48f3adeb9594213eb5579244b70f7430ff46e_full.jpg",
                        "avatarhash": "1fa48f3adeb9594213eb5579244b70f7430ff46e",
                        "lastlogoff": 1707394872,
                        "personastate": 4,
                        "realname": "Noah",
                        "primaryclanid": "103582791460010420",
                        "timecreated": 1424288420,
                        "personastateflags": 0,
                        "loccountrycode": "US",
                        "locstatecode": "NC"
                    }
                ]
            }
        }
            mock_get_user_summaries.return_value = mock_data_user_summaries

            result = steam.get_user_friend_list("76561198180337238")

        self.assertEqual(len(result.get("friendslist", {}).get("friends", [])), 14)

        mock_get.assert_called_once_with(
            f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={key}&steamid=76561198180337238&relationship=friend"
        )
        mock_get_user_summaries.assert_called_once_with([
        "76561197964773256",
        "76561197990263870",
        "76561198272061600",
        "76561198278434789",
        "76561198280900990",
        "76561198306179806",
        "76561198394501250",
        "76561198408373202",
        "76561198419992215",
        "76561198826680174",
        "76561198838907887",
        "76561199206927268",
        "76561199423499981",
        "76561199570226247"
    ])
    @patch('SteamHandler.requests.get')
    def test_get_user_achievements_per_game(self, mock_get):
        key = "none"
        steamid = "76561198180337238"
        appid = "1172470"

        # Set up mock response
        mock_data = {
            "playerstats":{
                "steamID":"76561198180337238",
                "gameName":"Apex Legends",
                "achievements":[
                    {"apiname":"THE_PLAYER_0","achieved":1,"unlocktime":1605558532},
                    {"apiname":"DECKED_OUT_1","achieved":1,"unlocktime":1605822181},
                    {"apiname":"TEAM_PLAYER_2","achieved":1,"unlocktime":1605560061},
                    {"apiname":"FULLY_KITTED_3","achieved":1,"unlocktime":1605562915},
                    {"apiname":"JUMPMASTER_4","achieved":1,"unlocktime":1605559403},
                    {"apiname":"WELL_ROUNDED_5","achieved":1,"unlocktime":1605559308},
                    {"apiname":"KILL_LEADER_6","achieved":1,"unlocktime":1605563749},
                    {"apiname":"APEX_OFFENSE_7","achieved":1,"unlocktime":1609795225},
                    {"apiname":"APEX_DEFENSE_8","achieved":1,"unlocktime":1605560965},
                    {"apiname":"APEX_SUPPORT_9","achieved":1,"unlocktime":1609959225},
                    {"apiname":"APEX_RECON_10","achieved":1,"unlocktime":1613069923},
                    {"apiname":"APEX_LEGEND_11","achieved":1,"unlocktime":1605560964}],
                    "success":True
                }
            }
        
        mock_response = MagicMock()
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response

        steam = Steam(key)

        result = steam.get_user_achievements_per_game(steamid, appid)

        # Assertions (Checking for game name and steam id)
        self.assertEqual(result["playerstats"]["steamID"], steamid)
        self.assertEqual(result["playerstats"]["gameName"], "Apex Legends")
        self.assertEqual(result["playerstats"]["success"], True)

        mock_get.assert_called_once_with(
            f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={appid}&key={key}&steamid={steamid}"
        )
    @patch('SteamHandler.requests.get')
    def test_get_user_stats(self, mock_get):
        key="none"
        steamid="76561198180337238"
        appid="1172470"

        mock_data = {
            "playerstats":{
                "steamID":"76561198180337238",
                "gameName":"Telstar_APL",
                "achievements":[
                    {"name":"THE_PLAYER_0","achieved":1},
                    {"name":"DECKED_OUT_1","achieved":1},
                    {"name":"TEAM_PLAYER_2","achieved":1},
                    {"name":"FULLY_KITTED_3","achieved":1},
                    {"name":"JUMPMASTER_4","achieved":1},
                    {"name":"WELL_ROUNDED_5","achieved":1},
                    {"name":"KILL_LEADER_6","achieved":1},
                    {"name":"APEX_OFFENSE_7","achieved":1},
                    {"name":"APEX_DEFENSE_8","achieved":1},
                    {"name":"APEX_SUPPORT_9","achieved":1},
                    {"name":"APEX_RECON_10","achieved":1},
                    {"name":"APEX_LEGEND_11","achieved":1}
                    ]
                }
            }
        mock_response = MagicMock()
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response

        steam = Steam(key)

        result = steam.get_user_stats_for_game(steamid, appid)

        # Assertions (Not checking Every achievement)
        self.assertEqual(result["playerstats"]["steamID"], steamid)
        self.assertEqual(result["playerstats"]["gameName"], "Telstar_APL")
        self.assertEqual(result["playerstats"]["achievements"][0]["name"], "THE_PLAYER_0")
        self.assertEqual(result["playerstats"]["achievements"][0]["achieved"], 1)

        mock_get.assert_called_once_with(
            f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={appid}&key={key}&steamid={steamid}"
        )

    @patch('SteamHandler.requests.get')
    def test_user_owned_games(self, mock_get):
        key="none"
        steamid="76561198348585939"
        mock_data = {"response":{
            "game_count":17,
            "games":[
                {"appid":1250,"name":"Killing Floor","playtime_forever":1,"img_icon_url":"d8a2d777cb4c59cf06aa244166db232336520547","has_community_visible_stats":True},
                {"appid":35420,"name":"Killing Floor Mod: Defence Alliance 2","playtime_forever":0,"img_icon_url":"ae7580a60cf77b754c723c72d5e31d530fbe7804","has_community_visible_stats":True},
                {"appid":72850,"name":"The Elder Scrolls V: Skyrim","playtime_forever":294,"img_icon_url":"b9aca8a189abd8d6aaf09047dbb0f57582683e1c","has_community_visible_stats":True,"content_descriptorids":[5]},
                {"appid":271590,"name":"Grand Theft Auto V","playtime_2weeks":5021,"playtime_forever":16021,"img_icon_url":"1e72f87eb927fa1485e68aefaff23c7fd7178251","has_community_visible_stats":True,"content_descriptorids":[5]},
                {"appid":282660,"name":"Easy eSports","playtime_forever":170,"img_icon_url":"38a313d2413d5c679dcf41e169cc4d815765d775"},{"appid":304050,"name":"Trove","playtime_forever":0,"img_icon_url":"76b62601bb6f0551c415697fe92a6653340f4a5e","has_community_visible_stats":True},
                {"appid":291480,"name":"Warface: Clutch","playtime_forever":589,"img_icon_url":"66ef308279871d99ca776d4602bf02a354570368","has_community_visible_stats":True,"content_descriptorids":[2,5]},
                {"appid":730,"name":"Counter-Strike 2","playtime_forever":72014,"img_icon_url":"8dbc71957312bbd3baea65848b545be9eae2a355","has_community_visible_stats":True,"content_descriptorids":[2,5]},
                {"appid":346900,"name":"AdVenture Capitalist","playtime_forever":584,"img_icon_url":"b4dd5ca1582ed52335b31960e05766fd22fa7cc4","has_community_visible_stats":True},
                {"appid":397900,"name":"Business Tour - Online Multiplayer Board Game","playtime_forever":81,"img_icon_url":"b6ce52a576e99f54c5d18f675540b9c3ee70ed47","has_community_visible_stats":True},
                {"appid":431240,"name":"Golf With Your Friends","playtime_forever":5052,"img_icon_url":"c6379c8ec66ac02565f1155bf3821b846164d93c","has_community_visible_stats":True},
                {"appid":591740,"name":"Sniper Fury","playtime_forever":4,"img_icon_url":"4fd67bcc9743993bbca2ad2aad9b4da68f7e6b6d","has_community_visible_stats":True,"content_descriptorids":[2,5]},
                {"appid":218620,"name":"PAYDAY 2","playtime_forever":2130,"img_icon_url":"a6abc0d0c1e79c0b5b0f5c8ab81ce9076a542414","has_community_visible_stats":True},
                {"appid":652980,"name":"Loading Screen Simulator","playtime_forever":94,"img_icon_url":"a05d56896d73128b477f78062b6cfc72f03c30d1","has_community_visible_stats":True},
                {"appid":674940,"name":"Stick Fight: The Game","playtime_forever":683,"img_icon_url":"28bc7ba8952d488e01e7136126cbbc3b42ee443a","has_community_visible_stats":True},
                {"appid":304930,"name":"Unturned","playtime_forever":0,"img_icon_url":"e18009fb628b35953826efe47dc3be556b689f4c","has_community_visible_stats":True},
                {"appid":1170970,"name":"Marbles on Stream","playtime_forever":0,"img_icon_url":"f9af9e6dba742ed3643cb0d9d8c88163ea044f9a","has_community_visible_stats":True}
                ]
            }
        }
        mock_response = MagicMock()
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response

        steam = Steam(key)
        result = steam.get_user_owned_games(steamid)
        self.assertEqual(result["game_count"], 17)
        self.assertEqual(result["games"][0]["name"], "Killing Floor")

        mock_get.assert_called_once_with(
            f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={steamid}&include_appinfo=true&format=json"
        )
    @patch('SteamHandler.requests.get')
    def test_get_user_recently_played(self, mock_get):
        key="none"
        steamid="76561198180337238"
        count="1"
        
        mock_data = {"response":{
            "total_count":2,
            "games":[
                {"appid":553850,"name":"HELLDIVERS™ 2","playtime_2weeks":729,"playtime_forever":729,"img_icon_url":"c3dff088e090f81d6e3d88eabbb67732647c69cf","playtime_windows_forever":729,"playtime_mac_forever":0,"playtime_linux_forever":0}
                ]
            }
        }

        mock_response = MagicMock()
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response
        
        steam = Steam(key)

        result = steam.get_user_recently_played(steamid, count)
        self.assertEqual(result["total_count"], 2)
        mock_get.assert_called_once_with(
            f"http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={key}&steamid={steamid}&count={count}&format=json"
        )
if __name__ == '__main__':
    unittest.main()
