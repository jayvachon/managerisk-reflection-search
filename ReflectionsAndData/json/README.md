various python scripts grab data from these json files.

* attribute-averages lists the average values across all plays (for example, at the end of level 1, the average protection % was 28%)
* raw-profiles contains profiles for each player, with attributes averaged from each level that the player played
* quintile-profiles contains profiles for each player. it takes the values from raw-profiles and ranks them according to which quintile the value falls into
* files appended with -all contain data for every player in the game. otherwise, the profiles only include players whose ips match game data and reflection data
