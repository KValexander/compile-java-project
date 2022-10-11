@echo off

set src=src
set bin=bin

if exist %src%/ goto start
else goto end

:end
	echo "CODE FOLDER DOESN'T NOT EXISTS"

:start
	powershell "Get-ChildItem -Path ./%src% -Name -File -s *.* > files.txt"
	powershell "(Get-Content files.txt) -replace '.*\.java', '' | Out-File -encoding ASCII files.txt"

	powershell "Get-ChildItem -Path ./%src% -Name -s *.java > source.txt"
	powershell "(Get-Content source.txt) -replace '^', '.\%src%\' | Out-File -encoding ASCII source.txt"

	rmdir /s /q %bin%
	javac -d %bin% @source.txt

	for /f "useback delims=" %%a IN ("files.txt") DO xcopy "%src%\%%a" "%bin%\%%a*"
	del source.txt
	del files.txt

	cls
	java -classpath ./%bin% com.main.Main
