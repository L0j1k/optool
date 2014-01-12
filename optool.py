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

app_version = 'v0.3a'

def extract(args):
  opt_length = args.length[0]
  opt_offset = args.offset[0]
  if(args.address):
    opt_offset = int("0x"+args.address, 0) + opt_offset
  if(args.file1):
    filedata = args.file1[0].read()
    if(opt_length == 0):
      outputdata = filedata[opt_offset:len(filedata):1]
    elif(opt_length > 0):
      outputdata = filedata[opt_offset:opt_offset+opt_length:1]
    else:
      outputdata = filedata[opt_offset:opt_offset+opt_length:-1]
    sys.stdout.write(outputdata)
    sys.exit(0)

def find(args):
  print("[+] find")

## output to:
#
# 00000  0011 2233 4455 6677 8899 aabb ccdd eeff  ................
# 00010  0011 2233 4455 6677 8899 aabb ccdd eeff  ................
###
##
# -> fix this nub shit
##
###
def hex(args):
  #debug
  print("[+] hex")
  filedata = args.file1[0].read()
  outputdata = ""
  for i in range(0,len(filedata)):
    nextchunk = str(filedata[i:i+16:1])
    for j in range(0, len(nextchunk)):
      this_address = "{=00002x}".format
      this_byteline = ""
      this_encoded = ""
    print byte(nextbyte)
    outputdata = outputdata + nextbyte
  print(outputdata)
  sys.exit(0)

def info(args):
  filedata=args.file1[0].read()
  print("[+] file information")
  print("[name]:",args.file1[0].name)
  print("[size]:",len(filedata),"bytes")
  print("\n[+] system information")
  print("[byteorder]:",sys.byteorder)
  sys.exit(0)

def main(args):
  print("[+] main")
  sys.exit(0)

def reverse(args):
  filedata = args.file1[0].read()
  print(filedata[::-1])
  sys.exit(0)

def swap(args):
  print("[+] swap")
  sys.exit(0)

def xor(args):
  print("[+] xor")
  sys.exit(0)

parser = argparse.ArgumentParser(
  description="Perform a variety of byte-level operations on files or byte sequences.",
  prog="optool.py",
  usage="optool.py"
)
# here goes [OPTIONS] you want to feed to your command
parser.add_argument("--version",
  action='version',
  version='optool.py '+app_version+' by L0j1k'
)
#parser.set_defaults(func=main)
subparsers = parser.add_subparsers(help="sub-command help")
# extract subparser
parser_extract = subparsers.add_parser("extract",
  help="extract a segment of specified length from specified offset in target file"
)
parser_extract.add_argument("-a", "--address",
  help="(hex) base hexadecimal address for extraction",
  const=0,
  default=0,
  metavar='hex_address',
  nargs='?',
  type=str
)
parser_extract.add_argument("offset",
  help="(int) extraction offset. use zero for file start. negative values reference from EOF",
  metavar='offset',
  nargs=1,
  type=int
)
parser_extract.add_argument("length",
  help="(int) length of bytes to extract. 0 extracts data from offset to EOF. if negative, returns reverse output (extracts backwards from offset)",
  metavar='length',
  nargs=1,
  type=int
)
parser_extract.add_argument("file1",
  help="primary target input file",
  nargs=1,
  type=argparse.FileType('r')
)
parser_extract.set_defaults(func=extract)
# find subparser
parser_find = subparsers.add_parser("find",
  help="attempts to find separate files inside input file, such as JPG, GIF, PNG, etc."
)
parser_find.add_argument("file1",
  help="primary target input file",
  nargs=1,
  type=argparse.FileType('r')
)
parser_find.set_defaults(func=find)
# hex subparser
parser_hex = subparsers.add_parser("hex",
  help="output target file into hexadecimal-formatted output"
)
parser_hex.add_argument("file1",
  help="primary target input file",
  nargs=1,
  type=argparse.FileType('r')
)
parser_hex.set_defaults(func=hex)
# info subparser
parser_info = subparsers.add_parser("info",
  help="display detailed information about target and system"
)
parser_info.add_argument("file1",
  help="primary target input file",
  nargs=1,
  type=argparse.FileType('r')
)
parser_info.set_defaults(func=info)
# reverse subparser
parser_reverse = subparsers.add_parser("reverse",
  help="reverse an input"
)
parser_reverse.add_argument("file1",
  help="primary target input file",
  nargs=1,
  type=argparse.FileType('r')
)
parser_reverse.set_defaults(func=reverse)
# swap subparser
parser_swap = subparsers.add_parser("swap",
  help="swap byte order of input (toggles big-/little-endian)"
)
parser_swap.add_argument("file1",
  help="primary target input file",
  nargs=1,
  type=argparse.FileType('r')
)
parser_swap.set_defaults(func=swap)
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
  help="byte sequence to xor with entire input file",
  default=False,
  metavar='byte',
  nargs=1,
  type=str
)
parser_xor.add_argument("-B", "--bytes",
  help="use provided byte sequences for xor operation instead",
  default=False,
  metavar=('byte1', 'byte2'),
  nargs=2,
  type=str
)
parser_xor.add_argument("-o", "--offset",
  help="xor beginning at provided offset in provided input",
  metavar='offset',
  nargs=1,
  type=int
)
parser_xor.set_defaults(func=xor)
args = parser.parse_args()
args.func(args)

## argparse subparsers:
# subparser xor [-o offset] file1 file2 | -b byte1 file1 | file1 -b byte1 | -B byte1 byte2
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
# info about file -- DONE
# extract from file -- DONE
# swap file

##
## required variables
##

##
## handle args
##

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
