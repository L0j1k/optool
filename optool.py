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

import argparse
import sys

__version__ = 'v0.5a'

DEFAULT_ENCODING = 'utf-8'
ACCEPTED_ENCODINGS = ['utf-8', 'utf-16', 'latin', 'ebcdic']
assert DEFAULT_ENCODING in ACCEPTED_ENCODINGS


def command(name):
    """Decorator to add metadata to a func_* declaration.
    """
    def command_decorator(function):
        """Actual decorator function returned by call to command().

        Example:
            @command("foo")
            def func_foo(args):
                ...

            Here, command("foo") is called at module import time, returning
            this inner function. Which is then called with func_foo as
            the first and only argument. Because this inner function
            returns the original function, the name 'func_foo' is bound
            to the original function just as if @command("foo") had not
            been put above its declaration.
        """
        function.name = name
        function.help = function.__doc__.strip().split("\n")[0]
        return function

    return command_decorator


@command("extract")
def func_extract(args):
    """Extract a segment of specified length from specified offset in target file.
    """
    if args.address:
        args.offset = int("0x" + args.address, 0) + args.offset
    if args.file1:
        filedata = args.file1.read()
        if args.length == 0:
            outputdata = filedata[args.offset:len(filedata):1]
        elif args.length > 0:
            outputdata = filedata[args.offset:args.offset + args.length:1]
        else:
            outputdata = filedata[args.offset:args.offset + args.length:-1]
        sys.stdout.write(outputdata)
    return 0


@command("find")
def func_find(args):
    """Attempt to find separate files inside input file, such as JPG, GIF, PNG, etc.
    """
    print("[+] find")
    return 0


## output to:
#
# 00000  0011 2233 4455 6677 8899 aabb ccdd eeff  ................
# 00010  0011 2233 4455 6677 8899 aabb ccdd eeff  ................
###
##
# -> fix this nub shit
##
###
@command("hexdump")
def func_hexdump(args):
    """Output target file into hexadecimal-formatted output.
    """
    #debug
    print("[+] hex")
    if args.encoding in ACCEPTED_ENCODINGS:
        print(args.encoding)
    else:
        return usage()
    filedata = args.file1.read()
    currentaddress = 0
    for i in range(0, len(filedata[0::8])):
        currentaddress += 8
        thischunk = str(filedata[i*8:i*8+8:1])
        #debug
        print("THISCHUNK:[", thischunk, "]len[", len(filedata[0::8]), "]")
        for thisbyte in thischunk:
            block_byte = "{}{} {}{} {}{} {}{} {}{} {}{} {}{} {}{}".format(thisbyte)
        block_addr = str("{}".format(hex(currentaddress)))
        block_data = ""
        outputline = block_addr + block_byte + block_data
        print(outputline)
    return 0


@command("info")
def func_info(args):
    """Display detailed information about target and system.
    """
    encoding = args.encoding
    filedata = args.file1.read()
    #debug
    print("BLAH[", filedata[0], "]")
    minbyte = bytes(min(filedata), encoding)
    maxbyte = bytes(max(filedata), encoding)
    print("[+] file information")
    print("[name]:", args.file1.name)
    print("[size]:", len(filedata), "bytes")
    print("[minbyte]:", minbyte)
    print("[maxbyte]:", maxbyte)
    print("\n[+] system information")
    print("[byteorder]:", sys.byteorder)
    return 0


def func_main(args):
    print("[+] main")
    return 0


@command("output")
def func_output(args):
    """Outputs specified byte sequence.
    """
    print("[+] output")
    if args.encoding in ACCEPTED_ENCODINGS:
        print(args.encoding)
    else:
        return usage()
    print()
    return 0


@command("reverse")
def func_reverse(args):
    """Reverse an input.
    """
    filedata = args.file1.read()
    print(filedata[::-1])
    return 0


@command("swap")
def func_swap(args):
    """Swap byte order of input (toggles big-/little-endian).
    """
    print("[+] swap")
    return 0


@command("xor")
def func_xor(args):
    """XOR provided targets with one another.
    """
    # todo: byte sequences
    if args.offset1:
        offset1 = args.offset1
    else:
        offset1 = 0
    if args.offset2:
        offset2 = args.offset2
    else:
        offset2 = 0
    if args.length:
        length = True
    else:
        length = False
    args.file1.seek(offset1)
    args.file2.seek(offset2)
    thislength = 0
    for thischar in args.file1.read():
        thislength += 1
        if length:
            if thislength > args.length:
                break
        try:
            sys.stdout.write(hex(ord(thischar) ^ ord(args.file2.read(1))))
        except:
            break
    return 0


def usage():
    print("")
    return 0


def make_parser():
    """Create ArgumentParser instance with the specs we need.
    """
    parser = argparse.ArgumentParser(
        description="Perform a variety of byte-level operations on files or byte sequences.",
    )
    # here goes [OPTIONS] you want to feed to your command
    parser.add_argument("--version",
        action='version',
        version='optool.py ' + __version__ + ' by L0j1k'
    )
    # parser.set_defaults(func=None)
    subparsers = parser.add_subparsers(help="sub-command help")

    def add_subparser(func):
        """Make a func_* subparser.
        """
        subparser = subparsers.add_parser(func.name, help=func.help)
        subparser.set_defaults(func=func)
        return subparser

    encodings_message = (
       "valid options are {0}. "
       "default is {1}.".format(
            ', '.join(repr(encoding) for encoding in ACCEPTED_ENCODINGS),
            repr(DEFAULT_ENCODING)
       )
    )

    # extract subparser
    parser_extract = add_subparser(func_extract)
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
        type=int
    )
    parser_extract.add_argument("length",
        help="(int) length of bytes to extract. 0 extracts data from offset to EOF. if negative, returns reversed output (extracts backwards from offset)",
        metavar='length',
        type=int
    )
    parser_extract.add_argument("file1",
        help="primary target input file",
        type=argparse.FileType('r')
    )

    # find subparser
    parser_find = add_subparser(func_find)
    parser_find.add_argument("file1",
        help="primary target input file",
        type=argparse.FileType('r')
    )

    # hex subparser
    parser_hexdump = add_subparser(func_hexdump)
    parser_hexdump.add_argument("-e", "--encoding",
      help="encoding for hexdump output. " + encodings_message,
      default=DEFAULT_ENCODING,
      metavar='encoding',
      nargs='?',
      type=str
    )

    parser_hexdump.add_argument("file1",
      help="primary target input file",
      type=argparse.FileType('r')
    )

    # info subparser
    parser_info = add_subparser(func_info)
    parser_info.add_argument("-e", "--encoding",
      help="encoding to use for file. " + encodings_message,
      default=DEFAULT_ENCODING,
      metavar='encoding',
      nargs='?',
      type=str
    )
    parser_info.add_argument("file1",
      help="primary target input file",
      type=argparse.FileType('r')
    )

    # output subparser
    parser_output = add_subparser(func_output)
    parser_output.add_argument("output1",
      help="sequence to output",
      type=str
    )
    parser_output.add_argument("-e", "--encoding",
      help="character encoding to use for decoding to bytes. " + encodings_message,
      default=DEFAULT_ENCODING,
      metavar='encoding',
      nargs='?',
      type=str
    )

    # reverse subparser
    parser_reverse = add_subparser(func_reverse)
    parser_reverse.add_argument("file1",
      help="primary target input file",
      type=argparse.FileType('r')
    )

    # swap subparser
    parser_swap = add_subparser(func_swap)
    parser_swap.add_argument("file1",
      help="primary target input file",
      type=argparse.FileType('r')
    )

    # xor subparser
    parser_xor = add_subparser(func_xor)
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

    return parser


def main():
    """Entry point orchestrating what module does when run as a script.
    """
    parser = make_parser()
    args = parser.parse_args()
    if 'func' not in args:
        parser.print_help()
        status = 1
    else:
        status = args.func(args)
    sys.exit(status or 0)


if __name__ == "__main__":
    main()

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
#if xorfiles:
#  with open(infiletwo, 'r') as inputtwo:
#    indatatwo = inputtwo.read()
#    print("xor",infileone,"and",infiletwo,"...")

#xor
#if xorfiles:
#  for i in range(0, totallen):
#    byte1 = indataone[i:1]
#    byte2 = indatatwo[i:1]
#    outputdata = outputdata + (byte1 ^ byte2)
