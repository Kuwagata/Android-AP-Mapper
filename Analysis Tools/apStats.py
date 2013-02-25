#!/usr/bin/env python
import os, sys, pickle

def main():
   datafile = open("data/apdict.dat",'r')
   data = pickle.load(datafile)
   datafile.close()

   stats = {"None":0, "WEP":0, "WPA":0, "WPA2":0,"Ad-hoc":0,"Other":0}
   
   filter_clemson = True
   filter_guest = True

   for bssid in data.keys():
      sec = data[bssid]["security"]
      if filter_clemson:
         if data[bssid]["name"] == "tigernet":
            continue
         if data[bssid]["name"] == "clemsonguest":
            continue
      if filter_guest:
         if "guest" in data[bssid]["name"]:
            continue
      if sec == "":
         stats["None"] += 1
         continue
      if "WPA2" in sec:
         stats["WPA2"] += 1
         continue
      elif "WPA" in sec:
         stats["WPA"] += 1
         continue
      elif "WEP" in sec:
         stats["WEP"] += 1
         continue
      elif "IBSS" in sec:
         stats["Ad-hoc"] += 1
         continue
      else:
         stats["Other"] += 1
         continue

   total = 0.0
   for count in stats.values():
      total += count

   print "---------Stats---------"
   print "WPA2: ", stats["WPA2"], ", ", float(stats["WPA2"])/total
   print "WPA: ", stats["WPA"], ", ", float(stats["WPA"])/total
   print "WEP: ", stats["WEP"], ", ", float(stats["WEP"])/total
   print "None: ", stats["None"], ", ", float(stats["None"])/total
   print "Ad-hoc: ", stats["Ad-hoc"], ", ", float(stats["Ad-hoc"])/total
   print "Other: ", stats["Other"], ", ", float(stats["Other"])/total
   print "\n*** Total: ", total, "***"

if __name__ == "__main__":
   main()
