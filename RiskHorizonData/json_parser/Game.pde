
class Game {

  ArrayList<LevelPath> possiblePaths;
  JSONArray jLevels;
  JSONObject losingLevel;
  int losingLevelNumber;
  int[] levelLostCounts;
  int[] levelPlayCounts;
  ArrayList<ArrayList<JSONObject>> sorted;

  Game (JSONArray _jLevels, JSONObject _losingLevel, int[] _levelLostCounts, int[] _levelPlayCounts) {
    jLevels = _jLevels;
    losingLevel = _losingLevel;
    losingLevelNumber = losingLevel.getInt ("level") - 1;
    levelLostCounts = _levelLostCounts;
    levelPlayCounts = _levelPlayCounts;

    sorted = sortLevelsByNumber ();
    getPossiblePaths ();
    /*int ppCount = 0;
    for (int i = 0; i < possiblePaths.size (); i ++) {
      if (possiblePaths.get (i).getPossiblePath ()) ppCount ++;
    }
    println (possiblePaths.size () + " ... " + ppCount);*/
  }

  private int getPossiblePathsCount () {
    int possiblePathsCount = 1;
    for (int i = 0; i < losingLevelNumber; i ++) {
      if (levelPlayCounts[i] == 0) continue;
      int levelsWon = (levelPlayCounts[i] - levelLostCounts[i]);
      if (levelsWon == 0) continue;
      possiblePathsCount *= levelsWon;
    }
    return possiblePathsCount;
  }

  private ArrayList<ArrayList<JSONObject>> sortLevelsByNumber () {
    // "Number" means level number (level 1, level 2, etc)
    ArrayList<ArrayList<JSONObject>> numbers = new ArrayList<ArrayList<JSONObject>>();

    // Initialize an ArrayList for each level
    for (int i = 0; i < losingLevelNumber + 1; i ++) {
      ArrayList<JSONObject> l = new ArrayList<JSONObject> ();
      numbers.add (l);
    }

    // Fill each ArrayList based on the level number
    for (int i = 0; i < jLevels.size (); i ++) {
      JSONObject jLevel = jLevels.getJSONObject (i);
      int l = jLevel.getInt ("level") - 1;
      if (!getLevelWon (jLevel) && l < losingLevelNumber) continue;
      if (l > losingLevelNumber) continue;
      numbers.get (l).add (jLevel);
    }

    return numbers;
  }

  private void getPossiblePaths () {
    
    int possiblePathsCount = getPossiblePathsCount ();
    possiblePaths = new ArrayList<LevelPath>(possiblePathsCount);
    int pathsCreated = 0;
    int failsafe = 0;
    
    // For each level number, keep track of our position in the array (so that one level is not added multiple times to the same path)
    int[] positions = new int[losingLevelNumber];
    for (int i = 0; i < positions.length; i ++) {
      positions[i] = 0;
    }
    
    /*while (pathsCreated < possiblePathsCount && failsafe < 1000) {
      
      ArrayList<JSONObject> path = new ArrayList<JSONObject>(losingLevelNumber + 1);
      // Each path begins at the losing level
      path.add (losingLevel);

      int levelNumber = losingLevelNumber - 1;
      
      while (levelNumber > -1) {
        JSONObject l = sorted.get (levelNumber).get (positions[levelNumber]);
        path.add (l);
        positions[levelNumber] ++;
        if (sorted.get (levelNumber).size () < (positions[levelNumber] + 1)) {
          positions[levelNumber] = 0;
        }
        levelNumber --;
      }
      
      possiblePaths.add (new LevelPath (path));
      
      pathsCreated ++;
      failsafe ++;
    }*/
    
    createLevelPath (losingLevelNumber, new ArrayList<JSONObject>());
    
    if (failsafe >= 999) {
      println ("failed");
    }
  }
  
  private void createLevelPath (int levelNumber, ArrayList<JSONObject> path) {
    ArrayList<JSONObject> sortedLevel = sorted.get (levelNumber);
    int sortedLevelSize = sortedLevel.size ();
    
    levelNumber --;
    for (int i = 0; i < sortedLevelSize; i ++) {
      path.add (sortedLevel.get (i));
      if (levelNumber == -1) {
        // Add the completed path if we're at level 1
        possiblePaths.add (new LevelPath (path));
        if (path.size () > 0) path.remove (path.size () - 1);
      } else {
        // Move onto the next level
        createLevelPath (levelNumber, path);
        path.remove (path.size () - 1);
      }
    }    
    /*if (levelNumber == 0) {
      for (int i = 0; i < sortedLevelSize; i ++) {
        path.add (sortedLevel.get (i));
        possiblePaths.add (new LevelPath (path));
        if (path.size () > 0) {
          path.remove (path.size () - 1);
        }  
      }
    } else {
      levelNumber --;
      for (int i = 0; i < sortedLevelSize; i ++) { 
        path.add (sortedLevel.get (i));
        createLevelPath (levelNumber, path);
        path.remove (path.size () - 1);
      }
    }*/
  }
}

