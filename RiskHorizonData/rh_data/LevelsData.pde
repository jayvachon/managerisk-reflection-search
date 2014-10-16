
class LevelsData {
  
  Table levels; // level_uuid, session_uuid, level, pause_time[blank], insuranceI, insuranceII, insuranceIII, development_end_percent, protection_end_percent, knowledge_time
  
  LevelsData (String table) {
    println ("loading levels data...");
    levels = loadTable (table);
  }
  
  ArrayList<TableRow> getLevelsInSession (String session) {
    ArrayList<TableRow> l = new ArrayList<TableRow>();
    for (int i = 0; i < levels.getRowCount (); i ++) {
      TableRow tr = levels.getRow (i);
      if (tr.getString (1).equals (session)) {
        l.add (tr); 
      }
    }
    return l;
  }
}
