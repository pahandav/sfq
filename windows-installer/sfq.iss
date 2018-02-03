[Setup]
AppName=sfq
AppVersion=1.0.1
DefaultDirName={pf}\sfq
DefaultGroupName=sfq
UninstallDisplayIcon={app}\sfq.exe
Compression=lzma/ultra64
SolidCompression=true
OutputDir=..\dist
; "ArchitecturesAllowed=x64" specifies that Setup cannot run on
; anything but x64.
ArchitecturesAllowed=x64
; "ArchitecturesInstallIn64BitMode=x64" requests that the install be
; done in "64-bit mode" on x64, meaning it should use the native
; 64-bit Program Files directory and the 64-bit view of the registry.
ArchitecturesInstallIn64BitMode=x64
InternalCompressLevel=ultra64
OutputBaseFilename=sfq-1.0.1-setup
VersionInfoVersion=1.0.1
VersionInfoTextVersion=1.0.1
VersionInfoCopyright=2017, pahandav
VersionInfoProductName=sfq
VersionInfoProductVersion=1.0.1
AppCopyright=2018, pahandav
AppVerName=1.0.1
LicenseFile=..\dist\sfq\LICENSE
AppPublisher=pahandav
UninstallDisplayName=sfq

[Files]
Source: ..\dist\sfq\_bz2.pyd; DestDir: {app}
Source: ..\dist\sfq\_hashlib.pyd; DestDir: {app}
Source: ..\dist\sfq\_lzma.pyd; DestDir: {app}
Source: ..\dist\sfq\_socket.pyd; DestDir: {app}
Source: ..\dist\sfq\_ssl.pyd; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-console-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-datetime-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-debug-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-errorhandling-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-file-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-file-l1-2-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-file-l2-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-handle-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-heap-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-interlocked-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-libraryloader-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-localization-l1-2-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-memory-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-namedpipe-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-processenvironment-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-processthreads-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-processthreads-l1-1-1.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-profile-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-rtlsupport-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-string-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-synch-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-synch-l1-2-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-sysinfo-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-timezone-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-core-util-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-crt-conio-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-crt-convert-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-crt-environment-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-crt-filesystem-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-crt-heap-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-crt-locale-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-crt-math-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-crt-process-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-crt-runtime-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-crt-stdio-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-crt-string-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-crt-time-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\api-ms-win-crt-utility-l1-1-0.dll; DestDir: {app}
Source: ..\dist\sfq\base_library.zip; DestDir: {app}
Source: ..\dist\sfq\COPYING.GPL; DestDir: {app}
Source: ..\dist\sfq\COPYING.Xiph; DestDir: {app}
Source: ..\dist\sfq\flac.exe; DestDir: {app}
Source: ..\dist\sfq\LICENSE; DestDir: {app}
Source: ..\dist\sfq\ofr.exe; DestDir: {app}
Source: ..\dist\sfq\pyexpat.pyd; DestDir: {app}
Source: ..\dist\sfq\python36.dll; DestDir: {app}
Source: ..\dist\sfq\README.txt; DestDir: {app}; Flags: isreadme
Source: ..\dist\sfq\select.pyd; DestDir: {app}
Source: ..\dist\sfq\sfq.exe; DestDir: {app}
Source: ..\dist\sfq\sfq.exe.manifest; DestDir: {app}
Source: ..\dist\sfq\ucrtbase.dll; DestDir: {app}
Source: ..\dist\sfq\unicodedata.pyd; DestDir: {app}
Source: ..\dist\sfq\VCRUNTIME140.dll; DestDir: {app}

[Icons]
Name: {group}\sfq; Filename: {app}\sfq.exe
Name: {commondesktop}\sfq (FLAC); Filename: {app}\sfq.exe; Tasks: 
Name: {commondesktop}\sfq (OptimFROG); Filename: {app}\sfq; Parameters: -o

[Tasks]
Name: modifypath; Description: Add application directory to your environmental path (DO NOT UNCHECK!)

[Code]
const
    ModPathName = 'modifypath';
    ModPathType = 'user';

function ModPathDir(): TArrayOfString;
begin
    setArrayLength(Result, 1)
    Result[0] := ExpandConstant('{app}');
end;
#include "modpath.iss"

[Run]
Filename: {sys}\compact.exe; Parameters: /c /s /a /i /exe:lzx *.*; WorkingDir: {app}; Flags: postinstall runhidden runascurrentuser; MinVersion: 0,10.0; Description: Compress application directory with NTFS Compression
Filename: {sys}\compact.exe; Parameters: /c /s /a /i *.*; WorkingDir: {app}; Flags: postinstall runhidden runascurrentuser; Description: Compress application directory with NTFS Compression; OnlyBelowVersion: 0,10.0
