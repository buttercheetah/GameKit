import unittest
import sys
import os
# While I am ware that there is a better way of doing this, i simply dont care enough to do it as it would require reformating the entire application.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from SteamHandler import Steam
from unittest.mock import patch, MagicMock, PropertyMock

class test_requests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.bad_request_body = """
        <html>
            <head>
                <title>Bad Request</title>
            </head>
            <body>
                <h1>Bad Request</h1>
                Please verify that all required parameters are being sent
            </body>
        </html>
        """

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
    def test_get_user_summeries_empty(self, mock_get):
        key = "none"
        mock_data = {"response":{"players":[]}}
        mock_response = MagicMock()
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response

        # Initialize your class
        steam = Steam(key)

        # Call the method you want to test with a single steamid
        result = steam.get_user_summeries(["76561198180337238"])
        # Assertions
        self.assertEqual(result, False)  # Check if the steamid is in the result
        # Verify that requests.get was called with the expected URL
        mock_get.assert_called_once_with(
            f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids=76561198180337238"
        )
    @patch('SteamHandler.requests.get')
    def test_get_user_friend_list_valid_data(self, mock_requests_get):
        # Create an instance of the Steam class with the API key 'xxxx'
        steam = Steam('xxxx')

        # Mock the response from the API with valid data
        mock_response = MagicMock()
        mock_response.json.return_value = {'friendslist': {'friends': [{'steamid': 'friend1'}, {'steamid': 'friend2'}]}}
        mock_requests_get.return_value = mock_response

        # Mock the get_user_summeries method to return a predefined result
        steam.get_user_summeries = MagicMock(return_value={'friend1': {...}, 'friend2': {...}})

        # Call the function with a steamid
        result = steam.get_user_friend_list('test_steamid')

        # Assert that the result is the expected data
        expected_result = {'friend1': {...}, 'friend2': {...}}
        self.assertEqual(result, expected_result)

    @patch('SteamHandler.requests.get')
    def test_get_user_friend_list_empty_list(self, mock_requests_get):
        # Create an instance of the Steam class with the API key 'xxxx'
        steam = Steam('xxxx')

        # Mock the response from the API with an empty friends list
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_requests_get.return_value = mock_response

        # Call the function with a steamid
        result = steam.get_user_friend_list('test_steamid')

        # Assert that the result is an empty dictionary
        self.assertEqual(result, False)
    
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
                    {"apiname":"DECKED_OUT_1","achieved":1,"unlocktime":1605822181}],
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
                    {"name":"DECKED_OUT_1","achieved":1}
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
            "game_count":2,
            "games":[
                {"appid":1250,"name":"Killing Floor","playtime_forever":1,"img_icon_url":"d8a2d777cb4c59cf06aa244166db232336520547","has_community_visible_stats":True},
                {"appid":35420,"name":"Killing Floor Mod: Defence Alliance 2","playtime_forever":0,"img_icon_url":"ae7580a60cf77b754c723c72d5e31d530fbe7804","has_community_visible_stats":True},
                ]
            }
        }
        mock_response = MagicMock()
        type(mock_response).status_code = PropertyMock(return_value=200)
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response

        steam = Steam(key)
        result = steam.get_user_owned_games(steamid)
        self.assertEqual(result["game_count"], 2)
        self.assertEqual(result["games"][0]["name"], "Killing Floor")

        mock_get.assert_called_once_with(
            f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={steamid}&include_appinfo=true&format=json"
        )
    @patch('SteamHandler.requests.get')
    def test_user_owned_games_none(self, mock_get):
        key="none"
        steamid="76561198348585939"
        mock_data = self.bad_request_body
        mock_response = MagicMock()
        mock_response.return_value = mock_data
        type(mock_response).status_code = PropertyMock(return_value=400)
        mock_get.return_value = mock_response

        steam = Steam(key)
        result = steam.get_user_owned_games(steamid)
        self.assertIsNone(result)

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
        type(mock_response).status_code = PropertyMock(return_value=200)
        steam = Steam(key)

        result = steam.get_user_recently_played(steamid, count)
        self.assertEqual(result["total_count"], 2)
        mock_get.assert_called_once_with(
            f"http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={key}&steamid={steamid}&count={count}&format=json"
        )
    @patch('SteamHandler.requests.get')
    def test_get_user_recently_played_none(self, mock_get):
        key="none"
        steamid="76561198180337238"
        count="1"
        
        mock_data = self.bad_request_body

        mock_response = MagicMock()
        mock_response.return_value = mock_data
        type(mock_response).status_code = PropertyMock(return_value=400)
        
        steam = Steam(key)

        result = steam.get_user_recently_played(steamid, count)
        self.assertIsNone(result)
        mock_get.assert_called_once_with(
            f"http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={key}&steamid={steamid}&count={count}&format=json"
        )
    @patch('SteamHandler.requests.get')
    def test_get_global_achievement_percentage(self, mock_get):
        key="none"
        appid="1172470"
        mock_data = {
            "achievementpercentages":{
                "achievements":[
                    {"name":"JUMPMASTER_4","percent":49.5},
                    {"name":"TEAM_PLAYER_2","percent":42}
                ]
            }
        }

        mock_response = MagicMock()
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response

        steam = Steam(key)

        result = steam.get_global_achievement_percentage(appid)

        self.assertIsNotNone(result["achievements"])
        mock_get.assert_called_once_with(
            f"http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={appid}&format=json"
        )
    @patch('SteamHandler.requests.get')
    def test_get_global_achievement_percentage_none(self, mock_get):
        key="none"
        appid="1172470"
        mock_data = {}

        mock_response = MagicMock()
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response

        steam = Steam(key)

        result = steam.get_global_achievement_percentage(appid)

        self.assertIsNone(result)
        mock_get.assert_called_once_with(
            f"http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={appid}&format=json"
        )
if __name__ == '__main__':

    unittest.main()
