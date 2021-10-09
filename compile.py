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

# Concat java files path
def java_dir_processing(path):
	global concat
	ld = os.listdir(path)
	for file in ld:
		if re.search(r"\.", file):
			concat += "./" + path + "/" + file + "\n"
		else: java_dir_processing(path + "/" + file)

# Get start class path
def class_dir_processing(path):
	global startclass
	ld = os.listdir(path)
	for file in ld:
		if re.search(r"\.", file):
			if(file == startfile):
				startclass = path + "/" + re.split(r"\.", file)[0]
				startclass = re.sub(r"/", ".", startclass.replace(classpath+"/", ""))
				return;
		else: class_dir_processing(path + "/" + file)

# Call jdp
java_dir_processing(javapath)

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