# Check logC Process Checking is ok or not
# Version 0.01.01
# Initail data 5/10/2023 

# Package to exe = pyinstaller -F ProcessChecking.py
# pyinstaller.exe -F --version-file file_version_info.txt test.py

from __future__ import print_function
import os
import shutil
import subprocess
import threading


Version = "0.01.01"

print("copyright © System General Corporation. all rights reserved. Don't fwd to other people.\n")
print("Function 1: Check verify after program")
print("Function 2: Check verify time zone")

function = input("Which function use? ")

if function.lower() == "version":
	print("Version = " + Version)
	input("Please key enter to leave.")
	quit()




SiteNumber_str = input("What site do you want to check? ") # 使用者輸入的東西都算是字串

if SiteNumber_str.lower() == "version":
	print("Version = " + Version)
	input("Please key enter to leave.")
	quit()

try:
	SiteNumber = int(SiteNumber_str)
except:
	print("Plase enter site number. ex: 3.")
	input("Please key enter to leave.")
	quit()

#######################################
#######################################
#######################################

try:
	f = open('LogC.txt','r')
except:
	print("LogC.txt not exist. Please put LogC.txt and ProcessChecking.exe into the same folder.")
	quit()

line = f.readlines()

def ParseSite( line_in_log, site):
	if ("Site#" + str(site) + " ID checking...") in line_in_log:
		return "get_ID_message"

	if ("Site#" + str(site) + " Programming...") in line_in_log:
		return "get_prog_message"
    
	if ("Site#" + str(site) + " Verifying...") in line_in_log:
		return "get_verify_message"

	if ("Site#"+ str(site) + " [")in line_in_log:
		if "Program Pass!" in line_in_log:
			return "Program Pass!"		

	return "none"

Process_ID = False
Process_P  = False
Process_V  = False
Process_Pass  = False
Site_err_flag = False

ID_Count = 0
PG_Count = 0
VF_Count = 0

line_count = 1

for x in line:
	if "get_ID_message" == ParseSite(x, SiteNumber):
		Process_ID = True
		ID_Count = ID_Count + 1

	if "get_prog_message" == ParseSite(x, SiteNumber):
		Process_P = True
		PG_Count = PG_Count + 1

	if "get_verify_message" == ParseSite(x, SiteNumber):
		Process_V = True
		VF_Count = VF_Count + 1

	if Process_ID:
		if "Program Pass!" == ParseSite(x, SiteNumber):
			Process_Pass = True

	if Process_ID and Process_P and Process_V and Process_Pass:
		ID_Count = 0
		PG_Count = 0
		VF_Count = 0
		Process_ID = False
		Process_P = False
		Process_V = False
		Process_Pass = False

	if ID_Count == 2:
		print("Process wrong. ID repeat. Please check line %d." %(line_count))
		break

	if PG_Count == 2:
		print("Process wrong. Verify repeat. Please check line %d." %(line_count))
		break

	if PG_Count == 2:
		print("Process wrong. Program repeat. Please check line %d." %(line_count))
		ID_Count = 0
		PG_Count = 0
		VF_Count = 0
		Process_ID = False
		Process_P = False
		Process_V = False
		Process_Pass = False
		Site_err_flag = True
		break

	if Process_ID and Process_P and not Process_V and Process_Pass:
		print("Process wrong. Verify not happen. Please check line %d." %(line_count))
		ID_Count = 0
		PG_Count = 0
		VF_Count = 0
		Process_ID = False
		Process_P = False
		Process_V = False
		Process_Pass = False
		Site_err_flag = True
		pass

	line_count = line_count + 1


f.close()

if not Site_err_flag:
	print("\nSite#%d is OK" %(SiteNumber))

input("Please key enter to leave.")