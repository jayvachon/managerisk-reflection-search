// Total # of players: 7184
// Total # of games played: 38152
// Average # of games played per person = 5.3
// Total # of games won: 141
// 0.36% of games were won 
//
// Percentage of people who finished these levels (won or lost):
// 1: 92.7%
// 2: 79.2%
// 3: 58.6%
// 4: 37.7%
// 5: 21.1%
// 6: 6.5%
//
// When these levels were played, the % of times they were passed:
// 1: 63.5%
// 2: 50.5%
// 3: 43.7%
// 4: 45.9%
// 5: 30.8%
// 6: 22.1%

JSONArray players;
float[] devGoals;

void setup () {
  devGoals = new float[] {
    0.01231, // Level 1
    0.04324, // Level 2
    0.09629, // Level 3
    0.17406, // Level 4 
    0.27871, // Level 5
    0.41208, // Level 6
    0.57579, 
    0.77131, 
    1.0
  };
  println ("loading JSON file...");
  players = loadJSONArray ("risk_horizon.json");
  println ("JSON loaded...");
  getGames ();
  println ("done");
}

private int getPlayersReachedLevel (int level) {
  // returns the number of players that reached level # "level"
  ArrayList<JSONObject> p = getPlayerObjects ();
  int levelReached = 0;
  for (int i = 0; i < p.size (); i ++) {
    ArrayList<JSONObject> l = getLevelsInPlayerSessions (p.get (i));
    if (levelsHasLevel (l, level)) levelReached ++;
  }
  return levelReached;
}

private boolean levelsHasLevel (ArrayList<JSONObject> levels, int level) {
  // returns true if the level array contains the level # "level"
  for (int i = 0; i < levels.size (); i ++) {
    if (levels.get (i).getInt ("level") == level) return true;
  }
  return false;
}

private ArrayList<JSONObject> getPlayerObjects () {
  // returns all players
  int size = getPlayerCount ();
  ArrayList<JSONObject> p = new ArrayList<JSONObject>();
  for (int i = 0; i < size; i ++) {
    p.add (players.getJSONObject (i));
  }
  return p;
}

private ArrayList<JSONObject> getLevelsInPlayerSessions (JSONObject player) {
  // returns an array of all levels played by a player (regardless of session)
  ArrayList<JSONObject> allLevels = new ArrayList<JSONObject>();
  JSONArray sessions = getSessionsInPlayer (player);
  for (int i = 0; i < sessions.size (); i ++) {
    JSONArray levels = getLevelsInSession (sessions.getJSONObject (i));
    for (int j = 0; j < levels.size (); j ++) {
      allLevels.add (levels.getJSONObject (j));
    }
  }
  return allLevels;
}

private JSONArray getSessionsInPlayer (JSONObject player) {
  return player.getJSONArray ("session");
}

private JSONArray getLevelsInSession (JSONObject session) {
  return session.getJSONArray ("levels");
}

private void getGames () {
  ArrayList<JSONObject> p = getPlayerObjects ();
  for (int i = 0; i < 1/*p.size ()*/; i ++) {
    JSONArray sessions = getSessionsInPlayer (p.get (i));
    for (int j = 0; j < 1/*sessions.size ()*/; j ++) {
      separateLevelsInSession (sessions.getJSONObject (j));
    }
  }
}

private void separateLevelsInSession (JSONObject session) {
  JSONArray jLevels = getLevelsInSession (session);
  Player p = new Player (jLevels);
}

private int XgetPossiblePathsCount (int[] levelPlayCounts, int[] levelLostCounts, int losingLevel) {
  int possiblePathsCount = 1;
  for (int i = 0; i < losingLevel; i ++) {
    if (levelPlayCounts[i] == 0) continue;
    int levelsWon = (levelPlayCounts[i] - levelLostCounts[i]);
    if (levelsWon == 0) continue;
    possiblePathsCount *= levelsWon;
  }
  return possiblePathsCount;
}

private int[] XgetLevelLostCounts (JSONObject[] losingLevels) {
  // Gets the total number of times each level was lost
  int[] levelLostCounts = new int[6];
  for (int i = 0; i < losingLevels.length; i ++) {
    if (losingLevels[i] == null) continue;
    int l = losingLevels[i].getInt ("level") - 1;
    levelLostCounts[l] ++;
  }
  return levelLostCounts;
}

private int[] XgetLevelPlayCounts (JSONArray jLevels) {
  // Gets the total number of times each level was played
  int[] levelPlayCounts = new int[6];
  int longestCount = 0;
  int longestCountLevel = 0;
  for (int i = 0; i < jLevels.size (); i ++) {
    JSONObject jLevel = jLevels.getJSONObject (i);
    int l = jLevel.getInt ("level") - 1;
    levelPlayCounts[l] ++;
    if (longestCount < levelPlayCounts[l]) {
      longestCount += levelPlayCounts[l];
      longestCountLevel = l;
    }
  }
  
  for (int i = 0; i < longestCountLevel; i ++) {
    levelPlayCounts[i] = max (levelPlayCounts[i], longestCount);
  }
  return levelPlayCounts;
}


private boolean getLevelWon (JSONObject jLevel) {
  // returns true if the level was won
  return (jLevel.getFloat ("development end percent") >= devGoals[jLevel.getInt ("level") - 1]);
}

private JSONObject[][] sortLevels (JSONArray jLevels) {
  JSONObject[][] l = new JSONObject[6][jLevels.size ()]; 
  for (int i = 0; i < 6; i ++) {
    int index = 0;
    for (int j = 0; j < jLevels.size (); j ++) {
      JSONObject jLevel = jLevels.getJSONObject (j);
      if (jLevel.getInt ("level") == (i + 1)) {
        l[i][index] = jLevel;
        index ++;
      }
    }
  }
  return l;
}

private boolean sessionHasMultipleGames (JSONArray levels) {
  // if the levels array only have one level 1, then there's only one game
  return (getGameCountInLevels (levels) > 1);
}

private int getGameCountInLevels (JSONArray levels) {
  int gameCount = 0;
  for (int i = 0; i < levels.size (); i ++) {
    JSONObject level = levels.getJSONObject (i);
    if (level.getInt ("level") == 1) {
      gameCount ++;
    }
  }
  return gameCount;
}

private int getPlayerCount () {
  return 7184;
  //return players.size ();
}

private int getTotalPlays () {
  return 38152;
  /*int size = getPlayerCount ();
   int level1Count = 0;
   for (int i = 0; i < size; i ++) {
   JSONObject player = players.getJSONObject (i);
   JSONArray sessions = getSessionsInPlayer (player);
   for (int j = 0; j < sessions.size (); j ++) {
   JSONArray levels = getLevelsInSession (sessions.getJSONObject (j));
   for (int k = 0; k < levels.size (); k ++) {
   JSONObject level = levels.getJSONObject (k);
   if (level.getInt ("level") == 1) level1Count ++;
   }
   }
   }
   return level1Count;*/
}

private int getTotalWins () {
  return 141;
  /*int size = getPlayerCount ();
   int wins = 0;
   float winningDev = devGoals[5];
   for (int i = 0; i < size; i ++) {
   JSONObject player = players.getJSONObject (i);
   JSONArray sessions = getSessionsInPlayer (player);
   for (int j = 0; j < sessions.size (); j ++) {
   JSONArray levels = getLevelsInSession (sessions.getJSONObject (j));
   for (int k = 0; k < levels.size (); k ++) {
   JSONObject level = levels.getJSONObject (k);
   if (level.getInt ("level") == 6) {
   if (level.getFloat ("development end percent") >= winningDev) {
   wins ++;
   }
   }
   }
   }
   }
   return wins;*/
}

private int[] getLevelsPlayed () {
  int size = getPlayerCount ();
  int[] levelsPlayed = new int[6];
  for (int i = 0; i < size; i ++) {
    JSONObject player = players.getJSONObject (i);
    JSONArray sessions = getSessionsInPlayer (player);
    for (int j = 0; j < sessions.size (); j ++) {
      JSONArray levels = getLevelsInSession (sessions.getJSONObject (j));
      for (int k = 0; k < levels.size (); k ++) {
        JSONObject level = levels.getJSONObject (k);
        levelsPlayed[level.getInt ("level") - 1] ++;
      }
    }
  }
  return levelsPlayed;
}

private int[] getLevelsPassed () {
  int size = getPlayerCount ();
  int[] levelsPassed = new int[6];
  for (int i = 0; i < size; i ++) {
    JSONObject player = players.getJSONObject (i);
    JSONArray sessions = getSessionsInPlayer (player);
    for (int j = 0; j < sessions.size (); j ++) {
      JSONArray levels = getLevelsInSession (sessions.getJSONObject (j));
      for (int k = 0; k < levels.size (); k ++) {
        JSONObject level = levels.getJSONObject (k);
        int l = level.getInt ("level") - 1;
        if (level.getFloat ("development end percent") >= devGoals[l]) {
          levelsPassed[l] ++;
        }
      }
    }
  }
  return levelsPassed;
}

private void getPercentPassed () {
  int[] levelsPlayed = getLevelsPlayed ();
  int[] levelsPassed = getLevelsPassed ();
  float[] percentPassed = new float[6];
  for (int i = 0; i < levelsPlayed.length; i ++) {
    percentPassed[i] = (float)levelsPassed[i] / (float)levelsPlayed[i];
    println (percentPassed[i]);
  }
}

