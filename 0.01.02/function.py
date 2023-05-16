from __future__ import print_function

def Check_time(time_str):
	Second = int(time_str[6:8])
	Minute = int(time_str[3:5])
	Hour = int(time_str[0:2])
	return Hour*60*60 + Minute*60 + Second #return unit is second


def ParseSite( line_in_log, site):
	if ("Site#" + str(site) + " ID checking...") in line_in_log:
		#print("ID " + str(Check_time(line_in_log)))
		return "get_ID_message", Check_time(line_in_log)

	if ("Site#" + str(site) + " Programming...") in line_in_log:
		return "get_prog_message", Check_time(line_in_log)
    
	if ("Site#" + str(site) + " Verifying...") in line_in_log:
		return "get_verify_message" , Check_time(line_in_log)
		
	if ("Site#"+ str(site)) in line_in_log:
		if "Program Pass!" in line_in_log:
			#print("PP " + str(Check_time(line_in_log)))
			return "Program_Process_Done"	, Check_time(line_in_log)

		if "Program fail" in line_in_log:
			return "Program_Process_Done"	, Check_time(line_in_log)

		if "Verify Pass!" in line_in_log:
			return "Verify_Process_Done"	, Check_time(line_in_log)

		if "Verify fail" in line_in_log:
			return "Verify_Process_Done"	, Check_time(line_in_log)

	return "none" , 0
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------

def function1_check_vf_after_pg():

	SiteNumber_str = input("What site do you want to check?\n") # 使用者輸入的東西都算是字串

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

######################################################################################
######################################################################################
######################################################################################

	try:
		f = open('LogC.txt','r')
	except:
		print("LogC.txt not exist. Please put LogC.txt and ProcessChecking.exe into the same folder.")
		quit()

	line = f.readlines()
######################################################################################
######################################################################################
######################################################################################
######################################################################################
######################################################################################
######################################################################################
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
		Parse_Message, Message_time = ParseSite(x, SiteNumber)

		if "get_ID_message" == Parse_Message:
			Process_ID = True
			ID_Count = ID_Count + 1

		if "get_prog_message" == Parse_Message:
			Process_P = True
			PG_Count = PG_Count + 1

		if "get_verify_message" == Parse_Message:
			Process_V = True
			VF_Count = VF_Count + 1

		if Process_ID:
			if "Verify_Process_Done" == Parse_Message:
				Process_Pass = True

			if "Program_Process_Done" == Parse_Message:
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

		if Process_V == 2:
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
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------

def function2_verfy_time_zone():

	SiteNumber_str = input("What site do you want to check?\n")

	try:
		SiteNumber = int(SiteNumber_str)
	except:
		print("Plase enter site number. ex: 3.")
		input("Please key enter to leave.")
		quit()

	Timing_Allow_L_str = input("How much time do programmer verification at least(minimum)? Please input second. ex: 5\n") 

	try:
		Timing_Allow_L = int(Timing_Allow_L_str)
	except:
		print("Plase enter second. ex: 5.")
		input("Please key enter to leave.")
		quit()


	Timing_Allow_H_str = input("How much time do programmer verification maximum? Please input second. ex: 5\n") 

	try:
		Timing_Allow_H = int(Timing_Allow_H_str)
	except:
		print("Plase enter second. ex: 5.")
		input("Please key enter to leave.")
		quit()


	if Timing_Allow_H < Timing_Allow_L:
		print("Maximum(%d) second less minimum(%d) second. Please restart." %(Timing_Allow_H, Timing_Allow_L))
		input("Please key enter to leave.")
		quit()

######################################################################################
######################################################################################
######################################################################################

	try:
		f = open('LogC.txt','r')
	except:
		print("LogC.txt not exist. Please put LogC.txt and ProcessChecking.exe into the same folder.")
		quit()

	line = f.readlines()


	Process_ID = False
	Process_V  = False
	Process_Pass  = False
	Site_err_flag = False

	ID_Count = 0
	VF_Count = 0

	line_count = 1

	for x in line:
		Parse_Message, Message_time = ParseSite(x, SiteNumber)

		if "get_ID_message" == Parse_Message:
			Process_ID = True
			ID_Time = Message_time
			ID_Count = ID_Count + 1

		if "get_verify_message" == Parse_Message:
			Process_V = True
			VF_Time = Message_time
			VF_Count = VF_Count + 1

		if Process_ID:
			if "Verify_Process_Done" == Parse_Message:
				Pass_time = Message_time
				Process_Pass = True

		if Process_ID and Process_V and Process_Pass:
			ID_Count = 0
			VF_Count = 0
			Process_ID = False
			Process_V = False
			Process_Pass = False
			####################
			#Check time zone
			####################
			
			#Step1: Checking cross day
			if (Pass_time - VF_Time) < 0:
				Pass_time  = Pass_time + 86400

			#Step2: Checking time zoe over seting
			if (Pass_time - VF_Time) > Timing_Allow_H:
				print("Process wrong. Verify time is too long. Spent %d second. Please check line %d." %( Pass_time - VF_Time , line_count))
				Site_err_flag = True

			if (Pass_time - VF_Time) < Timing_Allow_L:
				print("Process wrong. Verify time is too short. Spent %d second. Please check line %d." %( Pass_time - VF_Time , line_count))
				Site_err_flag = True


		if Process_ID and not Process_V and Process_Pass:
			print("Process wrong. Verify not happen. Please check line %d." %(line_count))
			ID_Count = 0
			VF_Count = 0
			Process_ID = False
			Process_V = False
			Process_Pass = False
			Site_err_flag = True
			pass

		line_count = line_count + 1


	f.close()

	if not Site_err_flag:
		print("\nSite#%d is OK" %(SiteNumber))

	input("Please key enter to leave.")

#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
def function3_check_all_time_zone():

	SiteNumber_str = input("What site do you want to check?\n")

	try:
		SiteNumber = int(SiteNumber_str)
	except:
		print("Plase enter site number. ex: 3.")
		input("Please key enter to leave.")
		quit()

	Timing_Allow_L_str = input("How much time do programmer verification at least(minimum)? Please input second. ex: 5\n") 

	try:
		Timing_Allow_L = int(Timing_Allow_L_str)
	except:
		print("Plase enter second. ex: 5.")
		input("Please key enter to leave.")
		quit()


	Timing_Allow_H_str = input("How much time do programmer verification maximum? Please input second. ex: 5\n") 

	try:
		Timing_Allow_H = int(Timing_Allow_H_str)
	except:
		print("Plase enter second. ex: 5.")
		input("Please key enter to leave.")
		quit()


	if Timing_Allow_H < Timing_Allow_L:
		print("Maximum(%d) second less minimum(%d) second. Please restart." %(Timing_Allow_H, Timing_Allow_L))
		input("Please key enter to leave.")
		quit()

######################################################################################
######################################################################################
######################################################################################

	try:
		f = open('LogC.txt','r')
	except:
		print("LogC.txt not exist. Please put LogC.txt and ProcessChecking.exe into the same folder.")
		quit()

	line = f.readlines()

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
		Parse_Message, Message_time = ParseSite(x, SiteNumber)

		if "get_ID_message" == Parse_Message:
			Process_ID = True
			ID_Time = Message_time
			Message_line_showed = line_count;
			ID_Count = ID_Count + 1

		if "get_prog_message" == Parse_Message:
			Process_P = True
			VF_Time = Message_time
			PG_Count = PG_Count + 1

		if "get_verify_message" == Parse_Message:
			Process_V = True
			VF_Time = Message_time
			VF_Count = VF_Count + 1

		if Process_ID:
			if ("Verify_Process_Done" == Parse_Message) or ("Program_Process_Done" == Parse_Message):
				Pass_time = Message_time
				Process_Pass = True

		if Process_ID and Process_V and Process_Pass:
			ID_Count = 0
			PG_Count = 0
			VF_Count = 0
			Process_ID = False
			Process_V = False
			Process_Pass = False
			####################
			#Check time zone
			####################
			
			#Step1: Checking cross day
			if (Pass_time - ID_Time) < 0:
				Pass_time  = Pass_time + 86400

			#Step2: Checking time zoe over seting
			if (Pass_time - ID_Time) > Timing_Allow_H:
				print("Process time wrong. Process time is too long. Spent %d second. " %( Pass_time - ID_Time))
				print("Please check line %d ~ %d." %(Message_line_showed, line_count))
				Site_err_flag = True

			if (Pass_time - ID_Time) < Timing_Allow_L:
				print("Process time wrong. Process time is too short. Spent %d second. " %( Pass_time - ID_Time))
				print("Please check line %d ~ %d." %(Message_line_showed, line_count))
				Site_err_flag = True


		if Process_ID and not Process_V and Process_Pass:
			print("Process wrong. Verify not happen. Please check line %d." %(line_count))
			ID_Count = 0
			PG_Count = 0
			VF_Count = 0
			Process_ID = False
			Process_V = False
			Process_Pass = False
			Site_err_flag = True
			pass

		line_count = line_count + 1


	f.close()

	if not Site_err_flag:
		print("\nSite#%d is OK" %(SiteNumber))

	input("Please key enter to leave.")


