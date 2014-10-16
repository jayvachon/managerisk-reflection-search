
class Players {
  
  ArrayList<Player> players;
  LevelsData levelsData;
  GrowersData growersData;
  ShocksData shocksData;
  
  Players (ArrayList<Player> _players, LevelsData _levelsData, GrowersData _growersData, ShocksData _shocksData) {
    players = _players;
    levelsData = _levelsData;
    growersData = _growersData;
    shocksData = _shocksData;
    
    println ("adding levels...");
    addLevels ();
    players.get (459).printLevels ();
    
    println ("done");
  }
  
  public void addLevels () {
    int size = players.size ();//round (players.size () / 4);
    for (int i = 0; i < size; i ++) {
      players.get (i).addLevels (levelsData, growersData, shocksData);
      float progress = (float)i / (float)size;
      progress = round (progress * 100.0);
      println (progress + "% " + i + " of " + size); 
    }
  }
  
  public ArrayList<Player> getPlayers () {
    /*ArrayList<Player> p2 = new ArrayList<Player>();
    p2.add (players.get (0));
    p2.add (players.get (1));
    int l = round (players.size () / 4);
    for (int i = 0; i < l; i ++) {
      p2.add (players.get (i));
    }*/
    return players;
  }
}
