# Check logC Process Checking is ok or not
# Version 0.01.01
# Initail data 5/10/2023 

# Package to exe = pyinstaller -F ProcessChecking.py
# pyinstaller.exe -F --version-file file_version_info.txt --icon=SGICO.ico ProcessChecking.py

from __future__ import print_function
import os
import shutil
import subprocess
import threading
import function

Version = "0.0.1.3"

if __name__ == '__main__':
	print("Please place LogC.txt and ProcessChecking.exe into the same folder\n")
	print("Function 1: Check verify exist after program.")
	print("Function 2: Check verify time gap.")
	print("Function 3: Check all session time gap.")

	function_str = input("Which function use?\n")

	if function_str.lower() == "version":
		print("Version = " + Version)
		input("Please key enter to leave.")
		quit()

	if function_str == "vRD mode":
		pass

	try:
		function_sel = int(function_str)
	except:
		print("Not a number. ex:1")
		input("Please key enter to leave.")
		quit()

	function_list = [ 1 , 2 , 3]
	Find_Flag = False;

	for x in function_list:
		if function_sel == x:
			Find_Flag = True
			break

	if Find_Flag == False:
		print("Plase select right functon.")
		input("Please key enter to leave.")
		quit()

	if function_sel == 1:
		function.function1_check_vf_after_pg()
	
	if function_sel == 2:
		function.function2_verfy_time_zone()

	if function_sel == 3:
		function.function3_check_all_time_zone()

