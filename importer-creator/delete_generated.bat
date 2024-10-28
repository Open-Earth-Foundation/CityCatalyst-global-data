@ECHO OFF
ECHO Deleting files in the generated folder and its subfolders...
FOR /R "generated" %%G IN (*.*) DO DEL /Q "%%G"
ECHO Files deleted.