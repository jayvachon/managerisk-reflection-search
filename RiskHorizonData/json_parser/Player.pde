
class Player {
  
  Game[] games;
  JSONArray jLevels;
  JSONObject[] losingLevels;
  
  Player (JSONArray _jLevels) {
    jLevels = _jLevels;
    
    losingLevels = getLosingLevels ();
    int[] levelLostCounts = getLevelLostCounts ();
    int[] levelPlayCounts = getLevelPlayCounts ();
    
    games = new Game[getLosingLevelsCount ()];
    for (int i = 0; i < games.length; i ++) {
      games[i] = new Game (jLevels, losingLevels[i], levelLostCounts, levelPlayCounts);
    }
  }
  
  private int getLosingLevelsCount () {
    if (!sessionHasMultipleGames (jLevels)) return 1;
    int levelsCount = jLevels.size ();
    JSONObject[] losingLevels = new JSONObject[levelsCount];
    int losingLevelsCount = 0;
    for (int i = 0; i < levelsCount; i ++) {
      JSONObject jLevel = jLevels.getJSONObject (i);
      if (!getLevelWon (jLevel)) {
        losingLevels[losingLevelsCount] = jLevel;
        losingLevelsCount ++;
      }
    }
    return losingLevelsCount;
  }
  
  private JSONObject[] getLosingLevels () {
    int levelsCount = jLevels.size ();
    JSONObject[] losingLevels = new JSONObject[levelsCount];
    int losingLevelsCount = 0;
    for (int i = 0; i < levelsCount; i ++) {
      JSONObject jLevel = jLevels.getJSONObject (i);
      if (!getLevelWon (jLevel)) {
        losingLevels[losingLevelsCount] = jLevel;
        losingLevelsCount ++;
      }
    }
    return losingLevels;
  }
  
  private int[] getLevelLostCounts () {
    // Gets the total number of times each level was lost
    int[] levelLostCounts = new int[6];
    for (int i = 0; i < losingLevels.length; i ++) {
      if (losingLevels[i] == null) continue;
      int l = losingLevels[i].getInt ("level") - 1;
      levelLostCounts[l] ++;
    }
    return levelLostCounts;
  }

  private int[] getLevelPlayCounts () {
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
    
    // Compensates for missing data. e.g. if x level 2's were played, but <x level 1's exist, set the number of level 1's played to the number of level 2's played 
    for (int i = 0; i < longestCountLevel; i ++) {
      levelPlayCounts[i] = max (levelPlayCounts[i], longestCount);
    }
    return levelPlayCounts;
  }
}
