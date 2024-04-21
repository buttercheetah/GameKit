# Steam Web API Flask App

## Overview
This is a capstone project developed for CSC 289, aiming to create a dynamic web application using Python Flask that leverages the Steam API to provide users with comprehensive information about their account, friends, and gaming activity. The project incorporates database caching to enhance performance and scalability, ensuring faster loading times and seamless user experience. Moreover, the application is designed with Docker deployment in mind, facilitating easy setup and management across various platforms.

### Key Features:
**Steam API Integration**: Utilizing Steam API endpoints to fetch real-time data related to games, user profiles, achievements, and more, providing users with up-to-date insights into their gaming activity.

**Python Flask Webserver**: Implementing Flask, a lightweight and versatile web framework, to develop a robust backend for handling user requests, routing, and rendering dynamic content.

**Database Caching**: Employing a database caching mechanism to store frequently accessed data locally, reducing API calls and enhancing the application's responsiveness and performance.
   > the schema can be found in the 'Database' Folder

**Docker Deployment**: Building the application with Docker containers to facilitate seamless deployment, portability, and scalability across different environments, ensuring consistent behavior and easy management.

### Technical Stack:
- Backend Framework: Python Flask
- Database: SQLite
- API Integration: Steam API
- Frontend: HTML, CSS, JavaScript
- Deployment: Docker or standalone


### Future Enhancements:

- Expand user authentication and authorization for a more personalized experience.
- Incorporate additional features such as game recommendations, social features, and user-generated content.
- Explore potential integration with other gaming platforms and APIs for broader functionality.
- Graph Data Visualization

## Prerequisites
- Python 3.x
- Flask
- Steam API key (set as an environment variable named 'STEAM_KEY')

## Installation
1. Docker
      - docker-compose examples provided under 'docker'
      - ```bash
         docker run -e production=false -e STEAM_KEY="xxx" -e WEB_URL="https://domain.com" -p <port to expose>:3000 ghcr.io/buttercheetah/gamekit:latest
         ```
2. Standalone
   1. Clone the repository:
      ```bash
      git clone https://github.com/yourusername/steam-web-api-app.git
      cd steam-web-api-app
      ```

   2. Install dependencies:
      ```bash
      pip install -r requirements.txt
      ```

   3. Set up enviroment variables:
      - Obtain a Steam API key from [Steamworks](https://steamcommunity.com/dev/apikey).
      - Set the API key as an environment variable named 'STEAM_KEY'.
         - Linux
         ```bash
         export STEAM_KEY="xxxx"
         ```
         - Windows
         ```bash
         $env:STEAM_KEY = "xxx"
         ```
      - Set WEB_URL to the url of the webpage as per the following example. Include http or https
         - Linux
         ```bash
         export WEB_URL="https://domain.com"
         ```
         - Windows
         ```bash
         $env:WEB_URL="https://domain.com"
         ```

   4. Run the application:
         - ```bash
            python app.py
            ```

## Project Structure
- Required programing files and other necessities are under root directory. ie. Dockerfile, main application (app.py), and SteamHandler.py 
- All HTML, CSS, and JavaScript files should be placed in the "templates" directory.

## Contribution Guidelines
- **Do not push directly to the main branch.**
- Create a branch for your work
- Commit your changes to your branch.
- Create a pull request (PR) for review.


## Disclaimer
This project is developed as part of the CSC 289 capstone project and is not intended for production use. Use the Steam API responsibly and adhere to their terms of service.
