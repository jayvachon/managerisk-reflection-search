
class GrowersData {

  Table growers; // grower_uuid, level_uuid, growerI, growerII, growerIII, growerIV, growerV, growerVI, growerVII, growerVIII, growerIX

  GrowersData (String table) {
    println ("loading growers data...");
    growers = loadTable (table);
  }

  TableRow getGrowersInLevel (String levelUUID) {
    for (int i = 0; i < growers.getRowCount (); i ++) {
      TableRow tr = growers.getRow (i);
      if (tr.getString (1).equals (levelUUID)) {
        return tr;
      }
    }
    return null;
  }
}

