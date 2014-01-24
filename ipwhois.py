#!/usr/bin/python3

#
# test connections for whois
#
# todo:
# 

import re, socket, sys

version = '0.1.0a'

def sysprint(data):
  sys.stdout.write(data)
  sys.stdout.flush()

def usage(message):
  print(sys.argv[0],version,"by L0j1k")
  print("checks a file for ip addresses and checks whois for each")
  print(sys.argv[0],"[file]\n")
  print(message)
  sys.exit(0)

argc = len(sys.argv)
if(argc != 2):
  usage("[!] wrong number of args")

inputFile = sys.argv[1]
print("[+] checking file",inputFile,"...")

with open(inputFile, 'r') as input:
  for line in input:
    line = line.rstrip()
    sysprint("[=] "+line)
    for chunk in line.split():
      sysprint("[-] "+chunk+"\n")
      matchez = re.search('([0123]?\.[0-9]?\.[0-9]+):()', chunk)
      if(matchez.group(1)):
        sysprint(matchez.group(0))
    sysprint("\n")
