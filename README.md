[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/d2zEkl7e)
# CS_2024_project

## Description

A client-server application for organizing game schedule and leaderboard for some sport event. There are some players, a game schedule is made by some rules (i plan to make some default scenarios and a possibility to make custom one), a leaderboard is sorted by some other rules (scenarios and a possibility to make custom one) (Game scheduling may depend from previous game results). So, something like challonge.com but with more custom tie-breaks.

## Setup

Describe the steps to set up the environment and run the application. This can be a bash script or docker commands.

```
docker build -t my-application .

docker run -d 8080:8080 my-application

```

## Requirements

Python, SQL, Flask, HTML...

## Features

Describe the main features the application performs.

* Authorization
* Possibility to delegate rights of moderating
* Creating a new event
* Updating results of games
* "On-line" mode -- you may see how would a scoreboard look like if some game ended in some result
* Default scenarios of tournament -- Round Robin, knockout, Group stage and then knockout, Swiss
* Default tie-breaks -- points, number of wins, point difference, ...
* Outputting the results of games, schedule, leaderboard
* Ability to add custom scenarios
* Ability to add custom tie-breaks
* Ability to change rules on the run (but games already played cannot be rescheduled)

## Git

project-shevlopmes

## Success Criteria

Describe the criteria by which the success of the project can be determined
(this will be updated in the future)

* Simple authorization
* Default scenario works
