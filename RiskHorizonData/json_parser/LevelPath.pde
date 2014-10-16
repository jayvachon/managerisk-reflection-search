
class LevelPath {
  
  ArrayList<JSONObject> path;
  boolean growersCompatible;
  
  LevelPath (ArrayList<JSONObject> _path) {
    path = _path;
    growersCompatible = getGrowersCompatible ();
    
    /*String s = "";
    for (int i = 0; i < path.size (); i ++) {
      int l = path.get (i).getInt ("level");
      s += l + ": ";
      
      String uuid = path.get (i).getString ("uuid");
      String ss = uuid.substring (0, 3);
      s += ss + ", ";
    }
    println (s);*/
    
    if (!growersCompatible) return;
    
    /*String s = "";
    for (int i = 0; i < path.size (); i ++) {
      int l = path.get (i).getInt ("level");
      s += l + ": ";
      
      String uuid = path.get (i).getString ("uuid");
      String ss = uuid.substring (0, 3);
      s += ss + ", ";
    }
    println (s);*/
    
    /*println ("======");
    for (int i = 0; i < path.size () - 1; i ++) {
      float time = getProtectionDifference (path.get (i), path.get (i + 1));
      JSONObject l = path.get (i);
      println ("level " + l.getInt ("level"));
      println ("protection time: " + time + ", protection end: " + l.getFloat ("protection end percent"));
      println ("development end: " + l.getFloat ("development end percent"));
    }
    println ("level 1");
    JSONObject l = path.get (path.size () - 1);
    float time = getProtectionDifference (l, null);
    println ("protection time: " + time + ", protection end: " + l.getFloat ("protection end percent"));
    println ("development end: " + l.getFloat ("development end percent"));*/
  }
  
  // ========== Growers ========== //
  
  private boolean getGrowersCompatible () {
    for (int i = 0; i < path.size () - 1; i ++) {
      int[] growers = getGrowers (path.get (i));
      int[] prevGrowers = getGrowers (path.get (i + 1));
      if (!crossCheckGrowers (growers, prevGrowers)) return false;
    }
    return true;
  }
  
  private boolean crossCheckGrowers (int[] growers, int[] prevGrowers) {
    for (int i = 0; i < growers.length; i ++) {
      if (growers[i] < prevGrowers[i]) return false;
    }
    return true;
  }
  
  private int[] getGrowers (JSONObject level) {
    JSONArray jGrowers = level.getJSONArray ("growers");
    int[] growers = new int[jGrowers.size ()];
    for (int i = 0; i < growers.length; i ++) {
      growers[i] = jGrowers.getInt (i);
    }
    return growers;
  }
  
  // ========== Shocks ========== //
  
  private ArrayList<JSONObject> getShocks (JSONObject level) {
    JSONArray jShocks = level.getJSONArray ("shocks");
    int shockCount = jShocks.size ();
    ArrayList<JSONObject> shocks = new ArrayList<JSONObject>();
    for (int i = 0; i < shockCount; i ++) {
      shocks.add (jShocks.getJSONObject (i));
    }
    return shocks;
  }
  
  private ArrayList<Float> getMultipliers (ArrayList<JSONObject> shocks) {
    ArrayList<Float> multipliers = new ArrayList<Float>();
    for (int i = 0; i < shocks.size (); i ++) {
      float multiplier = shocks.get (i).getFloat ("multiplier");
      if (multiplier > 0.0) multipliers.add (multiplier);
    }
    return multipliers;
  }
  
  // ========== Protection ========== //
  
  private float protectionPercentToTime (float percent) {
    return (percent / (0.000278 - (0.2988 * percent * 0.000278)) / 62.5);
  }
  
  private float getProtectionTime (JSONObject level) {
    float percent = level.getFloat ("protection end percent");
    return protectionPercentToTime (percent);
  }
  
  private float getProtectionDifference (JSONObject level, JSONObject prevLevel) {
    float time = getProtectionTime (level);
    float prevTime = (prevLevel == null) ? 0.0 : getProtectionTime (prevLevel);
    return max (0.0, time - prevTime);
  }
  
  public boolean getPossiblePath () {
    return growersCompatible;
  }
  
}
