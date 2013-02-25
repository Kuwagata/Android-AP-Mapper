#!/usr/bin/env python
import os, sys

def main():
   log = open("data/apgather.log",'r')
   new = open("data/apgather.new",'w')

   for line in log:
      if not line.startswith("["):
         print "Found corrupted line - Missing left brace"
         continue
      if not line.endswith("]\n"):
         print "Found corrupted line - Missing right brace"
         continue
      stripped_line = line.strip("[]\n")
      if len(stripped_line.split(",")) != 6:
         print "Found corrupted line - not enough data"
         continue
      new.write(line)
   
   log.close()
   new.close()
   os.rename("data/apgather.log", "data/apgather.old")
   os.rename("data/apgather.new", "data/apgather.log")

if __name__ == "__main__":
   main()
