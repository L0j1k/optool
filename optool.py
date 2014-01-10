#!/usr/bin/python3

#=-> optool.py -- perform a variety of byte-level operations on files or strings
#=-> (C)2014 L0j1k@L0j1k.com

import argparse, sys

# optool.py [file1] [file2]
# -> xor file1 with file2
# optool.py -b [bytes1] [file1]
# -> xor bytes1 with file1
# optool.py [file1] -b [bytes1]
# -> xor file1 with bytes1
# optool.py -B [bytes1] [bytes2]
# -> xor bytes1 with bytes2
# optool.py -r
# -> reverse file per-byte
# optool.py -i
# -> detail file info
# optool.py -o [offset] -x [length] 
# -> extract chunk length x starting offset o

parser = argparse.ArgumentParser(
  description="Perform a variety of byte-level operations on files or byte sequences.",
  prog="optool.py",
  usage="optool.py [OPTIONS] [FILE1] [FILE2]"
)
parser.add_argument("-b", "--byte",
  help="byte sequence to xor with input file",
  default=False,
  metavar='byte',
  nargs=1
)
parser.add_argument("-B", "--bytes",
  help="xor provided byte sequences with one another",
  default=False,
  metavar=('byte1', 'byte2'),
  nargs=2
)
parser.add_argument("-i", "--info",
  help="display detailed information about file",
  action="store_true",
  default=False
)
parser.add_argument("-o", "--offset",
  help="(int) extraction offset. default is file start",
  default=0,
  metavar='offset',
  nargs='?',
  type=int
)
parser.add_argument("-r", "--reverse",
  help="reverse an input file",
  action="store_true"
)
parser.add_argument("--version",
  action='version',
  version='optool.py v0.1a'
)
parser.add_argument("-x", "--extract",
  help="(int) length of bytes to extract. implies -o. default is 1. if negative, returns reversed from offset",
  default=1,
  metavar='length',
  nargs='?',
  type=int
)
parser.add_argument("file1",
  help="primary input file",
  nargs=1,
  type=argparse.FileType('r')
)
parser.add_argument("file2",
  help="secondary input file",
  nargs='?',
  type=argparse.FileType('r')
)
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
#if args.x:
#  extract_bytes = args.x

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
