# Import necessary modules
import requests, os, random, SteamHandler
from json import dumps
from flask import Flask, Response, render_template, redirect, request, send_from_directory
from flask_apscheduler import APScheduler
import traceback

# Initialize Flask app and APScheduler
app = Flask(__name__)
scheduler = APScheduler()

# Initialize SteamHandler and retrieve environment variables
Steam = SteamHandler.Steam(os.environ.get('STEAM_KEY', 'Steam_api_key'))
web_url = os.environ.get('WEB_URL', 'web_url')
production = os.environ.get('PRODUCTION', False)

# Route for default page
@app.route('/')
def default():
    return render_template("Login Page.html", web_url=web_url)

# Route for default page
@app.route('/search')
def searchpage():
    return render_template("Search_Page_Account.html", web_url=web_url)

# Route for authentication with Steam
@app.route("/auth")
def auth_with_steam():
    return render_template("steam_login_redirect.html",redirect_url=Steam.get_openid_url(web_url))

# Route for about page
@app.route("/about")
def about():
    return render_template("About_Us.html")

# Route for contact page
@app.route("/contact")
def contact():
    return render_template("Contact_Us.html")

# Route for authorization
@app.route("/authorize")
def authorize():
    user_id=str(request.args['openid.identity']).replace('https://steamcommunity.com/openid/id/','')
    return render_template("steam_login_receive_redirect.html",redirect_url=f"{web_url}/user/{user_id}",user_id=user_id)

# Route for search functionality
@app.route("/search/")
def search():
    search_query = request.args.get('search')
    search_type = request.args.get('type')
    if str(search_query).isnumeric():
        return redirect(f"{web_url}/user/{search_query}")
    else:
        vanitysearch = Steam.resolve_vanity_url(search_query)
        if vanitysearch['success'] == True:
            return redirect(f"{web_url}/user/{vanitysearch['steamid']}")
        else:
            return Response(404)

# Route for user login
@app.route('/login')
def login():
    return render_template("LoginPage.html")

# Route for user profile
@app.route('/user/<steamid>')
def user(steamid):
    return render_template("User_Page.html", user=Steam.get_user_summeries([steamid])[steamid], userlevel=Steam.get_user_steam_level(steamid), steamid = steamid)

# Route for user's friends list
@app.route('/user/<steamid>/friends')
def friend_list(steamid):
    friends = Steam.get_user_friend_list(steamid)
    if not friends:
        return render_template("examples/friend_list_error_example.html", user=Steam.get_user_summeries([steamid])[steamid])
    friends = list(friends.values())
    return render_template("examples/friend_list_example.html", friends=friends)

# Route for user's games list
@app.route('/user/<steamid>/games')
def game_list(steamid):
    games = Steam.get_user_owned_games(steamid)['games']
    if not games:
        return render_template("examples/game_list_error_example.html", user=Steam.get_user_summeries([steamid])[steamid])
    return render_template("examples/game_list_example.html", games=games)

# Route for retrieving user's friend list via API
@app.route("/api/friends")
def game_api():
    steamid = request.args.get('steamid')
    data = Steam.get_user_friend_list(steamid)
    if data == False:
        return Response(
        "Data is Private",
        status=401,
    )
    else:
        return data

# Route for retrieving user's groups list via API
@app.route("/api/groups")
def groups_api():
    try:
        steamid = request.args.get('steamid')
        response = Steam.get_user_group_list(steamid)
        return {'Response':response}
    except Exception:
        traceback.print_exc()
        return Response(
        "Data is Private",
        status=401,
    )

# Route for retrieving user's achievements via API
@app.route("/api/achievments")
def achievments_api():
    try:
        steamid = request.args.get('steamid')
        appid = request.args.get('appids')
        appids = appid.split(',')
        response = []
        for appid in appids:
            appachievment = Steam.get_user_achievements_per_game(steamid, appid)
            response.append(appachievment)
        return {'Response':response}
    except Exception:
        traceback.print_exc()
        return Response(
        "Data is Private",
        status=401,
    )

# Route for retrieving user's games via API
@app.route("/api/games")
def games_api():
    try:
        steamid = request.args.get('steamid')
        return Steam.get_user_owned_games(steamid)
    except Exception:
        traceback.print_exc()
        return Response(
        "Data is Private",
        status=401,
    )

# Route for retrieving user's game data via API
@app.route("/api/game_data")
def game_data_api():
    try:
        appid = request.args.get('appid')
        steamid = request.args.get('steamid')
        Steam.get_user_achievements_per_game(steamid, appid)
        return Steam.db_manager.fetch_specif_game_data(appid=appid,steamid=steamid)
    except Exception:
        traceback.print_exc()
        return Response(
        "Data is Private",
        status=401,
    )

# Route for serving JavaScript files
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('templates/javascript', path)

# Route for serving CSS files
@app.route('/stylesheets/<path:path>')
def send_stylesheets(path):
    return send_from_directory('templates/stylesheets', path)

# Route for serving image files
@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('templates/images', path)

# Scheduler tasks for cache clearing
@scheduler.task('interval', id='clear_cache', hours=1)
def clear_cache():
    Steam.db_manager.clear_cache()

@scheduler.task('interval', id='clear_users_table', days=7)
def clear_users_table():
    Steam.db_manager.clear_users_table()

@scheduler.task('interval', id='clear_friends_table', days=7)
def clear_friends_table():
    Steam.db_manager.clear_friends_table()

@scheduler.task('interval', id='clear_friends_table', days=7)
def clear_SteamGroupData():
    Steam.db_manager.clear_SteamGroupData()
    
@scheduler.task('interval', id='clear_user_games_table', days=2)
def clear_user_games_table():
    Steam.db_manager.clear_user_games_table()

@scheduler.task('interval', id='clear_user_groups_table', days=7)
def clear_user_groups_table():
    Steam.db_manager.clear_user_groups_table()

@scheduler.task('interval', id='clear_user_level_table', days=7)
def clear_user_level_table():
    Steam.db_manager.clear_user_level_table()

@scheduler.task('interval', id='clear_badges_table', days=7)
def clear_badges_table():
    Steam.db_manager.clear_badges_table()

@scheduler.task('interval', id='clear_achievement_percentages_table', days=1)
def clear_achievement_percentages_table():
    Steam.db_manager.clear_achievement_percentages_table()

@scheduler.task('interval', id='clear_achievements_table', days=1)
def clear_achievements_table():
    Steam.db_manager.clear_achievements_table()

@app.errorhandler(404) 
def not_found(e): 
  return render_template("Error Page.html") 

if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()  
    if production:
        app.run(host="0.0.0.0")
    else: 
        app.run(host="0.0.0.0", port=3000, debug = True)
