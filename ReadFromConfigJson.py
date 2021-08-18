import os
import zipfile
import sys
import json
from pyecharts.components import Image
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts

def get_config_file(file_path):
	unzip_file(file_path)
	config_dictionary = {}
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
			elif file.endswith(".res"):
				unzip_file(os.path.join(root,file))
				entrycard_path = os.path.join(root, file) + "_files"
				print(entrycard_path)
				for snap_root, snap_dirs, snap_folders in os.walk(entrycard_path):
					print(snap_root)
					print(snap_dirs)
					print(snap_folders)
					for snap_folder in snap_folders:
						print("##:" + snap_folder)

	show_data_in_pyecharts(config_dictionary)

def show_data_in_pyecharts(config_dictionary):
	for hap_name in config_dictionary:
		print(hap_name)
		hap_config_json = config_dictionary[hap_name]
		app_apiversion_compatible = hap_config_json['app']['apiVersion']['compatible']
		app_apiversion_target = hap_config_json['app']['apiVersion']['target']
		app_version_code = hap_config_json['app']['version']['code']
		app_version_name = hap_config_json['app']['version']['name']
		app_vendor = hap_config_json['app']['vendor']
		app_bundlename = hap_config_json['app']['bundleName']
		print(app_apiversion_compatible)
		print(app_apiversion_target)
		print(app_version_code)
		print(app_version_name)
		print(app_vendor)
		print(app_bundlename)

		module_mainability = hap_config_json['module']['mainAbility']
		module_distro_moduletype = hap_config_json['module']['distro']['moduleType']
		module_package = hap_config_json['module']['package']

		app_table = Table()
		app_table_headers = ["hap_name", "app_apiversion_compatible", "app_apiversion_target", "app_version_code", "app_version_name", "app_vendor", "app_bundlename"]
		app_table_rows = []
		current_row = [hap_name, app_apiversion_compatible, app_apiversion_target, app_version_code, app_version_name, app_vendor, app_bundlename]

		app_table_rows.append(current_row)

		app_table.add(app_table_headers, app_table_rows)
		app_table.set_global_opts(
    		title_opts=ComponentTitleOpts(title="Table-基本示例", subtitle="我是副标题支持换行哦")
		)
		pth = os.path.join(os.path.split(os.path.realpath(__file__))[0],"app_table.html")
		print(pth)
		app_table.render(pth)



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

