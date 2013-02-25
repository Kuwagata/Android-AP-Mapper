#!/usr/bin/env python
import os,sys,xml.dom.minidom, pickle

url = 'http://earth.google.com/kml/2.2'

def createkml(apDict):
   kmlfile = open("data/wepdata.kml","w")

   kmlDoc = xml.dom.minidom.Document()
   kmlElement = kmlDoc.createElementNS(url,'kml')
   kmlElement.setAttribute('xmlns',url)
   kmlElement = kmlDoc.appendChild(kmlElement)
   documentElement = kmlDoc.createElement('Document')
   documentElement = kmlElement.appendChild(documentElement)

   for bssid in apDict.keys():
      sec = apDict[bssid]["security"]

      if not "WEP" in sec:
         continue

      apcolor = "http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png"

      # Create placemark for each AP
      placemarkElement = kmlDoc.createElement('Placemark')
      
      # Create style for the placemark
      styleElement = kmlDoc.createElement('Style')
      iconStyleElement = kmlDoc.createElement('IconStyle')
      iconElement = kmlDoc.createElement('Icon')
      linkElement = kmlDoc.createElement('href')
      linkValue = kmlDoc.createTextNode(apcolor)
      linkElement.appendChild(linkValue)
      iconElement.appendChild(linkElement)
      iconStyleElement.appendChild(iconElement)
      styleElement.appendChild(iconStyleElement)
      placemarkElement.appendChild(styleElement)

      # Create extended data section for the placemark
      extElement = kmlDoc.createElement('ExtendedData')
      placemarkElement.appendChild(extElement)

      # Create data section for the placemark and set name
      descriptionElement = kmlDoc.createElement('Data')
      descriptionElement.setAttribute('name', 'Wireless Network')

      # Create value for the placemark
      wapElement = kmlDoc.createElement('value')
      descriptionElement.appendChild(wapElement)

      # Value contains name of Access Point and security type
      wapName = kmlDoc.createTextNode(str(apDict[bssid]["name"]))
      wapSec = kmlDoc.createTextNode(str(apDict[bssid]["security"]))
      wapElement.appendChild(wapName)
      wapElement.appendChild(wapSec)

      extElement.appendChild(descriptionElement)

      # Now create the point
      pointElement = kmlDoc.createElement('Point')
      placemarkElement.appendChild(pointElement)
      coorElement = kmlDoc.createElement('coordinates')
      coorElement.appendChild(kmlDoc.createTextNode(str(apDict[bssid]["lon"])+','+str(apDict[bssid]["lat"])))
      pointElement.appendChild(coorElement)
      
      documentElement.appendChild(placemarkElement)

   kmlfile.write(kmlDoc.toprettyxml(' ', newl = '\n', encoding = 'utf-8'))
   kmlfile.close()
   return

def main():
   dictfile = open("data/apdict.dat",'r')
   data = pickle.load(dictfile)
   createkml(data)

if __name__ == "__main__":
   main()
