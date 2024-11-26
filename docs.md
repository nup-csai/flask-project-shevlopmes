/{contest id}/games (GET) -- see the list of games and results

html page with all games and its results

/{contest id}/games/{game id} (GET) -- see the result of one game

html page with one game result

/{contest id}/games/{game id} (POST) -- change the result of one game

html page with one game result and buttons to change the result, also a button to change the status of the game to "live"

/{contest id}/scoreboard (GET) -- scoreboard of the tournament

html page with the results

/{contest id}/scoreboard/live (GET) -- like scoreboard, but, if some games are running, it assumes that they end immediately

html page with the results

/new-contest (POST) -- creates new contest and returns its id

/{contest id}/settings (POST) -- change settings of a tournament

html page with a lot of buttons

/login ?? -- it would be great to implement some authorization

/logout