@echo off

set src=src
set bin=bin
set class=com.main.Main

if not exist %src%/ goto nf else goto start

:start
	powershell "Get-ChildItem -Path ./%src% -Name -File -s *.* > files.txt"
	powershell "(Get-Content files.txt) -replace '.*\.java', '' | Out-File -encoding ASCII files.txt"

	powershell "Get-ChildItem -Path ./%src% -Name -s *.java > source.txt"
	powershell "(Get-Content source.txt) -replace '^', '.\%src%\' | Out-File -encoding ASCII source.txt"

	rmdir /s /q %bin%
	javac -d %bin% @source.txt
	if not exist %bin%/ goto error

	for /f "useback delims=" %%a IN ("files.txt") DO xcopy "%src%\%%a" "%bin%\%%a*"
	del source.txt files.txt

	cls
	java -classpath ./%bin% %class%

	goto end
	
:nf
	echo "CODE FOLDER DOESN'T NOT EXISTS"
	goto end

:error
	del source.txt files.txt
	echo "COMPILATION ERROR"
	goto end

:end
	pause