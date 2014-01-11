#!/usr/bin/python3

#=-> optool.py -- perform a variety of byte-level operations on files or strings
#=-> (C)2014 L0j1k@L0j1k.com

import argparse, os, sys

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
parser.add_argument("-f", "--find",
  help="attempts to find separate files inside input file, such as JPG, GIF, PNG, etc.",
  metavar='filetype',
  nargs=1
)
parser.add_argument("-i", "--info",
  help="display detailed information about file",
  action="store_true",
  default=False
)
parser.add_argument("-o", "--offset",
  help="(int) extraction offset. use zero for file start. requires -x. negative values reference from EOF",
  metavar='offset',
  nargs=1,
  type=int
)
parser.add_argument("-r", "--reverse",
  help="reverse an input file.",
  default=False,
  action="store_true"
)
parser.add_argument("-s", "--swap",
  help="swap byte order of input file.",
  action="store_true",
  default=False
)
parser.add_argument("-v", "--version",
  action='version',
  version='optool.py v0.2a by L0j1k'
)
parser.add_argument("-x", "--extract",
  help="(int) length of bytes to extract. requires -o. if negative, returns reverse output (same as extracting backwards from offset)",
  metavar='length',
  nargs=1,
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
# reverse file -- DONE
# info about file
# extract from file
# bytes to extract

def usage():
  print('optool.py -- perform a variety of byte-level operations')
  print('(C)2014 -- written by L0j1k@L0j1k.com')
  print('')
  print('usage: optool.py [OPTIONS] [file1] [file2]')
  sys.exit(0)

def usage():
  sys.exit(0)

#debug
print(len(sys.argv))

##
## required variables
##
func_extract=False
func_offset=False

##
## handle args
##

## -r, --reverse
if(args.reverse == True):
  filedata = args.file1[0].read()
  print("xor",filedata,"and",filedata,"...")
  output_data = filedata[::-1]
  print(output_data)
  sys.exit(0)
## -s, --swap
## -x, --extract
if(args.extract or args.offset):
  opt_length=args.extract
  opt_offset=args.offset
  if(args.file2):
    usage()
  if(args.file1):
    print("[+] starting extraction of",str(opt_length),"bytes from offset",str(opt_offset),"in",args.file1[0].name)
    filedata = args.file1[0].read()
    if(opt_length == 0):
      print("[*] cannot extract 0 bytes!")
      sys.exit(0)
    elif(opt_length > 0):
      #debug1
      print("filedata[",str(opt_offset),":",str(opt_offset+opt_length),":1]")
      outputdata = filedata[opt_offset:opt_offset+opt_length:1]
    else:
      #debug1
      print("filedata[",str(opt_offset),":",str(opt_offset+opt_length),":-1]")
      outputdata = filedata[opt_offset:opt_offset+opt_length:-1]
    print(outputdata)

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
