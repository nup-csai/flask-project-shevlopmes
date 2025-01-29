[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/d2zEkl7e)
# CS_2024_project

## Description

A client-server application for organizing game schedule and leaderboard for some sport event. There are some players, a game schedule is made by some rules (knockout format) .Game scheduling may depend from previous game results. So, something like challonge.com.

Application will be on https://flask-project-shevlopmes-production.up.railway.app/

## Setup


```
 Build the Docker image
      docker build . --file Dockerfile --tag first-try 
 Run the Docker image
       docker run -p 8080:8080 --name name first-try

```

## Requirements

Python, SQL, Flask, HTML

## Features

Describe the main features the application performs.

* Creating a new event (done automatically when you write new contest_id)
* Updating results of games
* Adding new games manually
* Outputting the results of games, schedule
* "Knockout format" -- the app automatically checks if all the games from one stage have been played so the next stage should be generated

## Git

flask-project-shevlopmes

## Success Criteria

Describe the criteria by which the success of the project can be determined


* Site works well
* Can add new player using "/contests/<contest id>/add"
* Can add new game using "/contests/<contest id>/games/add"
* See all games using "/contests/<contest id>/games"
* Turn on the knockout mode using "/contests/<contest id>/knockout" -- please note that number of players should be a power of 2 and there should be no games
* Update the result of one game using "/contests/<contest id>/games/<game id>"

Please note that both indexations are 1-based.

## Video
[here](https://www.youtube.com/watch?v=hoiXLvEHqEc)
