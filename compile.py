import shutil
import os
import re

# Storage
concat = ""
assets = []
startclass = ""
# Static config
config = {
	"javapath": "java",
	"classpath": "class",
	"sourcetxt": "source.txt",
	"compilebat": "compile.bat",
	"startfile": "Main.class",
	"runbat": "run.bat",
}

# Getting configurations from a file
if os.path.exists("compile_config.txt"):
	f = open("compile_config.txt", "r")
	for line in f:
		line = line.replace(" ", "").split("=");
		config[line[0]] = re.sub(r"\"", "", re.findall(r"\".*\"",line[1])[0]);
	f.close()

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
		if re.search(config["startfile"], file):
			startclass = path + "/" + re.split(r"\.", file)[0]
			startclass = re.sub(r"/", ".", startclass.replace(config["classpath"]+"/", ""))
			return;
		elif os.path.isdir(path + "/" + file): class_dir_processing(path + "/" + file)

# Copy assets
def assets_processing():
	global assets
	for asset in assets:
		topath = re.sub(r"\/\w*\.\w*", "/", asset.replace(config["javapath"], config["classpath"], 1))
		if not os.path.exists(topath):
			shutil.copytree(topath.replace(config["classpath"], config["javapath"]),topath)
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
java_dir_processing(config["javapath"])

# Create file with paths
create_file(config["sourcetxt"], concat)

# Delete class folder if it exists
if os.path.exists(config["classpath"]): shutil.rmtree(config["classpath"])

# Create file with compilation command
create_file(config["compilebat"], "javac -d " + config["classpath"] + " @" + config["sourcetxt"] + "\n")

# Compilation activation
os.system(config["compilebat"])
# Removing intermediate files
os.remove(config["compilebat"])
os.remove(config["sourcetxt"])

# Call ap
assets_processing()
# Call cdp
class_dir_processing(config["classpath"])

# Creating an interpretation file
create_file(config["runbat"], "java -classpath ./" + config["classpath"] + " " + startclass + "\npause")

# Running the code
os.system(config["runbat"])

# Removing intermediate files
os.remove(config["runbat"])