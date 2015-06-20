#fleet-x
import os
import re
import time
from datetime import datetime
from sys import stdout

print ("fleet-x v0.0.1")
print ("\n")
print ("Usage")
print ("On startup the most recently changed fleet chat log is automatically selected.")
print ("Any new lines starting with 'x' or 'X' are counted. Counter is reset by '---'.")
print ("\n")
print ("Use at your own risk")
print ("This program only parses plain text chat logs located under My Documents.")
print ("There is NO cache scraping or client modification going on.")
print ("\n")

path = os.getenv('USERPROFILE') + "\\Documents\\EVE\\logs\\ChatLogs"
print("Path: " + path) 
os.chdir(path);

file = max([f for f in os.listdir('.') if f.lower().startswith('fleet')], key=os.path.getmtime) 
print ("File: " + file)

print("\n")

print("Waiting for people to x-up...")

count = 0

def parseLine(line):
  global count
  m = re.match( ' \[ .* \] .* \> x', line, re.I)
  if m:
    count = count +1
    stdout.write("\rCount: %d" % count)
    stdout.flush()

  m = re.match( ' \[ .* \] .* \> ---', line, re.I)
  if m:
    count = 0
    print("\n\n--- " + datetime.utcnow().strftime("%H:%M") + " ---")
     
fd = open(file,'rb')
fd.seek(0, 2)
pos = fd.tell()
if pos % 2 != 0:
  pos = pos - 1

while True:
  fd.seek(pos, 0)
  bytes = bytearray(fd.read(8192))
  if len(bytes) < 2 or bytes.count(b'\n') == 0:
    time.sleep(0.3)
    continue
  
  for i in range(len(bytes)-1):
    if bytes[i] == 0 and bytes[i+1] == 10:
      cr = i + 1
      break
    if bytes[i] == 255 and bytes[i+1] == 254:
      bytes[i] = 32
      bytes[i+1] = 00
    
  line = bytes[0:cr].decode('utf-16')
  parseLine(line)  
  pos = pos + cr + 2
    
