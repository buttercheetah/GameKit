// Asynchronously loads the user's friends list from the API using their Steam ID
async function loadFriends(usteamid) {
    // Construct the API URL for fetching friends data
    const apiUrl = `/api/friends?steamid=${usteamid}`;

    // Fetch the data from the API endpoint
    fetch(apiUrl)
    .then(response => {
        // Handle HTTP errors
        if (!response.ok) {
            // Display an error message if the response is not okay
            document.getElementById("friends_list").innerHTML = `<p>Private</p>`;
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        // Parse the response as JSON
        return response.json();
    })
    .then(data => {
        // Display the list of friends on the webpage
        document.getElementById("friends_list").innerHTML = `<ul>`;
        let i = 0;
        // Iterate over each friend in the response
        for (const steamid in data) {
            i++;
            if (i === 9) { break; } // Limit the number of displayed friends
            if (data.hasOwnProperty(steamid)) {
                const friend = data[steamid];
                // Display each friend's name with a link to their profile
                document.getElementById("friends_list").innerHTML += `<li><a href='/user/${steamid}'>${friend.personaname}</a></li>`;
            }
        }
        document.getElementById("friends_list").innerHTML += `</ul>`;
    })
    .catch(error => {
        // Handle any errors that occur during the fetch operation
        console.error('Error:', error);
    });
}

// Asynchronously loads the user's groups from the API using their Steam ID
async function loadGroups(usteamid) {
    // Construct the API URL for fetching groups data
    const apiUrl = `/api/groups?steamid=${usteamid}`;

    // Fetch the data from the API endpoint
    fetch(apiUrl)
    .then(response => {
        // Handle HTTP errors
        if (!response.ok) {
            // Display an error message if the response is not okay
            document.getElementById("user_groups").innerHTML = `<p>Private</p>`;
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        // Parse the response as JSON
        return response.json();
    })
    .then(data => {
        // Display the list of groups on the webpage
        document.getElementById("user_groups").innerHTML = `<ul>`;
        let i = 0;
        let done = []; // Track group IDs to avoid duplicates
        // Iterate over each group in the response
        for (const allallgroups in data.Response) {
            i++;
            for (const allgroups in allallgroups) {
                if (i === 10) { break; } // Limit the number of displayed groups
                const groups = data.Response.groups[i];
                for (const group in groups[0]) {
                    const cgroup = groups[0][group][0]
                    if (done.includes(cgroup['groupid'])) {
                        // Skip if the group has already been displayed
                    } else {
                        // Display the group name
                        document.getElementById("user_groups").innerHTML += `<li>${cgroup.groupName}</li>`;
                        done.push(cgroup['groupid']) // Mark the group as displayed
                    }
                }
            }
        }
        document.getElementById("user_groups").innerHTML += `</ul>`;
    })
    .catch(error => {
        // Handle any errors that occur during the fetch operation
        console.error('Error:', error);
    });
}

// Asynchronously loads the user's games library from the API using their Steam ID
async function loadGames(usteamid) {
    // Construct the API URL for fetching games data
    const apiUrl = `/api/games?steamid=${usteamid}`;
    
    // Fetch the data from the API endpoint
    fetch(apiUrl)
    .then(response => {
        // Handle HTTP errors
        if (!response.ok) {
            // Display an error message if the response is not okay
            document.getElementById("friends_list").innerHTML = `<p>Private</p>`;
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        // Parse the response as JSON
        return response.json();
    })
    .then(data => {
        // Sort games alphabetically by name
        data.games.sort((a, b) => a.name.localeCompare(b.name));
        let gamelist = "";
        // Iterate over each game in the response
        for (let i = 0; i < data.games.length; i++) {
            const game = data.games[i];
            // Add a link to select the game and display its name
            gamelist += `<a onclick="selectgame('${game.appid}','${game.name.replace('\'','')}','${usteamid}')">${game.name}</a>`;
        }
        document.getElementById("gamedropdown-list").innerHTML = gamelist;

        // Display the list of games on the webpage
        document.getElementById("games_list").innerHTML = `<ul>`;
        let i = 0;
        for (const gamedata in data['games']) {
            i++;
            if (i == 8) { break; } // Limit the number of displayed games
            const game = data['games'][gamedata];
            // Display each game's name
            document.getElementById("games_list").innerHTML += `<li>${game.name}</li>`;
        }
        document.getElementById("games_list").innerHTML += `</ul>`;

        // Sort games by playtime and display the top 4 most played games
        const sortedGames = data['games'].sort((a, b) => b.playtime_forever - a.playtime_forever);
        document.getElementById("most_played_games").innerHTML = `<ol>`;
        for (let i = 0; i < Math.min(4, sortedGames.length); i++) {
            const game = sortedGames[i];
            document.getElementById("most_played_games").innerHTML += `<li>${Math.floor(game.playtime_forever/60)} hours - ${game.name}</li>`;
        }
        document.getElementById("most_played_games").innerHTML += `</ol>`;

        // Fetch achievements for the top 50 most recently played games
        const topsortedGames = data['games']
        .sort((a, b) => b.rtime_last_played - a.rtime_last_played)
        .slice(0, 50)
        .map(game => game.appid)
        .join(',');

        const apiUrl = `/api/achievments?steamid=${usteamid}&appids=${topsortedGames}`;
        
        fetch(apiUrl)
        .then(response => {
            // Handle HTTP errors
            if (!response.ok) {
                // Display an error message if the response is not okay
                document.getElementById("newest_achievement").innerHTML = `<p>Private</p>`;
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            // Parse the response as JSON
            return response.json();
        })
        .then(data => {
            // Filter only achievements that have been achieved
            const filteredData = data.Response.map(item => {
                if (item.playerstats && item.playerstats.achievements) {
                    const achievements = item.playerstats.achievements.filter(achievement => achievement.achieved === 1);
                    return { playerstats: { achievements: achievements }, ...item.playerstats }
                } else {
                    return item;
                }
            });
            
            // Sorting the achievements by unlocktime in descending order
            responseData = filteredData.flat().filter(data => data.playerstats?.achievements?.length > 0);
            responseData.sort((a, b) => b.playerstats.achievements[0].unlocktime - a.playerstats.achievements[0].unlocktime);

            // Create an ordered list HTML
            let ol = document.createElement('ol');

            // Add achievements to the list
            for (let i = 0; i < Math.min(responseData.length, 5); i++) {
                let achievement = responseData[i].playerstats.achievements[0];
                let gameName = responseData[i].gameName;
                let displayName = achievement.displayName;
                let unlocktime = new Date(achievement.unlocktime * 1000).toLocaleDateString();
            
                let li = document.createElement('li');
                li.textContent = `${gameName} - ${displayName} - ${unlocktime}`;
                ol.appendChild(li);
            }

            // Set the inner HTML of the div with ID "newest_achievement"
            document.getElementById('newest_achievement').innerHTML = '';
            document.getElementById('newest_achievement').appendChild(ol);
        })
        .catch(error => {
            // Handle any errors that occur during the fetch operation
            console.error('Error:', error);
        });
    })
    .catch(error => {
        // Handle any errors that occur during the fetch operation
        console.error('Error:', error);
    });
}

// Toggle visibility of the dropdown menu
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Filter items in the dropdown menu based on user input
function filterFunction() {
    var input, filter, ul, li, a, i;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    div = document.getElementById("myDropdown");
    a = div.getElementsByTagName("a");
    for (i = 0; i < a.length; i++) {
        txtValue = a[i].textContent || a[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            a[i].style.display = "";
        } else {
            a[i].style.display = "none";
        }
    }
}

// Update selected game information
function selectgame(appid,appname,steamid) {
    document.getElementById("GameSelection").innerHTML = appname;
    appidselection = appid;
}

// Load additional data for a selected game
function loaddataforgame(steamid, operation) {
    // Set the databox to a loading statement.
    document.getElementById("DataBoxData").innerHTML  = "<p>Loading...</p>";
    //console.log(appidselection)
    const apiUrl = `/api/game_data?appid=${appidselection}&steamid=${steamid}`;
    fetch(apiUrl)
    .then(response => {
        // Handle HTTP errors
        if (!response.ok) {
            // Display an error message if the response is not okay
            document.getElementById("friends_list").innerHTML = `<p>Private</p>`;
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        // Parse the response as JSON
        return response.json();
    })
    .then(data => {
        let texttoset = "";
        try {
            if (operation == 'Last_Played') {
                let date = new Date(data.rtime_last_played * 1000);
                texttoset = `<p>Last played on ${date}</p>`;
            } else if (operation == 'Achievements') {
                for (let i = 0; i < data.Achievments.playerstats.achievements.length; i++) {
                    texttoset += `<p>${data.Achievments.playerstats.achievements[i]['displayName']} - ${data.Achievments.playerstats.achievements[i]['description']}</p>`;
                }
            } else if (operation == 'Total_Playtime') {
                texttoset = `<p>Total Playtime: ${(data.playtime_forever/60).toFixed(2)} hours</p>`;
            }
        } catch (error) {
            console.error(error);
            texttoset = '<p>No data to display</p>'
        }
        document.getElementById("DataBoxData").innerHTML  = texttoset;
    })
    .catch(error => {
        // Handle any errors that occur during the fetch operation
        console.error('Error:', error);
    });
}

// Global variable to store the selected game's App ID
let appidselection = 0;
