import os
import zipfile
import sys
import json

config_dictionary = {}

def get_config_file(file_path):
	unzip_file(file_path)
	hap_files_dir = file_path + "_files"
	for root,dirs,files in os.walk(hap_files_dir):
		for file in files:
			if file.endswith(".hap"):
				unzip_file(os.path.join(root,file))
				config_file_path = os.path.join(os.path.join(root, file) + "_files", "config.json")
				print(config_file_path)
				load_dict = {}
				with open(config_file_path, "r") as load_config_file:
					load_dict = json.load(load_config_file)
				config_dictionary[file] = load_dict
				print(config_dictionary)


def unzip_file(file_path):
	zip_file = zipfile.ZipFile(file_path)
	if os.path.isdir(file_path + "_files"):
		pass
	else:
		os.mkdir(file_path + "_files")
	for names in zip_file.namelist():
		zip_file.extract(names, file_path + "_files/")
	zip_file.close()

argv_lenth = len(sys.argv)
file_path = ""
if argv_lenth <= 1:
	pass
else:
	file_path = sys.argv[1]
	get_config_file(file_path)

