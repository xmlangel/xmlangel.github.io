#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# markdown toc generator, v1.8
#
# Jaemok Jeong, 2014/10/27

from AppKit import NSPasteboard, NSArray
import re
import argparse

headRe = re.compile(r"(#+)\s*([^#]*)")

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def sendToClipboard(content):
    pb = NSPasteboard.generalPasteboard()
    pb.clearContents()
    c = NSArray.arrayWithObject_(content)
    pb.writeObjects_(c)


def generateSectionNum(format, depth, pos, sectionCount):
    # print format, depth, pos, sectionCount
    ganadara = u'가나다라마바사아자차카타파하'
    gndr = u'ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ'
    try:
        currentFormat = format[pos-depth]
    except IndexError:
        currentFormat = 'D'

    if currentFormat == 'd':
        return ".".join([str(s) for s in sectionCount if s != 0])[(depth-1)*2:]+"."
    elif currentFormat == '*':
        return "*"
    elif currentFormat == 'A':
        return chr(ord('A')+sectionCount[pos-1]-1)+"."
    elif currentFormat == 'a':
        return chr(ord('a')+sectionCount[pos-1]-1)+"."
    elif currentFormat == 'H':
        return ganadara[sectionCount[pos-1]-1]+"."
    elif currentFormat == 'h':
        return gndr[sectionCount[pos-1]-1]+"."
    else:
        return str(sectionCount[pos-1])+"."

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--depth", help="Start section number", type=int, default=2)
    parser.add_argument("-c", "--clipboard", help="Copy output to clipboard", dest='clipboard', action='store_true')
    parser.add_argument("-i", "--indent", help="Indent size", type=int, default=4)
    parser.add_argument("-f", "--format", help="ex) DDD* - D:1. d:1.1. *:* a:a. A:A. H:가. h:ㄱ.", default="DD**")
    parser.add_argument('filename')

    args = parser.parse_args()

    sectionCount = [0,0,0,0,0]
    currentPos = 0
    toc = ""

    with open(args.filename, "r") as f:
        for line in f.readlines():
            l = line.strip()
            if l.startswith("#"):
                m = headRe.match(l)
                c = len(m.group(1))
                if (c < args.depth):
                    continue
                if c == currentPos:
                    sectionCount[c-1] += 1
                elif c > currentPos:
                    for i in range(currentPos,c):
                        sectionCount[i] = 1
                    currentPos = c
                else:
                    sectionCount[c-1] += 1
                    for i in range(c,currentPos):
                        sectionCount[i] = 0
                    currentPos = c

                sec = generateSectionNum(args.format, args.depth, currentPos, sectionCount)
                spaces = " "*(currentPos-args.depth)*args.indent
                newsec = spaces + "%s %s\n" % (sec, m.group(2))
                print newsec.rstrip().encode('utf-8')
                toc += newsec
    if args.clipboard:
        sendToClipboard(toc)
    
if __name__ == '__main__':
    main()