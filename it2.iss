; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{8774AC69-8B0F-4C8A-8BE9-8CCF0A7F4F34}
AppName=LFUCG Interface Tool
AppVersion=1.0
;AppVerName=LFUCG Interface Tool 1.0
AppPublisher=C2Logix, Inc.
AppPublisherURL=http://www.c2logix.com/
AppSupportURL=http://www.c2logix.com/
AppUpdatesURL=http://www.c2logix.com/
DefaultDirName={pf}\LFUCG Interface Tool
DefaultGroupName=LFUCG Interface Tool
OutputDir=C:\Pyfiles
OutputBaseFilename=LFUCG Tool Setup
SetupIconFile=C:\Python25\dist\images\C2icon.ico
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Python25\dist\Interface_Tool2.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Python25\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\LFUCG Interface Tool"; Filename: "{app}\Interface_Tool2.exe"
Name: "{group}\{cm:UninstallProgram,LFUCG Interface Tool}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\LFUCG Interface Tool"; Filename: "{app}\Interface_Tool2.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\Interface_Tool2.exe"; Description: "{cm:LaunchProgram,LFUCG Interface Tool}"; Flags: nowait postinstall skipifsilent

