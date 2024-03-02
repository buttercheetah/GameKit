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
if __name__ == '__main__':
    unittest.main()
