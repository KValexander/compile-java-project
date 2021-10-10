import os
import re

# Config
concat = ""
javapath = "java"
classpath = "class"
sourcetxt = "source.txt"
compilebat = "compile.bat"
startfile = "Main.class"
startclass = ""
runbat = "run.bat"

# Concatenating paths to java files
def java_dir_processing(path):
	global concat
	ld = os.listdir(path)
	for file in ld:
		if re.search(r"\.java", file):
			concat += "./" + path + "/" + file + "\n"
		elif os.path.isdir(path + "/" + file): java_dir_processing(path + "/" + file)

# Getting the path to the starting class
def class_dir_processing(path):
	global startclass
	ld = os.listdir(path)
	for file in ld:
		if re.search(startfile, file):
			startclass = path + "/" + re.split(r"\.", file)[0]
			startclass = re.sub(r"/", ".", startclass.replace(classpath+"/", ""))
			return;
		elif os.path.isdir(path + "/" + file): class_dir_processing(path + "/" + file)

# Call jdp
java_dir_processing(javapath)
print(concat);

# Create file with paths 
f = open(sourcetxt, "w+")
f.write(concat)
f.close()

# Create file with compilation command
f = open(compilebat, "w+")
f.write("rd /s "+ classpath +" \n")
f.write("javac -d " + classpath + " @" + sourcetxt + "\n")
f.close()

# Compilation activation
os.system(compilebat)
# Removing intermediate files
os.remove(compilebat)
os.remove(sourcetxt)

# Call cdp
class_dir_processing(classpath)

# Creating an interpretation file
f = open(runbat, "w+")
f.write("java -classpath ./" + classpath + " " + startclass + "\npause")
f.close()

# Running the code
os.system(runbat)

# Removing intermediate files
os.remove(runbat)