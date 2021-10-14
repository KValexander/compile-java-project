import shutil
import os
import re

from tkinter import *

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
	"startclass": "Main.class",
	"runbat": "run.bat",
	"copyassets": "true"
}

# Getting configurations from a file
if os.path.exists("compile_config.txt"):
	f = open("compile_config.txt", "r")
	for line in f:
		line = line.replace(" ", "").split("=");
		config[line[0]] = line[1].rstrip();
	f.close()

# Entries
entries = {
	"javapath": "Java dir: ",
	"classpath": "Class dir: ",
	"sourcetxt": "Source txt: ",
	"compilebat": "Compile bat: ",
	"startclass": "Start class: ",
	"runbat": "Run bat: ",
	"copyassets": "Copy assets: "
}

# Setting configurations
def setting_configurations():
	for key, val in entries.items():
		if(entries[key].get() != ""): config[key] = entries[key].get()

	# Overwrite config file
	f = open("compile_config.txt", "w+")
	for key, val in config.items():
		f.write(key + " = " + val + "\n")
	f.close()

	# Call start processing
	start_processing()

# GUI
def tkinter_interface():
	global entries

	# Window
	window = Tk()
	window.title("Java compilation automator")
	window.resizable(width=False, height=False)
	window.geometry("400x300")

	# Labels and Entries
	i = 0
	for key, val in entries.items():
		entries[key] = create_field(window, val, 30, 0, i)
		entries[key].insert(0, config[key])
		i += 2

	# Button
	button = Button(window, text="Run", background="#888", foreground="#eee", padx="20", pady="0", font="20", command=setting_configurations)
	button.grid(column=2,row=0, padx=20)

	# Mainloop
	window.mainloop()

# Create field
def create_field(win, text, width, c, r):
	label = Label(win, text=text)
	label.grid(column=c, row=r, pady=10, padx=10)
	txt = Entry(win, width=width)
	txt.grid(column=c+1, row=r)
	return txt

# Concatenating paths to java files
def java_dir_processing(path):
	global concat, assets
	concat = ""
	assets.clear()
	ld = os.listdir(path)
	for file in ld:
		if re.search(r"\.java", file):
			concat += "./" + path + "/" + file + "\n"
		elif os.path.isdir(path + "/" + file): java_dir_processing(path + "/" + file)
		else: assets.append(path + "/" + file)

# Getting the path to the starting class
def class_dir_processing(path):
	global startclass
	startclass = ""
	if(not os.path.exists(path)): return False;
	ld = os.listdir(path)
	for file in ld:
		if re.search(config["startclass"], file):
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

# Start programm
def start_processing():

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

	# Checking for compilation success
	# and getting the path to the starting class 
	if(class_dir_processing(config["classpath"]) == False):
		return print("\nJCA message: Compilation error")
	if(not startclass):
		return print("\nJCA message: Startup error")
	else: 
 		print("JCA message: Compilation is successful")

	# Call ap
	if(config["copyassets"] == "true"): assets_processing()

	# Creating an interpretation file
	create_file(config["runbat"], "java -classpath ./" + config["classpath"] + " " + startclass)

	# Running the code
	os.system(config["runbat"])

	# Removing intermediate files
	os.remove(config["runbat"])


# Call GUI
tkinter_interface()