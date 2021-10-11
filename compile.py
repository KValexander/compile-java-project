import shutil
import os
import re

# Config
concat = ""
assets = []
javapath = "java"
classpath = "class"
sourcetxt = "source.txt"
compilebat = "compile.bat"
startfile = "Main.class"
startclass = ""
runbat = "run.bat"

# Concatenating paths to java files
def java_dir_processing(path):
	global concat, assets
	ld = os.listdir(path)
	for file in ld:
		if re.search(r"\.java", file):
			concat += "./" + path + "/" + file + "\n"
		elif os.path.isdir(path + "/" + file): java_dir_processing(path + "/" + file)
		else: assets.append(path + "/" + file)

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

# Copy assets
def assets_processing():
	global assets
	for asset in assets:
		topath = re.sub(r"\/\w*\.\w*", "/", asset.replace(javapath, classpath, 1))
		if not os.path.exists(topath):
			shutil.copytree(topath.replace(classpath, javapath),topath)
			for filename in os.listdir(topath):
				fullpath = topath + filename
				if os.path.isfile(fullpath): os.unlink(fullpath)
				elif os.path.isdir(fullpath): shutil.rmtree(fullpath)
		shutil.copy(asset, topath)

# File creation
def create_file(name, content):
	f = open(name, "w+")
	f.write(content)
	f.close()

# Call jdp
java_dir_processing(javapath)
print(concat);
print(assets);

# Create file with paths
create_file(sourcetxt, concat)

# Delete class folder if it exists
if os.path.exists(classpath): shutil.rmtree(classpath)

# Create file with compilation command
create_file(compilebat, "javac -d " + classpath + " @" + sourcetxt + "\n")

# Compilation activation
os.system(compilebat)
# Removing intermediate files
os.remove(compilebat)
os.remove(sourcetxt)

# Call ap
assets_processing()
# Call cdp
class_dir_processing(classpath)

# Creating an interpretation file
create_file(runbat, "java -classpath ./" + classpath + " " + startclass + "\npause")

# Running the code
os.system(runbat)

# Removing intermediate files
os.remove(runbat)