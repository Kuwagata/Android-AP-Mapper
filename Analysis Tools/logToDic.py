#!/usr/bin/env python
import os, sys, pickle

def main():
   log = open("data/apgather.log",'r')
   apDict = {}
   for line in log:
      line = line.strip("[]\n")
      bssid,name,security,power,lat,lon = line.split(",")
      if bssid in apDict:
         if power > apDict[bssid]["power"]:
            apDict[bssid]["lat"] = lat
            apDict[bssid]["lon"] = lon
      else:
         apDict[bssid] = {"name":name,"security":security,"power":power,"lat":lat, "lon":lon}

   toWrite = open("data/apdict.dat",'w')
   pickle.dump(apDict,toWrite,0)

if __name__ == "__main__":
   main()
