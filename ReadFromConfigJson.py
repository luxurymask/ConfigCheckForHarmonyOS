import os
import zipfile
import sys
import json
from pyecharts.components import Image
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
from pyecharts.charts import Page

def get_config_file(file_path):
	unzip_file(file_path)
	config_dictionary = {}
	hap_files_dir = file_path + "_files"
	for root,dirs,files in os.walk(hap_files_dir):
		for file in files:
			if file.endswith(".hap"):
				unzip_file(os.path.join(root,file))
				config_file_path = os.path.join(os.path.join(root, file) + "_files", "config.json")
				load_dict = {}
				with open(config_file_path, "r") as load_config_file:
					load_dict = json.load(load_config_file)
				config_dictionary[file] = load_dict
			elif file.endswith(".res"):
				unzip_file(os.path.join(root,file))
				entrycard_path = os.path.join(os.path.join(root, file) + "_files", "EntryCard")
				print("111" + entrycard_path)
				for snap_folder_name in os.listdir(entrycard_path):
					print(snap_folder_name)
					config_dictionary["EntryCard-" + snap_folder_name] = {}
					for snap_root, snap_dirs, snap_files in os.walk(os.path.join(entrycard_path, snap_folder_name)):
						for snap_file in snap_files:
							print(os.path.join(snap_root, snap_file))
							config_dictionary["EntryCard-" + snap_folder_name][snap_file] = os.path.join(snap_root, snap_file)

	# print(config_dictionary)
	show_data_in_pyecharts(config_dictionary)

def show_data_in_pyecharts(config_dictionary):
	page = Page()
	pth = os.path.join(os.path.split(os.path.realpath(__file__))[0],"zsdflkasj_page.html")
	app_apiversion_compatible = None

	app_table = Table()
	app_table_headers = ["app_apiversion_compatible", "app_apiversion_target", "app_version_code", "app_version_name", "app_vendor", "app_bundlename"]

	module_table = Table()
	module_table_headers = ["hap_name", "module_mainability", "module_distro_moduletype", "module_package"]
	module_table_headers.append("module_ability_form_name")
	module_table_headers.append("module_ability_form_isdefault")
	module_table_headers.append("module_ability_form_defaultdemension")
	module_table_headers.append("module_ability_form_description")
	module_table_rows = []

	for key in config_dictionary:
		module_ability_icon = ""
		module_ability_form_name = ""

		if key.startswith("EntryCard-"):
			pth = os.path.join(os.path.split(os.path.realpath(__file__))[0],"app_image.html")
			snapshot_imgs = config_dictionary[key]
			for snapshot_img in snapshot_imgs:
				if snapshot_img.startswith(module_ability_form_name):
					print("#####" + snapshot_img + module_ability_form_name)
					img_path = snapshot_imgs[snapshot_img];
					print(key + ": " + img_path)
					image = Image()
					img_src = (img_path)
					image.add(
						src = img_src,
						style_opts={"width": "600px", "height": "600px", "style": "margin-top: 20px"}
					)
					image.set_global_opts(
    					title_opts=ComponentTitleOpts(title=key, subtitle=img_path)
					)
					# page.add(image)
					image.render(pth)
		else:
			pth = os.path.join(os.path.split(os.path.realpath(__file__))[0],"app_table.html")
			hap_name = key
			hap_config_json = config_dictionary[hap_name]

			if app_apiversion_compatible == None:
				app_apiversion_compatible = hap_config_json['app']['apiVersion']['compatible']
				app_apiversion_target = hap_config_json['app']['apiVersion']['target']
				app_version_code = hap_config_json['app']['version']['code']
				app_version_name = hap_config_json['app']['version']['name']
				app_vendor = hap_config_json['app']['vendor']
				app_bundlename = hap_config_json['app']['bundleName']

				app_table_rows = [[app_apiversion_compatible, app_apiversion_target, app_version_code, app_version_name, app_vendor, app_bundlename]]
				app_table.add(app_table_headers, app_table_rows)
				app_table.set_global_opts(
    				title_opts=ComponentTitleOpts(title="app基础信息", subtitle="")
				)
				page.add(app_table)

			else:
				if app_apiversion_compatible != hap_config_json['app']['apiVersion']['compatible']:
					table_subtitle.append("app info not compatible: app_apiversion_compatible-" + hap_config_json['app']['apiVersion']['compatible'] + "\n")
				if app_apiversion_target != hap_config_json['app']['apiVersion']['target']:
					table_subtitle.append("app info not compatible: app_apiversion_target-" + hap_config_json['app']['apiVersion']['target'] + "\n")
				if app_version_code != hap_config_json['app']['version']['code']:
					table_subtitle.append("app info not compatible: app_version_code-" + hap_config_json['app']['version']['code'] + "\n")
				if app_version_name != hap_config_json['app']['version']['name']:
					table_subtitle.append("app info not compatible: app_version_name-" + hap_config_json['app']['version']['name'] + "\n")
				if app_vendor != hap_config_json['app']['vendor']:
					table_subtitle.append("app info not compatible: app_vendor-" + hap_config_json['app']['vendor'] + "\n")
				if app_bundlename != hap_config_json['app']['bundleName']:
					table_subtitle.append("app info not compatible: app_bundlename-" + hap_config_json['app']['bundleName'] + "\n")
			# print(app_apiversion_compatible)
			# print(app_apiversion_target)
			# print(app_version_code)
			# print(app_version_name)
			# print(app_vendor)
			# print(app_bundlename)
	
			module_mainability = hap_config_json['module']['mainAbility'] if 'mainAbility' in hap_config_json['module'] else ""
			module_distro_moduletype = hap_config_json['module']['distro']['moduleType']
			module_package = hap_config_json['module']['package']

			current_row = [hap_name, module_mainability, module_distro_moduletype, module_package]
	
			module_abilities = hap_config_json['module']['abilities'];
			for module_ability in module_abilities:
				module_ability_name = module_ability['name']
				if 'forms' in module_ability and module_ability_name == module_mainability:
					module_ability_icon = module_ability['icon']
					module_ability_forms = module_ability['forms']
					for module_ability_form in module_ability_forms:
						module_ability_form_isdefault = module_ability_form['isDefault'] if 'isDefault' in module_ability_form else ""
						if module_ability_form_isdefault == "":
							continue
						module_ability_form_name = module_ability_form['name']
						module_ability_form_defaultdemension = module_ability_form['defaultDimension']
						module_ability_form_description = module_ability_form['description']
						current_row.append(module_ability_form_name)
						current_row.append(module_ability_form_isdefault)
						current_row.append(module_ability_form_defaultdemension)
						current_row.append(module_ability_form_description)
			if len(current_row) != len(module_table_headers):
				current_row.append("")
				current_row.append("")
				current_row.append("")
				current_row.append("")
			module_table_rows.append(current_row)
			module_table.add(module_table_headers, module_table_rows)

			module_table.set_global_opts(
    			title_opts=ComponentTitleOpts(title="hap基础信息", subtitle="")
			)
	page.add(module_table)
	# app_table.render(pth)
	page.render(pth)


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

