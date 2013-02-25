import android
import time
import pickle

# Global vars for script
droid = android.Android()
interval = 5
gps_interval = 6
apDict = {}
logfile = open("apgather.log", 'w')

#--------------------------------------------------------*

# Returns list of access points found
# Each AP is a dictionary with values:
# ssid: name of the access point
# bssid: mac address of the access point
# capabilities: security used, if used
# frequency: frequency broadcasted
# level: power level detected
def get_ap_list():
   droid.wifiStartScan()
   return droid.wifiGetScanResults().result

# Returns dictionary of latitude and longitude
# at the current location
def get_loc():
   droid.startLocating()
   time.sleep(gps_interval)
   location = droid.readLocation().result
   if location != None:
      if "gps" in location:
         location = location["gps"]
      elif "network" in location:
         location = location["network"]
   droid.stopLocating()
   return location

# Incomplete - need to specify how it writes to file
# Writes to a log file as a backup measure
def write_to_log(bssid, ap):
   logfile.write("[")
   logfile.write(str(bssid) + ",")
   logfile.write(str(ap["name"]) + ",")
   logfile.write(str(ap["security"]) + ",")
   logfile.write(str(ap["power"]) + ",")
   logfile.write(str(ap["lat"]) + ",")
   logfile.write(str(ap["lon"]) + "]\n")

# Scans for access points
# Currently stops if the phone's volume is
# changed
def ap_scan():
   exit_flag = False
   pause_flag = False
   
   droid.wifiLockAcquireScanOnly()
   
   while not exit_flag:
      if pause_flag == True:
         continue

      polled_event = droid.eventWaitFor("scanevent",interval*1000).result
      droid.eventClearBuffer()

      if polled_event != None:
         if polled_event["data"] == "toggle":
            exit_flag = True
            continue
         if polled_event["data"] == "pause":
            if pause_flag:
               pause_flag = False
            else:
               pause_flag = True
            continue
      
      location = get_loc()
      if location == None:
         continue
      hotspots = get_ap_list()
      lat = location["latitude"]
      lon = location["longitude"]
      
      if len(hotspots) == 0:
         continue
         
      for ap in hotspots:
         name = ap["ssid"]
         bssid = ap["bssid"]
         security = ap["capabilities"]
         power = ap["level"]
         
         if bssid in apDict:
            #compare power
            if power < apDict[bssid]["power"]:
               #replace old with new
               apDict[bssid]["power"] = power
               apDict[bssid]["lat"] = lat
               apDict[bssid]["lon"] = lon
         else:
            #add new
            apDict[bssid] = {"name": name, "security": security, "power": power, "lat": lat, "lon": lon}
         # Log the raw data for verification/recovery purposes
         write_to_log(bssid, apDict[bssid])
   droid.wifiLockRelease
   return 

# Incomplete - need to specify how it writes to file
def ap_to_file(fname):
   apfile = open(fname, 'w')
   for mac in apDict.keys():
      # Standardize this format
      apfile.write(pickle.dumps(apDict))
   apfile.close()

#--------------------------------------------------------*

# SCRIPT EXECUTES FROM HERE

droid.wakeLockAcquireDim()

droid.webViewShow("file:///sdcard/sl4a/scripts/AP_Scanner/AP_Scanner_UI.html")

started = False

while True:
   polledEvent = droid.eventWaitFor("scanevent").result
   droid.eventClearBuffer()

   if polledEvent["data"] == "toggle":
      ap_scan()
      continue
   if polledEvent["data"] == "write":
      ap_to_file("apdata")
      continue
   if polledEvent["data"] == "exit":
      break

# Remember to close our log
logfile.close()

# Release wake lock before we leave
droid.wakeLockRelease()

print len(apDict) , " access points found during the scan!"
