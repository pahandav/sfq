sfq Version 1.0.0

This program compresses and decompresses Soundfont (.sf2) files. It does so through the use of external FLAC or OptimFROG encoders. It is written in Python for cross-platform compatibility, and should both get better compression than SFArk and SFPACK, but should also not corrupt your files like SFPack does.


Requirements:

64-bit version of Windows, Linux, Mac OS X (confirmed to not work on 10.6 or below), or FreeBSD (other systems supported only for FLAC-encoded files)

64-bit Python 3.3 or above (it will work on some files with 32-bit Python, but crashes with larger ones)

Executable encoders for FLAC and OptimFROG in your system's environment path.


Installation:

On Windows, use the setup installer release on the Github repo. This will install everything you need to run it on a command line.

For other systems, download the source code from the Github repo, and place sfq.py into your system path.
Obtain the appropriate FLAC binary from http://xiph.org/flac/, and the appropriate OptimFROG binary from http://losslessaudio.org/, and install them to your environment path. Use of a package manager to install these is highly recommended if possible.

Building:

This program is built for Windows with pyinstaller. If you wish to build your own copy, modify the .spec file to point to where you have the sfq.py, flac.exe, and ofr.exe, and run pyinstaller against the .spec script. Inno Setup scripts are also provided in the windows-installer directory. Compile the installer after building the program.


Why this program exists:

Soundfonts are a combination of PCM audio and non-audio data. The optimal way to compress a soundfont is to compress the audio data with a lossless audio compressor, and the non-audio data with a general compressor.

There are other programs that can do this, namely SFPACK and SFArk. SFPACK gets extremely high compression ratios, but is Windows-only, and usually corrupts the files. SFArk doesn't corrupt files, but is also Windows-only (even though there is an open-source decompressor available.)

sfq is designed to leverage better lossless audio compressors that can be run on a cross-platform basis to ensure that compressed Soundfonts can be used on any major operating system. FLAC is provided as an encoder format for maximum compatibility. OptimFROG is provided to allow better compression ratios than is possible with SFPACK and SFArk, at the cost of only being able to decompress the sfq file on a smaller number of operating systems.

For more information and comparisons, please watch this video: https://youtu.be/UsfDv2NqSd0


Usage:

To decompress files, pass a sfq compressed file to the program.

To compress files, pass a sf2 Soundfont to the program.

No command line switches are needed to compress with the default setting of FLAC with the best preset. sfq will only compress FLAC with the best preset. For OptimFROG, you can specify the compression level. WARNING: DO NOT FURTHER COMPRESS sfq FILES COMPRESSED WITH OPTIMFROG LEVEL 2 OR GREATER. THEY WILL GET BIGGER. If you need to add them to an archive, use the "Store" compression option.

Command Line Switches:

-o: This sets the audio compressor to OptimFROG. It gets better compression than FLAC, but is slower, and can only be decompressed on certain operating systems.

-l (level number):  This switch specifies the OptimFROG compression level to use. This is any number between 0 and 10, and max. Levels 0 and 1 are not recommended, as they don't compress very well for the time taken. Levels 10 and max are also not recommended, as they are extremely slow for the extra compression they obtain over level 9. If you do want the extra compression, level max is the recommended level, as it takes the same amount of time to decompress as level 10.

-u: This outputs the non-audio data in the soundfont as uncompressed data, rather than the default of LZMA compressed data. This could be useful if the sfq file will be read by a program that cannot decompress LZMA data. This option is currently pointless, but is in here for future use.


Licensing:

sfq.py and sfq.iss are licensed under an MIT license, so it can be used as a module in other programs, or so it can be reimplemented in other programming languages.

FLAC is Copyright (c) 2004-2009 Josh Coalson, 2011-2017 Xiph.Org Foundation and licensed under the GNU General Public License. Source code is available at http://downloads.xiph.org/releases/flac/

OptimFROG is Copyright © 1996-2017, Florin Ghido, and is redistributed unmodified with the Windows Installer under license. Additional licensing information available here: http://losslessaudio.org/License.php

modpath.iss is licensed under the LGPL, version 3: http://www.gnu.org/licenses/lgpl.html


Acknowledgments:

Josh Coalson and all the people who wrote FLAC.
Florin Ghido for writing the best lossless audio compressor out there.
Jared Breland for his modpath.iss script for Inno Setup: http://www.legroom.net/software


TODO:

Write a GUI.
Fix it so it works properly on 32-bit Python (don't count on me doing this).


Visit my YouTube channel at: http://www.youtube.com/channel/UCVY8W2RJUIzfqNYoGL83AnQ
Visit my Twitter at: http://twitter.com/pahandav