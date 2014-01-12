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
  usage="optool.py"
)
# here goes [OPTIONS] you want to feed to your command
parser.add_argument("-v", "--version",
  action='version',
  version='optool.py v0.2a by L0j1k'
)
subparsers = parser.add_subparsers(help="sub-command help")
# xor subparser
parser_xor = subparsers.add_parser('xor',
  help="xor provided targets with one another"
)
parser_xor.add_argument("file1",
  help="primary input file",
  nargs='?',
  type=argparse.FileType('r')
)
parser_xor.add_argument("file2",
  help="secondary input file",
  nargs='?',
  type=argparse.FileType('r')
)
parser_xor.add_argument("-b", "--byte",
  help="byte sequence to xor with input file. requires -x",
  default=False,
  metavar='byte',
  nargs=1
)
parser_xor.add_argument("-B", "--bytes",
  help="xor provided byte sequences with one another. requires -x",
  default=False,
  metavar=('byte1', 'byte2'),
  nargs=2
)
# info subparser
parser_info = subparsers.add_parser("info",
  help="display detailed information about target and system"
)
parser_info.add_argument("file1",
  help="primary target input file",
  nargs=1,
  type=argparse.FileType('r')
)
# extract subparser
parser_extract = subparsers.add_parser("extract",
  help="extract a segment of specified length from specified offset in target file"
)
parser_extract.add_argument("offset",
  help="(int) extraction offset. use zero for file start. negative values reference from EOF",
  metavar='offset',
  nargs=1,
  type=int
)
parser_extract.add_argument("length",
  help="(int) length of bytes to extract. if negative, returns reverse output (extracts backwards from offset)",
  metavar='length',
  nargs=1,
  type=int
)
parser_extract.add_argument("file1",
  help="primary target input file",
  nargs=1,
  type=argparse.FileType('r')
)
# find subparser
parser_find = subparsers.add_parser("find",
  help="attempts to find separate files inside input file, such as JPG, GIF, PNG, etc."
)
parser_find.add_argument("file1",
  help="primary target input file",
  nargs=1,
  type=argparse.FileType('r')
)
# reverse subparser
parser_reverse = subparsers.add_parser("reverse",
  help="reverse an input"
)
parser_reverse.add_argument("file1",
  help="primary target input file",
  nargs=1,
  type=argparse.FileType('r')
)
# swap subparser
parser_swap = subparsers.add_parser("swap",
  help="swap byte order of input (toggles big-/little-endian)"
)
parser_swap.add_argument("file1",
  help="primary target input file",
  nargs=1,
  type=argparse.FileType('r')
)
args = parser.parse_args()

## examples
# optools.py xor file1 file2
# optools.py xor -b 'ff' file1
# optools.py xor file1 -b 'ff'
# optools.py xor -B 'ff' 'a1'
# optools.py info file1
# optools.py extract 10 1 file1
# optools.py find file1
# optools.py swap file1
# optools.py reverse file1
## argparse subparsers:
# subparser xor file1 file2 | -b byte1 file1 | file1 -b byte1 | -B byte1 byte2
# subparser info
# subparser extract length offset file1
# subparser find
# subparser swap
# subparser reverse

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

## -i, --info
if(args.info == True):
  filedata=args.file1[0].read()
  print("<File information>")
  print("[Name]:",args.file1[0].name)
  print("[Size]:",len(filedata),"bytes")
  print("--------------\n<System information>")
  print("[Byteorder]:",sys.byteorder)
  sys.exit(0)
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
