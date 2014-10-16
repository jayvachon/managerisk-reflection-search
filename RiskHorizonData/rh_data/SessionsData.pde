
class SessionsData {

  Table sessions; // session_uuid, IPv4, datetime, email[blank]

  SessionsData (String table) {
    sessions = loadTable (table);
  }

  public ArrayList<Player> createPlayers () {
    ArrayList<Player> players = new ArrayList<Player>();
    ArrayList<String> ips = getColumn (sessions, 1, false);
    for (int i = 0; i < ips.size (); i ++) {
      String ip = ips.get (i);
      ArrayList<TableRow> playerSessions = getPlayerSessions (ip);
      players.add (new Player (ip, playerSessions));
    }
    return players;
  }

  private ArrayList<TableRow> getPlayerSessions (String ip) {
    ArrayList<TableRow> s = new ArrayList<TableRow>();
    
    for (int i = 0; i < sessions.getRowCount (); i ++) {
      TableRow r = sessions.getRow (i);
      if (r.getString (1).equals (ip)) {
        s.add (r);
      }
    }
    
    return s;
  }
}

