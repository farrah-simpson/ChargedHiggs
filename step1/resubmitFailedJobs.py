#!/usr/bin/python

import os,sys,pickle

inputDir = '/uscms/home/fsimpson/nobackup/scratch/FWLJMETstuff/CMSSW_10_6_19/src/ChargedHiggs/step1/condor_singleLepton_UL17/'#'/uscms_data/d3/ssagir/FWLJMET102X_1lep2018_Oct2019_4t_042520_step1/'
resubmit_err = False
resubmit_out = False
resubmit_fail = False
resubmit_running = False  # Make sure you know what you are doing with this option!
resubmit = False

samplesDone = []
if os.path.exists(os.getcwd()+'/samplesDone.p'): pickle.load(open('samplesDone.p','rb'))
N_totjobs = 0
N_running = 0
N_err  = 0
N_out  = 0
N_fail = 0
samples = [x for x in os.walk(inputDir).next()[1]]
for sample in sorted(samples):
	#if 'WJetsToLNu_HT-2500ToInf_' not in sample: continue
	print "SAMPLE:",sample
	if sample in samplesDone: continue
	files = [x for x in os.listdir(inputDir+'/'+sample) if '.job' in x]
	sampleDone = True
	for file in files:
		N_totjobs+=1
		jFile = inputDir+'/'+sample+'/'+file
		lFile = inputDir+'/'+sample+'/'+file.replace('.job','.log')
		eFile = inputDir+'/'+sample+'/'+file.replace('.job','.err')
		oFile = inputDir+'/'+sample+'/'+file.replace('.job','.out')
		
		isOutFileExist = False
		isOutFileOK = False
		isErrFileExist = False
		isThereError = False
		isLogFileExist = False
		isJobDone = False
		isJobFailed = False
		
		if os.path.exists(oFile): isLogFileExist = True
		if isLogFileExist: 
			logFdata = open(lFile).read()
			if 'Normal termination' in logFdata: 
				isJobDone = True
				if 'Normal termination (return value 0)' not in logFdata: isJobFailed = True
				
		if os.path.exists(oFile): isOutFileExist = True
		if isOutFileExist: 
			outFdata = open(oFile).read()
			if 'Npassed_ALL' in outFdata and 'done' in outFdata and 'error' not in outFdata: isOutFileOK = True
			if 'WARNING! Event does not have defined ttbar category!!!' in outFdata: print outFdata
		
		if os.path.exists(eFile): isErrFileExist = True
		if isErrFileExist: 
			errFdata = open(eFile).read()
			if 'error' in errFdata or 'Error' in errFdata: isThereError = True
			#if 'unknown branch' in errFdata: isThereError = False
			statement33 = "Permission denied" in errFdata
		statement = isOutFileExist and isOutFileOK
		statement = statement and isErrFileExist and not isThereError 
		statement = statement and isLogFileExist and isJobDone and not isJobFailed
		if not statement or statement33:
			sampleDone = statement
			print "        FILE:",file
			if not (isLogFileExist and isJobDone):
				print "              --Job still running!"
				N_running+=1
				if resubmit_running:
					print "                RESUBMITTING ..."
					os.chdir(inputDir+'/'+sample)
					os.system('rm ' + lFile)
					os.system('rm ' + eFile)
					os.system('rm ' + oFile)
					os.system('condor_submit ' + jFile)
			elif isJobFailed:
				print "              --Job failed!"
				N_fail+=1
				if resubmit or resubmit_fail:
					print "                RESUBMITTING ..."
					os.chdir(inputDir+'/'+sample)
					os.system('rm ' + lFile)
					os.system('rm ' + eFile)
					os.system('rm ' + oFile)
					os.system('condor_submit ' + jFile)
			elif not (isOutFileExist and isOutFileOK):
				print "              --Problem in out file!"
				N_out+=1
				if resubmit or resubmit_out:
					print "                RESUBMITTING ..."
					os.chdir(inputDir+'/'+sample)
					os.system('rm ' + lFile)
					os.system('rm ' + eFile)
					os.system('rm ' + oFile)
					os.system('condor_submit ' + jFile)
			elif not (isErrFileExist and not isThereError):
				print "              --There is error!"
				N_err+=1
				if resubmit or resubmit_err:
					print "                RESUBMITTING ..."
					os.chdir(inputDir+'/'+sample)
					os.system('rm ' + lFile)
					os.system('rm ' + eFile)
					os.system('rm ' + oFile)
					os.system('condor_submit ' + jFile)
	if sampleDone: samplesDone.append(sample)

pickle.dump(samplesDone,open(os.getcwd()+'/samplesDone.p','wb'))
print N_running, "jobs are still running!"
print N_err, "jobs have error in .err file!"
print N_out, "jobs have error in .out file!"
print N_fail, "jobs failed!"
print N_running+N_err+N_out+N_fail,"/",N_totjobs, "jobs resubmitted in total!"

