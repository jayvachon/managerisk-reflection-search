
class Player {

  class Session {
    
    class Level {
      
      TableRow level;
      TableRow growers;
      ArrayList<TableRow> shocks;
      
      Level (TableRow _level, TableRow _growers, ArrayList<TableRow> _shocks) {
        level = _level;
        growers = _growers;
        shocks = _shocks;
      }  
      
      public void printGrowers () {
        println ("got it");
      }
      
      public String getUUID () {
        return level.getString (0);
      }
      
      public int getLevel () {
        return level.getInt (2);
      }
      
      public int[] getInsurances () {
        int[] insurances = new int[3];
        
        insurances[0] = level.getInt (4);
        insurances[1] = level.getInt (5);
        insurances[2] = level.getInt (6);
      
        return insurances;
      }
      
      public float getDevelopmentEndPercent () {
        return level.getFloat (7);
      }
      
      public float getProtectionEndPercent () {
        return level.getFloat (8);
      }
      
      public float getKnowledgeTime () {
        return level.getFloat (9);
      }
      
      public TableRow getGrowers () {
        return growers;
      }
      
      public ArrayList<TableRow> getShocks () {
        return shocks;
      }
    }
    
    TableRow row;
    String uuid;
    String dateTime;
    ArrayList<Level> levels;
    ArrayList<TableRow> l2; 
    
    Session (TableRow _row) {
      row = _row;
      uuid = row.getString (0);
      dateTime = row.getString (2);
    }

    public void addLevels (LevelsData l, GrowersData g, ShocksData s) {
      levels = new ArrayList<Level>(); 
      l2 = l.getLevelsInSession (uuid);
      for (int i = 0; i < l2.size (); i ++) {
        TableRow tr = l2.get (i);
        String uuid = tr.getString (0);
        TableRow growers = g.getGrowersInLevel (uuid);
        ArrayList<TableRow> shocks = s.getShocksInLevel (uuid);
        Level l3 = new Level (tr, growers, shocks);
        levels.add (l3);
      } 
    }
    
    public String getUUID () {
      return uuid;
    }
    
    public String getDateTime () {
      return dateTime;
    }
    
    public ArrayList<Player.Session.Level> getLevels () {
      return levels;
    }

    public void printLevels () {
      println (uuid);
      //levels.get (0).printGrowers ();
      //for (int i = 0; i < levels.size (); i ++) {
        
        //int l = levels.get (i).getInt (2);
        //println (i + ": " + l);
      //}
    }
  }

  String ip;
  ArrayList<Player.Session> sessions;
  ArrayList<TableRow> levels;

  Player (String _ip, ArrayList<TableRow> _sessions) {
    ip = _ip;
    sessions = new ArrayList<Player.Session> ();
    for (int i = 0; i < _sessions.size (); i ++) {
      Player.Session s = new Player.Session (_sessions.get (i));
      sessions.add (s);
    }
  }

  public void addLevels (LevelsData l, GrowersData g, ShocksData s) {
    for (int i = 0; i < sessions.size (); i ++) {
      sessions.get (i).addLevels (l, g, s);
    }
  }

  public void printSessions () {
    for (int i = 0; i < sessions.size (); i ++) {
      println (sessions.get (i));
    }
  }

  public void printLevels () {
    /*for (int i = 0; i < sessions.size (); i ++) {
      sessions.get (i).printLevels ();
    }*/
  }
  
  public String getIP () {
    return ip;
  }
  
  public ArrayList<Player.Session> getSessions () {
    return sessions;
  }
}

