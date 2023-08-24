import os,itertools


lepPtCutList = [100] 
metCutList = [100]
drCutList = [1]
mtCutList = [0]
jet1PtCutList =[200] 
jet2PtCutList = [100]
jet3PtCutList = [0]
AK4HTCutList = [510]

cutConfigs = list(itertools.product(lepPtCutList,metCutList,mtCutList,drCutList,jet1PtCutList,jet2PtCutList,jet3PtCutList,AK4HTCutList))
for conf in cutConfigs:
	lepPtCut,metCut,mtCut,drCut,jet1PtCut,jet2PtCut,jet3PtCut,AK4HTCut=conf[0],conf[1],conf[2],conf[3],conf[4],conf[5],conf[6],conf[7]
	if jet2PtCut > jet1PtCut or jet3PtCut > jet1PtCut or jet3PtCut > jet2PtCut: continue
	cutString = 'lep'+str(int(lepPtCut))+'_MET'+str(int(metCut))+'_DR'+str(drCut)
	cutString+= '_HT'+str(AK4HTCut)
	cutString+= '_jet1Pt'+str(jet1PtCut) + '_jet2Pt'+str(jet2PtCut)

	trainings=[

	{
	'year':'R17',
	'variable':'HT',
	'postfix': 'templates_2023_7_27', #'66vars_4j_pt20',
	'cutString': cutString,
	'path':'root://cmseos.fnal.gov//store/user/fsimpson/FWLJMET106XUL_singleLep2017UL_RunIISummer20v2_step2/'
	},
	#{
	#'year':'R17',
	#'variable':'HT',
	#'postfix':'66vars_6j_pt20',
	#'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_08262020_step3_wenyu/BDT_SepRank6j73vars2017year_66vars_mDepth2_6j_year2017/'
	#},
	#{
	#'year':'R17',
	#'variable':'BDT',
	#'postfix':'73vars_4j_pt20',
	#'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_08262020_step3_wenyu/BDT_SepRank6j73vars2017year_73vars_mDepth2_4j_year2017/'
	#},
	#{
	#'year':'R17',
	#'variable':'BDT',
	#'postfix':'73vars_6j_pt20',
	#'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_08262020_step3_wenyu/BDT_SepRank6j73vars2017year_73vars_mDepth2_6j_year2017/'
	#},
	#
	#{
	#'year':'R18',
	#'variable':'BDT',
	#'postfix':'66vars_4j_pt20',
	#'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_08262020_step3_wenyu/BDT_SepRank6j73vars2017year_66vars_mDepth2_4j_year2018/'
	#},
	#{
	#'year':'R18',
	#'variable':'BDT',
	#'postfix':'66vars_6j_pt20',
	#'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_08262020_step3_wenyu/BDT_SepRank6j73vars2017year_66vars_mDepth2_6j_year2018/'
	#},
	#{
	#'year':'R18',
	#'variable':'BDT',
	#'postfix':'73vars_4j_pt20',
	#'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_08262020_step3_wenyu/BDT_SepRank6j73vars2017year_73vars_mDepth2_4j_year2018/'
	#},
	#{
	#'year':'R18',
	#'variable':'BDT',
	#'postfix':'73vars_6j_pt20',
	#'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_08262020_step3_wenyu/BDT_SepRank6j73vars2017year_73vars_mDepth2_6j_year2018/'
	#},
	
	]
	
	combinations = [
	#'66vars_4j_pt20_BDT',
	#'66vars_6j_pt20_BDT',
	#'73vars_4j_pt20_BDT',
	#'73vars_6j_pt20_BDT'
	 ]
	
	#which step would you like to run?
	#1 doCondorTemplates
	#2 doTemplates + modifyBinning + plotTemplates
	#3 dataCard + limit + significance
	#4 combination limit + significance
	#5 print results

	step=3
	
	if step==1:
		os.chdir('makeTemplates')
		for train in trainings:
			os.system('python doCondorTemplates.py '+train['year']+' '+train['variable']+' '+train['postfix']+' '+train['path'])
		os.chdir('..')
	
	if step==2:
		os.chdir('makeTemplates')
		for train in trainings:
			shell_name = 'condor_step2_'+train['year']+'_'+train['postfix']+'_'+train['variable']+'_'+train['cutString']+'.sh'
			shell=open(shell_name,'w')
			shell.write(
	'#!/bin/bash\n\
	source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
	cd /home/fsimpson/CMSSW_10_2_10/src\n\
	eval `scramv1 runtime -sh`\n\
	cd '+os.getcwd()+'\n\
	python doTemplates.py '+train['year']+' '+train['postfix']+'\n\
	python modifyBinning.py '+train['year']+' '+train['variable']+' '+train['postfix']+'\n\
	python plotTemplates.py '+train['year']+' '+train['variable']+' '+train['postfix']+'\n')
			shell.close()
			jdf_name = 'condor_step2_'+train['year']+'_'+train['postfix']+'_'+train['variable']+'.job'
			jdf=open(jdf_name,'w')
			jdf.write(
	'universe = vanilla\n\
	Executable = '+os.getcwd()+'/'+shell_name+'\n\
	Should_Transfer_Files = YES\n\
	WhenToTransferOutput = ON_EXIT\n\
	request_memory = 3072\n\
	Output = '+os.getcwd()+'/log/'+shell_name.split('.sh')[0]+'.out\n\
	Error = '+os.getcwd()+'/log/'+shell_name.split('.sh')[0]+'.err\n\
	Log = '+os.getcwd()+'/log/'+shell_name.split('.sh')[0]+'.log\n\
	Notification = Error\n\
	Arguments = \n\
	Queue 1\n')
			jdf.close()
			os.system('condor_submit '+jdf_name)
		os.chdir('..')
	
	
	if step==3:
		os.chdir('combineLimits')
		for train in trainings:
			shell_name = 'condor_step3_'+train['year']+'_'+train['postfix']+'_'+train['variable']+'_'+train['cutString']+'.sh'
			shell=open(shell_name,'w')
			shell.write(
	'#!/bin/bash\n\
	source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
	cd /uscms/home/fsimpson/nobackup/scratch/FWLJMETstuff/CMSSW_10_2_10/src\n\
	eval `scramv1 runtime -sh`\n\
	cd '+os.getcwd()+'\n\
	python dataCard.py '+train['postfix']+' '+train['year']+' '+train['variable']+' '+train['cutString']+'\n\
	cd limits_'+train['year']+'_'+train['postfix']+'_'+train['cutString']+'\n\
	combineTool.py -M Significance -d cmb/*/workspace.root --there -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 -n .sig --parallel 4\n\
	combineTool.py -M AsymptoticLimits -d cmb/*/workspace.root --there --run=blind --cminDefaultMinimizerStrategy 0 -n .limit --parallel 4\n\
    combineTool.py -M CollectLimits */*/*.limit.* --use-dirs -o limits.json\n\
    combineTool.py -M CollectLimits */*/*.sig.* --use-dirs -o sigs.json\n\
	cd ..\n')
			shell.close()
			jdf_name = 'condor_step3_'+train['year']+'_'+train['postfix']+'_'+train['variable']+'.job'
			jdf=open(jdf_name,'w')
			jdf.write(
	'universe = vanilla\n\
	Executable = '+os.getcwd()+'/'+shell_name+'\n\
	Should_Transfer_Files = YES\n\
	WhenToTransferOutput = ON_EXIT\n\
	request_memory = 3072\n\
	Output = '+os.getcwd()+'/log/'+shell_name.split('.')[0]+'.out\n\
	Error = '+os.getcwd()+'/log/'+shell_name.split('.')[0]+'.err\n\
	Log = '+os.getcwd()+'/log/'+shell_name.split('.')[0]+'.log\n\
	Notification = Error\n\
	Arguments = \n\
	Queue 1\n')
			jdf.close()
			os.system('condor_submit '+jdf_name)
		os.chdir('..')
	
	
	if step==4:
		os.chdir('combineLimits')
		for combo in combinations:
	
			shell_name = 'condor_step4_'+combo+'.sh'
			shell=open(shell_name,'w')
			shell.write(
	'#!/bin/bash\n\
	source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
	cd /home/fsimpson/CMSSW_10_2_10/src\n\
	eval `scramv1 runtime -sh`\n\
	cd '+os.getcwd()+'\n\
	combineCards.py R17=limits_R17_'+combo+'/cmb/combined.txt.cmb R18=limits_R18_'+combo+'/cmb/combined.txt.cmb &> BDTcomb/'+combo+'.txt\n\
	text2workspace.py  BDTcomb/'+combo+'.txt  -o BDTcomb/'+combo+'.root\n\
	combine -M Significance BDTcomb/'+combo+'.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 &> BDTcomb/sig_'+combo+'.txt\n\
	combine -M AsymptoticLimits BDTcomb/'+combo+'.root --run=blind --cminDefaultMinimizerStrategy 0 &> BDTcomb/asy_'+combo+'.txt\n')
			shell.close()
			jdf_name = 'condor_step4_'+combo+'.job'
			jdf=open(jdf_name,'w')
			jdf.write(
	'universe = vanilla\n\
	Executable = '+os.getcwd()+'/'+shell_name+'\n\
	Should_Transfer_Files = YES\n\
	WhenToTransferOutput = ON_EXIT\n\
	request_memory = 3072\n\
	Output = '+os.getcwd()+'/log/'+shell_name.split('.')[0]+'.out\n\
	Error = '+os.getcwd()+'/log/'+shell_name.split('.')[0]+'.err\n\
	Log = '+os.getcwd()+'/log/'+shell_name.split('.')[0]+'.log\n\
	Notification = Error\n\
	Arguments = \n\
	Queue 1\n')
			jdf.close()
			os.system('condor_submit '+jdf_name)
		os.chdir('..')
	
	def printlim(spec,year,variable):
	
		inputDir='limits_'+year+'_'+spec+'_'+variable
	
		sigFile = inputDir+'/sig.txt'
		sigData = open(sigFile,'r').read()
		siglines = sigData.split('\n')
		limFile = inputDir+'/asy.txt'
		limData = open(limFile,'r').read()
		limlines = limData.split('\n')
		theSig = ''
		theLim = ['']*5
		for line in siglines:
			if line.startswith('Significance:'): theSig = line.split()[-1]
		for line in limlines:
			if line.startswith('Expected  2.5%:'): theLim[0] =  "{:.2f}".format(float(line.split()[-1])*12)
			if line.startswith('Expected 16.0%:'): theLim[1] = "{:.2f}".format(float(line.split()[-1])*12)
			if line.startswith('Expected 50.0%:'): theLim[2] = "{:.2f}".format(float(line.split()[-1])*12)
			if line.startswith('Expected 84.0%:'): theLim[3] = "{:.2f}".format(float(line.split()[-1])*12)
			if line.startswith('Expected 97.5%:'): theLim[4] = "{:.2f}".format(float(line.split()[-1])*12)
		print year+' , '+variable+' , '+spec+' , '+theSig+' , '+theLim[0]+' , '+theLim[1]+' , '+theLim[2]+' , '+theLim[3]+' , '+theLim[4]
	
	def printcombolim(combo):
	
		inputDir='BDTcomb/'
	
		sigFile = inputDir+'/sig_'+combo+'.txt'
		sigData = open(sigFile,'r').read()
		siglines = sigData.split('\n')
		limFile = inputDir+'/asy_'+combo+'.txt'
		limData = open(limFile,'r').read()
		limlines = limData.split('\n')
		theSig = ''
		theLim = ['']*5
		for line in siglines:
			if line.startswith('Significance:'): theSig = line.split()[-1]
		for line in limlines:
			if line.startswith('Expected  2.5%:'): theLim[0] =  "{:.2f}".format(float(line.split()[-1])*12)
			if line.startswith('Expected 16.0%:'): theLim[1] = "{:.2f}".format(float(line.split()[-1])*12)
			if line.startswith('Expected 50.0%:'): theLim[2] = "{:.2f}".format(float(line.split()[-1])*12)
			if line.startswith('Expected 84.0%:'): theLim[3] = "{:.2f}".format(float(line.split()[-1])*12)
			if line.startswith('Expected 97.5%:'): theLim[4] = "{:.2f}".format(float(line.split()[-1])*12)
		print '17+18 , BDT , '+combo+' , '+theSig+' , '+theLim[0]+' , '+theLim[1]+' , '+theLim[2]+' , '+theLim[3]+' , '+theLim[4]
	
	if step==5:
		print 'Year , Var , Specifications , Significance , -2sigma, -1sigma, central, +1sigma, +2sigma'
		os.chdir('combineLimits')
		for train in trainings:
			printlim(train['postfix'] , train['year'] , train['variable'])
		for combo in combinations:
			printcombolim(combo)
		os.chdir('..')
	# python makeTemplates/doCondorTemplates.py R17 BDT 40vars_6j /mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_05182020_step3_wenyu/BDT_SepRank6j73vars2017year40top_40vars_mDepth2_4j_year2018/
	# python makeTemplates/doTemplates.py R17 40vars_6j
	# python makeTemplates/modifyBinning.py R17 BDT 40vars_6j
	# python makeTemplates/plotTemplates.py R17 BDT 40vars_6j
	# python combineLimits/dataCard.py R17 BDT 40vars_6j

