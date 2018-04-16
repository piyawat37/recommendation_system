@echo off

set REL_PATH=..\..\
set ABS_PATH=

rem
pushd %REL_PATH%

rem
set ABS_PATH=%CD%

rem
popd

cd ABS_PATH
cd SSF/movie-recommendation/src/frontend
start cmd.exe /k "npm run dev"


C:
start cmd.exe /k "mongod"