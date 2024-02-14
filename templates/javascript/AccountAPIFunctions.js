function loadFriends(usteamid) {
    const apiUrl = `/api/friends?steamid=${usteamid}`;

    fetch(apiUrl)
    .then(response => {
        if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Iterate over each friend in the response
        document.getElementById("friends_list").innerHTML = `<ul>`
        for (const steamid in data) {
            if (data.hasOwnProperty(steamid)) {
                const friend = data[steamid];
                // Log or display the formatted output (avatar - personaname)
                console.log(`${friend.avatar} - ${friend.personaname}`);
                document.getElementById("friends_list").innerHTML += `<li><img src=${friend.avatar}> - ${friend.personaname}</li>`
            }
        }
        document.getElementById("friends_list").innerHTML += `</ul>`
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
function loadGames(usteamid) {
    const apiUrl = `/api/games?steamid=${usteamid}`;

    fetch(apiUrl)
    .then(response => {
        if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Iterate over each friend in the response
        document.getElementById("games_list").innerHTML = `<ul>`
        for (const gamedata in data['games']) {
            const game = data['games'][gamedata];
            console.log(`http://media.steampowered.com/steamcommunity/public/images/apps/${game.appid}/${game.img_icon_url}.jpg - ${game.name} - ${game.playtime_forever}`);
            document.getElementById("games_list").innerHTML += `<li><img src=http://media.steampowered.com/steamcommunity/public/images/apps/${game.appid}/${game.img_icon_url}.jpg> - ${game.name} - ${game.playtime_forever}</li>`;
        }
        document.getElementById("friends_list").innerHTML += `</ul>`
    })
    .catch(error => {
        console.error('Error:', error);
    });
}