
// Writes the Risk Horizon data to a JSON file

SessionsData sessionsData;
LevelsData levelsData;
GrowersData growersData;
ShocksData shocksData;

Players players;

JSONWriter jsonWriter;

void setup () {   

  levelsData = new LevelsData ("levels.csv");
  growersData = new GrowersData ("growers.csv");
  shocksData = new ShocksData ("shocks.csv");
  sessionsData = new SessionsData ("sessions.csv");
  println ("creating players...");
  players = new Players (sessionsData.createPlayers (), levelsData, growersData, shocksData);
  jsonWriter = new JSONWriter (players);
}

boolean containsString (ArrayList<String> a, String str) {
  for (int i = 0; i < a.size (); i ++) {
    String s = a.get (i);
    if (s.equals (str)) return true;
  }
  return false;
}

ArrayList<String> getColumn (Table t, int column, boolean allowDuplicates) {
  ArrayList<String> s = new ArrayList<String>();
  for (int i = 1; i < t.getRowCount (); i ++) {
    String str = t.getRow (i).getString (column);
    if (!allowDuplicates) {
      if (containsString (s, str)) continue;
    }
    s.add (str);
  }
  return s;
} 

