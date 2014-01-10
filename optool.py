#!/usr/bin/python3

#=-> optool.py -- perform a variety of byte-level operations on files or strings
#=-> (C)2014 L0j1k@L0j1k.com

import argparse, sys

parser = argparse.ArgumentParser(description="Perform a variety of byte-level operations on files or byte sequences.")
parser.add_argument("-b", "--byte", help="byte sequence to xor with input file")
parser.add_argument("-B", "--bytes", help="xor provided byte sequences with one another")
parser.add_argument("-i", "--info", help="display detailed information about file")
parser.add_argument("-o", "--offset", help="extraction offset (default is file start)")
parser.add_argument("-r", "--reverse", help="reverse an input file", action="store_true")
parser.add_argument("-x", "--extract", help="(int) length of bytes to extract. implies -o. default is 1. if negative, returns reversed from offset", type=int)
args = parser.parse_args()

# todo:
# xor files
# xor file with byteseq
# xor two byteseqs
# reverse file
# info about file
# extract from file
# bytes to extract

def usage():
  print('optool.py -- perform a variety of byte-level operations')
  print('(C)2014 -- written by L0j1k@L0j1k.com')
  print('')
  print('usage: optool.py [OPTIONS] [file1] [file2]')
  sys.exit(0)

#debug
print(len(sys.argv))

#handle args
if args.x:
  extract_bytes = args.x

#open files
#with open(infileone, 'r') as inputone:
#  indataone = inputone.read()

#print status and impending operations
#if(xorfiles == True):
#  with open(infiletwo, 'r') as inputtwo:
#    indatatwo = inputtwo.read()
#    print("xor",infileone,"and",infiletwo,"...")

#xor
#if(xorfiles == True):
#  for i in range(0, totallen):
#    byte1 = indataone[i:1]
#    byte2 = indatatwo[i:1]
#    outputdata = outputdata + (byte1 ^ byte2)

#print status and summarize operations
print("finished!")
