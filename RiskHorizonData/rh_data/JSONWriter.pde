
class JSONWriter {
  
  JSONObject container;
  Players players;
  
  JSONWriter (Players _players) {
    players = _players;
    
    container = new JSONObject ();
    
    JSONArray jPlayers = createPlayersArray (players.getPlayers ());
    container.setJSONArray ("players", jPlayers);
    saveJSONArray (jPlayers, "data/risk_horizon.json");
  }
  
  private JSONArray createPlayersArray (ArrayList<Player> ps) {
    JSONArray jPlayers = new JSONArray ();
    for (int i = 0; i < ps.size (); i ++) {
      JSONObject jPlayer = createPlayerObject (ps.get (i));
      jPlayers.setJSONObject (i, jPlayer);
    }
    return jPlayers;
  }
  
  private JSONObject createPlayerObject (Player p) {
    JSONObject jPlayer = new JSONObject ();
    jPlayer.setString ("ipv4", p.getIP ());
    
    JSONArray jSessions = createSessionsArray (p);
    jPlayer.setJSONArray ("session", jSessions);
    return jPlayer;
  }
  
  private JSONArray createSessionsArray (Player p) {
    JSONArray jSessions = new JSONArray ();
    ArrayList<Player.Session> sessions = p.getSessions ();
    for (int i = 0; i < sessions.size (); i ++) {
      JSONObject jSession = createSessionObject (sessions.get (i));
      jSessions.setJSONObject (i, jSession);
    }
    return jSessions;
  }
  
  private JSONObject createSessionObject (Player.Session session) {
    JSONObject jSession = new JSONObject ();
    jSession.setString ("uuid", session.getUUID ());
    jSession.setString ("datetime", session.getDateTime ());
    
    JSONArray jLevels = createLevelsArray (session);
    jSession.setJSONArray ("levels", jLevels);
    return jSession;
  }
  
  private JSONArray createLevelsArray (Player.Session session) {
    JSONArray jLevels = new JSONArray ();
    ArrayList<Player.Session.Level> levels = session.getLevels ();
    for (int i = 0; i < levels.size (); i ++) {
      JSONObject jLevel = createLevelObject (levels.get (i));
      jLevels.setJSONObject (i, jLevel);
    }
    return jLevels;
  }
  
  private JSONObject createLevelObject (Player.Session.Level level) {
    JSONObject jLevel = new JSONObject ();
    
    jLevel.setString ("uuid", level.getUUID ());
    jLevel.setInt ("level", level.getLevel ());
    jLevel.setFloat ("development end percent", level.getDevelopmentEndPercent ());
    jLevel.setFloat ("protection end percent", level.getProtectionEndPercent ());
    jLevel.setFloat ("research time", level.getKnowledgeTime ());
    int[] insurances = level.getInsurances (); 
    JSONArray jInsurances = new JSONArray ();
    for (int i = 0; i < insurances.length; i ++) {
      jInsurances.setBoolean (i, insurances[i] == 1);
    }
    jLevel.setJSONArray ("insurances", jInsurances);
    
    JSONArray jGrowers = createGrowersArray (level);
    JSONArray jShocks = createShocksArray (level);
    
    jLevel.setJSONArray ("growers", jGrowers);
    jLevel.setJSONArray ("shocks", jShocks);
    
    return jLevel;
  }
  
  private JSONArray createGrowersArray (Player.Session.Level level) {
    JSONArray jGrowers = new JSONArray ();
    TableRow growers = level.getGrowers ();
    if (growers == null) {
      return jGrowers;
    }
    int columnCount = growers.getColumnCount ();
    for (int i = 2; i < columnCount; i ++) {
      jGrowers.setInt (i - 2, growers.getInt (i));
    }
    return jGrowers;
  }
  
  private JSONArray createShocksArray (Player.Session.Level level) {
    JSONArray jShocks = new JSONArray ();
    ArrayList<TableRow> shocks = level.getShocks ();
    for (int i = 0; i < shocks.size (); i ++) {
      JSONObject jShock = createShockObject (shocks.get (i));
      jShocks.setJSONObject (i, jShock);
    }
    return jShocks;
  }
  
  private JSONObject createShockObject (TableRow shock) {
    JSONObject jShock = new JSONObject ();
    jShock.setString ("uuid", shock.getString (0));
    jShock.setFloat ("probability", shock.getFloat (3));
    jShock.setFloat ("severity", shock.getFloat (4));
    jShock.setFloat ("research", shock.getFloat (5));
    jShock.setFloat ("damage", shock.getFloat (6));
    jShock.setFloat ("multiplier", shock.getFloat (8));
    return jShock;
  }
}
