#!/usr/bin/env python3

import os
import time
import hashlib
import subprocess
import lzma
import glob
import mmap
import argparse


def checktempfile():  # check to see if tempfiles already exist
    if os.path.isfile(strippedFilename+'ofr'):  # remove tempfiles if they already exist
        os.remove(strippedFilename+'ofr')
    if os.path.isfile(strippedFilename+'pcm'):
        os.remove(strippedFilename+'pcm')
    if os.path.isfile(strippedFilename+'raw'):
        os.remove(strippedFilename+'raw')
    if os.path.isfile(strippedFilename+'flac'):
        os.remove(strippedFilename+'flac')


def isitcompressed():  # check magic number to see if compressed
    firstbytes = data[0:4]  # copy magic number header
    firstbytestext = str(firstbytes,encoding="Latin-1")  # convert to string
    if firstbytestext == sfqx:  # check to see if magic number matches
        return 1
    elif firstbytestext == sfqu:
        return 2
    else:  # if no sfq header return 0
        return 0


def parsecompressed():  # find out how long the non-audio data is
    lzmalengthbytes = bytes(data[4:7])  # get length bytes
    lzmalengthint = int.from_bytes(lzmalengthbytes, byteorder='little')  # convert to integer
    return lzmalengthint


def parsesfq16(sfqdata):  # parse non-audio data to figure out where to write data
    sampleindex = sfqdata.find(samplemagic)  # find beginning of sample data
    firstchunkend = sampleindex + 12  # add 12 to figure out where to insert decompressed audio
    return firstchunkend


def parsesfq24(sfqdata):  # parse non-audio data to figure out where to write data
    sampleindex = sfqdata.find(samplemagic)  # find beginning of sample data
    firstchunkend = sampleindex + 12  # add 12 to figure out where to insert decompressed audio
    sample24end = sampleindex + 20  # add 20 to figure out where to insert decompressed 24-bit audio
    return firstchunkend, sample24end


def isitasoundfont():  # check magic numbers to determine if the file is a soundfont
    RIFF = b'\x52\x49\x46\x46'  # magic number for RIFF file
    sfbk = b'\x73\x66\x62\x6b'  # magic number for soundfont file
    v204 = b'\x02\x00\x04\x00'  # version number for 24-bit soundfont files
    sample24 = b'\x73\x6d\x32\x34'  # magic number for 24-bit sample bank
    firstbytes = data[0:4]
    if firstbytes == RIFF:
        secondbytes = data[8:12]
        if secondbytes == sfbk:
            sfver = data[32:36]
            if sfver == v204:
                sfvercheck = data.find(sample24)
                if sfvercheck != -1:
                    return 2
                else:
                    return 1
            else:
                return 1
        else:
            return 0
    else:
        return 0


def convertlength(binarylength):  # convert length to integer
    lengthhex = bytes(data[binarylength:binarylength+5])  # grab length bytes from file
    length = int.from_bytes(lengthhex, byteorder='little')  # convert to bytes
    return length


def parsesoundfont16():  # parse 16-bit soundfont to find chunks and data lengths
    sampleindex = data.find(samplemagic)  # find sample bank chunk start
    lengthindex = sampleindex + 8  # set the index for where the length bytes are
    length = convertlength(lengthindex)  # convert length to integer
    firstchunkend = sampleindex + 12  # set end of first chunk
    lastchunk = sampleindex + 12 + length # set end of second chunk
    return firstchunkend, lastchunk


def parsesoundfont24():  # parse 24-bit soundfont to find chunks and data lengths
    sampleindex16 = data.find(samplemagic)  # find sample bank chunk start
    lengthindex16 = sampleindex16 + 8  # set the index for where the length bytes are
    length16 = convertlength(lengthindex16)  # convert length to integer
    firstchunkend = sampleindex16 + 12  # set end of first chunk
    sampleindex24 = sampleindex16 + 12 + length16  # set beginning of second chunk
    length24 = length16 // 2  # length of final 8-bits of audio is half the length of the 16-bit audio
    secondchunkend = sampleindex24 + 8  # set end of second chunk
    lastchunk = sampleindex24 + 8 + length24  # set beginning of last chunk
    return firstchunkend, sampleindex24, secondchunkend, lastchunk


def constructsfqheader(sfqheaderbytes, sf2hash, sfqtype):  # create header for non-audio data
    if sfqtype == 1:
        sfqheaderbytes.extend(ofrbitheader16.encode('Latin-1'))  # write ofr 16-bit header
    elif sfqtype == 2:
        sfqheaderbytes.extend(ofrbitheader24.encode('Latin-1'))  # write ofr 24-bit header
    elif sfqtype == 3:
        sfqheaderbytes.extend(flacbitheader16.encode('Latin-1'))  # write flac 16-bit header
    elif sfqtype == 4:
        sfqheaderbytes.extend(flacbitheader24.encode('Latin-1'))  # write flac 24-bit header
    sfqheaderbytes.extend(sf2hash.encode('Latin-1'))  # write sha1 hash
    return sfqheaderbytes


def hashsoundfont(datatohash):  # create a text hexdigest of file
    soundfonthash = hashlib.sha1(datatohash).hexdigest()
    return soundfonthash


def createxz(sfqdata):  # LZMA-compress non-audio data
    if uncompressedheader == False:  # if no -u option, compress the header
        lzmadata = lzma.compress(sfqdata, preset=9)  # compress
    else:  # if -u option, don't compress header
        lzmadata = sfqdata

    lzmabytes = bytearray()
    if uncompressedheader == False:  # if no -u option, encode sfqx
        lzmabytes.extend(sfqx.encode('Latin-1'))  # add compressed file header
    else:  # if -u option, encode sfqu
        lzmabytes.extend(sfqu.encode('Latin-1'))  # add uncompressed file header
    lzmalengthint = len(lzmadata)  # get length of compressed data
    lzmalengthbytes = lzmalengthint.to_bytes(3, byteorder='little')  # convert length to binary
    lzmabytes.extend(lzmalengthbytes)  # append binary length
    lzmabytes.extend(lzmadata)  # append compressed data
    return lzmabytes


def writesfq(lzmabytes):  # write final sfq file
    if ofrcompression == True:  # deal with the different output filenames
        audiofile = open(strippedFilename+'ofr', 'rb')
    else:
        audiofile = open(strippedFilename+'flac', 'rb')
    audio = mmap.mmap(audiofile.fileno(), 0, access=mmap.ACCESS_COPY)
    final = open(strippedFilename+'sfq', 'wb')
    final.write(lzmabytes)  # write compressed non-audio data
    final.close()
    final = open(strippedFilename+'sfq', 'ab')
    final.write(audio)  # write compressed audio data
    final.close()
    audio.close()
    audiofile.close()
    if ofrcompression == True:
        os.remove(strippedFilename+'ofr')  # delete compressed audio temp file
    else:
        os.remove(strippedFilename+'flac')  # delete compressed audio temp file


def checksfqheader(sfqheader):   # find out what type of soundfont the file is
    magicnumber = sfqheader[0:8]  # copy non-audio data header
    if magicnumber == ofrbitheader16:  # if 16-bit ofr return 1
        return 1
    elif magicnumber == ofrbitheader24:  # if 24-bit ofr return 2
        return 2
    elif magicnumber == flacbitheader16:  # if 16-bit flac return 3
        return 3
    elif magicnumber == flacbitheader24:  # if 24-bit flac return 4
        return 4


def ofrcompress(bitdepth):  # compress with ofr
    subprocess.call(["ofr", "--encode", "--preset", ofrpreset, "--raw", "--channelconfig", "MONO", "--sampletype", bitdepth, "--rate", "44100", strippedFilename+"pcm"])


def flaccompress(bitdepth):  # compress with flac
    subprocess.call(["flac", "--best", "--force-raw-format", "--endian=little", "--channels=1", "--bps=" + bitdepth, "--sample-rate=44100", "--sign=signed", strippedFilename+"pcm"])


def ofrdecompress():  # decompress ofr
    subprocess.call(["ofr", "--decode", strippedFilename+"ofr"])  # run optimfrog to decompress audio data
    os.remove(strippedFilename+'ofr')  # delete compressed temp file


def flacdecompress():  # decompress flac
    subprocess.call(["flac", "-d", "--force-raw-format", "--endian=little", "--sign=signed", strippedFilename+"flac"])  # run FLAC to decompress audio data
    os.remove(strippedFilename+'flac')  # delete compressed temp file
    os.rename(strippedFilename+'raw', strippedFilename+'pcm')


def compressed(headertype):  # sfq handler
    checktempfile()
    print("Decompressing " + filename)
    compressedlength = parsecompressed()  # find out length of non-audio bytes
    compressedcopylength = compressedlength + 7  # add length of header
    lzmadata = data[7:compressedcopylength]  # copy non-audio data to memory
    if headertype == 1:  # if header is lzma compressed
        lzmadecompressed = lzma.decompress(lzmadata)  # decompress non-audio data
    elif headertype == 2:  # if header is uncompressed
        lzmadecompressed = lzmadata
    sfqheader = str(lzmadecompressed[0:48], encoding="Latin-1")  # get header of non-audio data
    sfqtype = checksfqheader(sfqheader)  # find out what type of soundfont the file is
    sfqdata = lzmadecompressed[48:]  # copy everything after header to memory
    audiotype16 = False  # set variable for audio bit-depth
    if sfqtype == 1:  # set if 16-bit
        audiotype16 = True
    elif sfqtype == 3:
        audiotype16 = True
    if sfqtype == 1:
        audio = open(strippedFilename+'ofr', 'wb')  # open a temp file
    elif sfqtype == 2:
        audio = open(strippedFilename+'ofr', 'wb')  # open a temp file
    elif sfqtype == 3:
        audio = open(strippedFilename+'flac', 'wb')  # open a temp file
    elif sfqtype == 4:
        audio = open(strippedFilename+'flac', 'wb')  # open a temp file
    audio.write(data[compressedcopylength:])  # copy compressed audio to temp file
    audio.close()  # close temp file
    if sfqtype == 1:
        ofrdecompress()
    elif sfqtype == 2:
        ofrdecompress()
    elif sfqtype == 3:
        flacdecompress()
    elif sfqtype == 4:
        flacdecompress()
    time.sleep(1)  # wait one second
    if audiotype16 == True:  # 16-bit soundfont handler
        print("\nWriting " + strippedFilename + "sf2\n")
        firstchunkend = parsesfq16(sfqdata)  # parse non-audio data to figure out where to write data
        firstchunk = sfqdata[0:firstchunkend]  # copy up to sample chunk
        lastchunk = sfqdata[firstchunkend:]  # copy after sample chunk
        final = open(strippedFilename+'sf2', 'wb')  # open final file
        final.write(firstchunk)  # write first chunk to final file
        final.close()
        final = open(strippedFilename+'sf2', 'ab')
        pcmfile = open(strippedFilename+'pcm', 'rb')  # open temp uncompressed audio file
        pcm = mmap.mmap(pcmfile.fileno(), 0, access=mmap.ACCESS_COPY)
        final.write(pcm)  # write uncompressed audio to final file
        final.close()
        final = open(strippedFilename+'sf2', 'ab')
        final.write(lastchunk)  # write last chunk of non-audio data
        final.close()
        pcm.close()
        pcmfile.close()
        os.remove(strippedFilename+'pcm')  # remove temp uncompressed audio file
    if audiotype16 == False:  # 24-bit soundfont handler
        chunklist = parsesfq24(sfqdata)  # parse non-audio data to figure out where to write data
        firstchunkend = chunklist[0]  # get end of first chunk
        secondchunkend = chunklist[1]  # get end of second chunk
        firstchunk = sfqdata[0:firstchunkend]  # copy up to sample chunk
        secondchunk = sfqdata[firstchunkend:secondchunkend]  # copy between sample chunks
        lastchunk = sfqdata[secondchunkend:]  # copy after sample chunk
        final = open(strippedFilename+'sf2', 'wb')
        final.write(firstchunk)  # write first chunk
        final.close()
        print("\nDecombobulating 24-bit soundfont audio data...\n")
        pcmfile = open(strippedFilename+'pcm', 'rb')
        pcm = mmap.mmap(pcmfile.fileno(), 0, access=mmap.ACCESS_COPY)
        audio = bytearray()  # create bytearray to temporarily hold audio data
        audio.extend(pcm)
        pcm.close()
        pcmfile.close()
        audiolenint = len(audio)  # get length of audio
        final = open(strippedFilename+'sf2', 'ab')
        i = 1
        j = 0
        while i < audiolenint:  # seperate 16-bit audio from 24-bit stream
            index16 = i + 2
            final.write(audio[i:index16])
            i = i + 3
        final.close()
        final = open(strippedFilename+'sf2', 'ab')
        final.write(secondchunk)  # write in-between sample sets data
        final.close()
        final = open(strippedFilename+'sf2', 'ab')
        while j < audiolenint:  # seperate lower 8-bits from 24-bit stream
            index24 = j + 1
            final.write(audio[j:index24])
            j = j + 3
        final.close()
        final = open(strippedFilename+'sf2', 'ab')
        final.write(lastchunk)  # write last chunk
        final.close()
        pcmfile.close()
        os.remove(strippedFilename+'pcm')

    finalcheck = open(strippedFilename+'sf2', 'rb')  # get ready to hash final sf2 file
    finalcheckhandle = mmap.mmap(finalcheck.fileno(), 0, access=mmap.ACCESS_COPY)
    finalhash = sfqheader[8:]  # get hash data
    print("Hashing " + strippedFilename + "sf2\n")
    sf2hash = hashsoundfont(finalcheckhandle)  # hash file
    finalcheckhandle.close()
    finalcheck.close()
    if sf2hash == finalhash:  # check to see if hash matches
        print("Integrity confirmed.\n")
    else:
        print("Something went horribly wrong! The decompressed soundfont is not the same as the original!\n")


def compresssoundfont16():  # compress 16-bit sf2
    checktempfile()
    print("Hashing " + filename + "\n")
    sf2hash = hashsoundfont(data)  # hash original sf2 file

    print("Compressing " + filename)
    soundfontindex = parsesoundfont16()  # parse 16-bit soundfont to find chunks and data lengths

    firstchunkend = soundfontindex[0]  # get end of first chunk
    lastchunk = soundfontindex[1]  # get end of second chunk

    sfqdata = bytearray()  # create bytearray to hold non-audio data header
    if ofrcompression == True:
        sfqdata = constructsfqheader(sfqdata, sf2hash, 1)  # create header for ofr-compressed non-audio data
    else:
        sfqdata = constructsfqheader(sfqdata, sf2hash, 3)  # create header for flac-compressed non-audio data
    sfqdata.extend(data[0:firstchunkend])  # add first chunk
    sfqdata.extend(data[lastchunk:])  # add second chunk

    pcm = open(strippedFilename+'pcm', 'wb')
    pcm.write(data[firstchunkend:lastchunk])  # write temp audio file
    pcm.close()

    lzmabytes = createxz(sfqdata)  # LZMA-compress non-audio data

    if ofrcompression == True:  # is flac compression on?
        ofrcompress("SINT16")  # ofr compress audio data
    else:
        flaccompress("16")  # flac compress audio data

    os.remove(strippedFilename+'pcm')  # delete temp file
    time.sleep(1)
    print("\nWriting " + strippedFilename + "sfq\n")
    writesfq(lzmabytes)  # write final sfq file
    print("Compressed " + filename + "\n")


def compresssoundfont24():  # compress 16-bit sf2
    checktempfile()
    print("Hashing " + filename + "\n")
    sf2hash = hashsoundfont(data)  # hash original sf2 file

    print("Compressing " + filename + "\n")
    soundfont24index = parsesoundfont24()  # parse 24-bit soundfont to find chunks and data lengths
    firstchunkend = soundfont24index[0]  # get chunk starts and ends
    secondchunkstart = soundfont24index[1]
    secondchunkend = soundfont24index[2]
    lastchunkend = soundfont24index[3]

    sfqdata = bytearray()  # create bytearray to hold non-audio data header
    if ofrcompression == True:
        sfqdata = constructsfqheader(sfqdata, sf2hash, 2)  # create header for ofr-compressed non-audio data
    else:
        sfqdata = constructsfqheader(sfqdata, sf2hash, 4)  # create header for flac-compressed non-audio data
    sfqdata.extend(data[0:firstchunkend])  # add first chunk
    sfqdata.extend(data[secondchunkstart:secondchunkend])  # add in-between sample streams chunk
    sfqdata.extend(data[lastchunkend:])  # add last chunk

    print("Combobulating 24-bit soundfont audio data...")
    audio16 = bytearray()  # create bytearray to hold 16-bit stream
    audio16.extend(data[firstchunkend:secondchunkstart])  # copy 16-bit stream
    audio24 = bytearray()  # create bytearray to hold final 8-bits
    audio24.extend(data[secondchunkend:lastchunkend])  # copy final 8-bits

    pcm = open(strippedFilename+'pcm', 'ab')
    audiolenint = len(audio16)  # get length of audio
    i = 0
    j = 0
    while i < audiolenint:  # interleave the 8-bit and 16-bit streams to create a 24-bit stream
        index16 = i + 2
        index24 = j + 1
        pcm.write(audio24[j:index24])
        pcm.write(audio16[i:index16])
        i = i + 2
        j = j + 1
    pcm.close()

    lzmabytes = createxz(sfqdata)  # LZMA-compress non-audio data

    if ofrcompression == True:  # is flac compression on?
        ofrcompress("SINT24")  # ofr compress audio data
    else:
        flaccompress("24")  # flac compress audio data

    os.remove(strippedFilename+'pcm')  # delete temp file
    time.sleep(1)
    print("\nWriting " + strippedFilename + "sfq\n")
    writesfq(lzmabytes)  # write final sfq file
    print("Compressed " + filename + "\n")


# constants used in multiple functions
sfqx = 'sfqx'  # sfq LZMA-compressed header
sfqu = 'sfqu'  # sfq uncompressed header
ofrbitheader16 = 'sfqofr16'   # 16-bit ofr sfq header
ofrbitheader24 = 'sfqofr24'   # 24-bit ofr sfq header
flacbitheader16 = 'sfqfla16'  # 16-bit flac sfq header
flacbitheader24 = 'sfqfla24'  # 24-bit flac sfq header
samplemagic = b'\x73\x64\x74\x61\x73\x6d\x70\x6c'  # 16-bit sample bank magic number

parser = argparse.ArgumentParser(add_help=True, description='This program compresses and decompresses soundfonts using FLAC or OptimFROG.')  # add argument parser

parser.add_argument('-u', action='store_true', help="Turns off compression for the header (see readme for details)") # argument for uncompressed header
parser.add_argument('-o', action='store_true', help="Compresses with OptimFROG (better compression, but less compatible)") # argument for flac compression
parser.add_argument('-l', metavar='level', action='store', default="9", help="Specify OptimFROG compression level (0 - 10, max) (default: 9)")  # add option for ofr preset level
parser.add_argument('FILE', nargs='+', help='Specify sf2 or sfq file to compress/decompress')  # get filename(s)

args = parser.parse_args()  # parse command-line arguments

filenamearg = args.FILE  # set filename
ofrcompression = args.o  # set optimfrog compression
ofrpreset = args.l  # set compression level
uncompressedheader = args.u

for filenameindex in range(len(filenamearg)):  # loop through filenames if wildcard detected
    filename = filenamearg[filenameindex]
    for filename in glob.glob(filename):
        strippedFilename = filename[0:-3]  # name of file stripped of extension
        binaryFile = open(filename, 'rb')  # open file as binary
        data = mmap.mmap(binaryFile.fileno(), 0, access=mmap.ACCESS_COPY)  # create readable file object

        isCompressed = isitcompressed()  # check to see if compressed

        if isCompressed != 0:  # if compressed, run through compressed protocol
            compressed(isCompressed)

        isSounfont = 0
        isSoundfont = isitasoundfont()  # check to see if soundfont file

        if isSoundfont == 1:  # branch to 16-bit and 24-bit soundfont compressors
            compresssoundfont16()
        elif isSoundfont == 2:
            compresssoundfont24()
        data.close()
        binaryFile.close()

input("Press Enter to continue...")