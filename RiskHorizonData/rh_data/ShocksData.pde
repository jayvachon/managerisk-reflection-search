
class ShocksData {
  
  Table shocks; // shock_uuid, level_uuid, instantiate_time[blank], probability, severity, time_researched, damage, times_viewed[blank], minigame_multiplier
  
  ShocksData (String table) {
    println ("loading shocks data...");
    shocks = loadTable ("shocks.csv");
  }
  
  ArrayList<TableRow> getShocksInLevel (String levelUUID) {
    ArrayList<TableRow> shockRows = new ArrayList<TableRow>();
    for (int i = 0; i < shocks.getRowCount (); i ++) {
      TableRow tr = shocks.getRow (i);
      if (tr.getString (1).equals (levelUUID)) {
        shockRows.add (tr);       
      }
    }
    return shockRows;
  }
}
