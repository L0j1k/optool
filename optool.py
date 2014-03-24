#!/usr/bin/python3
# (C)2014 L0j1k@L0j1k.com
"""Perform a variety of byte-level operations on files or strings.

optool.py [file1] [file2]
-> xor file1 with file2
optool.py -b [bytes1] [file1]
-> xor bytes1 with file1
optool.py [file1] -b [bytes1]
-> xor file1 with bytes1
optool.py -B [bytes1] [bytes2]
-> xor bytes1 with bytes2
optool.py -r
-> reverse file per-byte
optool.py -i
-> detail file info
optool.py -o [offset] -x [length]
-> extract chunk length x starting offset o
"""

import argparse, os, sys

app_version = 'v0.5a'


def func_extract(args):
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

def func_find(args):
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
def func_hexdump(args):
  #debug
  print("[+] hex")
  encoding = args.encoding
  if(args.encoding == 'utf-8'):
    print('utf-8')
  elif(args.encoding == 'utf-16'):
    print('utf-16')
  elif(args.encoding == 'latin'):
    print('latin')
  elif(args.encoding == 'ebcdic'):
    print('ebcdic')
  else:
    usage()
  filedata = args.file1[0].read()
  currentaddress = 0
  for i in range(0,len(filedata[0::8])):
    currentaddress += 8
    thischunk = str(filedata[i*8:i*8+8:1])
    #debug
    print("THISCHUNK:[",thischunk,"]len[",len(filedata[0::8]),"]")
    for thisbyte in thischunk:
      block_byte = "{}{} {}{} {}{} {}{} {}{} {}{} {}{} {}{}".format(thisbyte)
    block_addr = str("{}".format(hex(currentaddress)))
    block_data = ""
    outputline = block_addr + block_byte + block_data
    print(outputline)
  sys.exit(0)

def func_info(args):
  encoding = args.encoding
  filedata=args.file1[0].read()
  #debug
  print("BLAH[",filedata[0],"]")
  minbyte = bytes(min(filedata), encoding)
  maxbyte = bytes(max(filedata), encoding)
  print("[+] file information")
  print("[name]:",args.file1[0].name)
  print("[size]:",len(filedata),"bytes")
  print("[minbyte]:",minbyte)
  print("[maxbyte]:",maxbyte)
  print("\n[+] system information")
  print("[byteorder]:",sys.byteorder)
  sys.exit(0)

def func_main(args):
  print("[+] main")
  sys.exit(0)

def func_output(args):
  print("[+] output")
  if(args.encoding == 'utf-8'):
    print('utf-8')
  elif(args.encoding == 'utf-16'):
    print('utf-16')
  elif(args.encoding == 'latin'):
    print('latin')
  elif(args.encoding == 'ebcdic'):
    print('ebcdic')
  else:
    usage()
  byteseq = args.output1[0]
  print()
  sys.exit(0)

def func_reverse(args):
  filedata = args.file1[0].read()
  print(filedata[::-1])
  sys.exit(0)

def func_swap(args):
  print("[+] swap")
  sys.exit(0)

def func_xor(args):
  # todo: byte sequences
  if(args.offset1):
    offset1 = args.offset1
  else:
    offset1 = 0
  if(args.offset2):
    offset2 = args.offset2
  else:
    offset2 = 0
  if(args.length):
    length = True
  else:
    length = False
  args.file1.seek(offset1)
  args.file2.seek(offset2)
  thislength = 0
  for thischar in args.file1.read():
    thislength += 1
    if(length):
      if(thislength > args.length):
        break
    try:
      sys.stdout.write(hex(ord(thischar) ^ ord(args.file2.read(1))))
    except:
      break
  sys.exit(0)

def usage():
  print("")
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
  help="(int) length of bytes to extract. 0 extracts data from offset to EOF. if negative, returns reversed output (extracts backwards from offset)",
  metavar='length',
  nargs=1,
  type=int
)
parser_extract.add_argument("file1",
  help="primary target input file",
  nargs=1,
  type=argparse.FileType('r')
)
parser_extract.set_defaults(func=func_extract)
# find subparser
parser_find = subparsers.add_parser("find",
  help="attempts to find separate files inside input file, such as JPG, GIF, PNG, etc."
)
parser_find.add_argument("file1",
  help="primary target input file",
  nargs=1,
  type=argparse.FileType('r')
)
parser_find.set_defaults(func=func_find)
# hex subparser
parser_hexdump = subparsers.add_parser("hexdump",
  help="output target file into hexadecimal-formatted output"
)
parser_hexdump.add_argument("-e", "--encoding",
  help="encoding for hexdump output. possible values are 'utf-8', 'utf-16', 'latin', 'ebcdic'. default is 'utf-8'",
  default='utf-8',
  metavar='encoding',
  nargs='?',
  type=str
)
parser_hexdump.add_argument("file1",
  help="primary target input file",
  nargs=1,
  type=argparse.FileType('r')
)
parser_hexdump.set_defaults(func=func_hexdump)
# info subparser
parser_info = subparsers.add_parser("info",
  help="display detailed information about target and system"
)
parser_info.add_argument("-e", "--encoding",
  help="encoding to use for file. valid options are 'utf-8', 'utf-16', 'latin1', ebcdic'. default is 'utf-8'",
  default='utf-8',
  metavar='encoding',
  nargs='?',
  type=str
)
parser_info.add_argument("file1",
  help="primary target input file",
  nargs=1,
  type=argparse.FileType('r')
)
parser_info.set_defaults(func=func_info)
# output subparser
parser_output = subparsers.add_parser("output",
  help="outputs specified byte sequence"
)
parser_output.add_argument("output1",
  help="sequence to output",
  nargs=1,
  type=str
)
parser_output.add_argument("-e", "--encoding",
  help="character encoding to use for decoding to bytes. valid options are 'utf-8', 'utf-16', 'latin1', 'ebcdic'. default is 'utf-8'",
  default='utf-8',
  metavar='encoding',
  nargs='?',
  type=str
)
parser_output.set_defaults(func=func_output)
# reverse subparser
parser_reverse = subparsers.add_parser("reverse",
  help="reverse an input"
)
parser_reverse.add_argument("file1",
  help="primary target input file",
  nargs=1,
  type=argparse.FileType('r')
)
parser_reverse.set_defaults(func=func_reverse)
# swap subparser
parser_swap = subparsers.add_parser("swap",
  help="swap byte order of input (toggles big-/little-endian)"
)
parser_swap.add_argument("file1",
  help="primary target input file",
  nargs=1,
  type=argparse.FileType('r')
)
parser_swap.set_defaults(func=func_swap)
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
parser_xor.add_argument("-l", "--length",
  help="xor for specified length. default all",
  metavar='length',
  nargs='?',
  type=int
)
parser_xor.add_argument("-o1", "--offset1",
  help="xor beginning at provided offset in first input file. default 0",
  default=0,
  metavar='offset',
  nargs='?',
  type=int
)
parser_xor.add_argument("-o2", "--offset2",
  help="xor beginning at provided offset in second input file. default 0",
  default=0,
  metavar='offset',
  nargs='?',
  type=int
)
parser_xor.set_defaults(func=func_xor)
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

############################################################3
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
