import os,shutil,datetime,time
import getpass
from ROOT import *
from XRootD import client #execfile("/uscms_data/d3/jmanagan/EOSSafeUtils.py")
xrdClient = client.FileSystem("root://cmseos.fnal.gov/")

start_time = time.time()

#IO directories must be full paths

#relbase ='/user_data/ssagir/CMSSW_10_2_10/'
#inputDir='/eos/uscms/store/user/lpcljm/FWLJMET102X_1lep2017_052219/' # or 2018
inputDir='/eos/uscms/store/user/lpcljm/FWLJMET102X_1lep2017_Oct2019/' # or 2018
outputDir='/store/group/lpcbril/MC_test/ChargedHiggsNew/nominal'#'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_4t_12142019_step1/nominal/' # or 2018
condorDir='/uscms_data/d3/jluo/work/CMSSW_dir/CMSSW_10_2_10/src/LJMet-Slimmer-4tops/step1/condor/'
Year = 2017 # or 2018
finalStateYear = 'singleLep'+str(Year)
shifts = ['JECup','JECdown','JERup','JERdown']

runDir=os.getcwd()
inDir=inputDir[10:]
outDir=outputDir#[10:]

gROOT.ProcessLine('.x compileStep1.C')

print 'Starting submission'
count=0

dirList = [
#'DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8',
#'DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8',
#'DYJetsToLL_M-50_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8',
#'DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8',
#'DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8',
#'DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8',
#'QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8',
#'QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8',
#'QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8',
#'QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8',
#'QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8',
#'QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8',
#'QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8',
#'ST_s-channel_antitop_leptonDecays_13TeV-PSweights_powheg-pythia',
#'ST_s-channel_top_leptonDecays_13TeV-PSweights_powheg-pythia',
#'ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8',
#'ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8',
#'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8',
#'ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8',
# 'JetHT',
#'SingleElectron',
#'SingleMuon',
#'TTHH_TuneCP5_13TeV-madgraph-pythia8',
#'TTTJ_TuneCP5_13TeV-madgraph-pythia8',
#'TTTT_TuneCP5_13TeV-amcatnlo-pythia8',
#'TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8',
#'TTTW_TuneCP5_13TeV-madgraph-pythia8',
#'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8',
# 'TTTo2L2Nu_TuneCP5_erdON_13TeV-powheg-pythia8',
#'TTTo2L2Nu_TuneCP5down_PSweights_13TeV-powheg-pythia8',
#'TTTo2L2Nu_TuneCP5up_PSweights_13TeV-powheg-pythia8',
#'TTTo2L2Nu_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8',
#'TTTo2L2Nu_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8',
#'TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8',
# 'TTToHadronic_TuneCP5_erdON_13TeV-powheg-pythia8',
#'TTToHadronic_TuneCP5down_PSweights_13TeV-powheg-pythia8',
#'TTToHadronic_TuneCP5up_PSweights_13TeV-powheg-pythia8',
#'TTToHadronic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8',
#'TTToHadronic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8',
#'TTToSemiLepton_HT500Njet9_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TTToSemiLeptonic_TuneCP5_erdON_13TeV-powheg-pythia8',
# 'TTToSemiLeptonic_TuneCP5down_PSweights_13TeV-powheg-pythia8',
# 'TTToSemiLeptonic_TuneCP5up_PSweights_13TeV-powheg-pythia8',
#'TTToSemiLeptonic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8',
#'TTToSemiLeptonic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8',
#'TTWH_TuneCP5_13TeV-madgraph-pythia8',
#'TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8',
#'TTWW_TuneCP5_13TeV-madgraph-pythia8',
#'TTWZ_TuneCP5_13TeV-madgraph-pythia8',
#'TTZH_TuneCP5_13TeV-madgraph-pythia8',
#'TTZToLLNuNu_M-10_TuneCP5_PSweights_13TeV-amcatnlo-pythia8',
#'TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8',
#'TTZZ_TuneCP5_13TeV-madgraph-pythia8',
# 'TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8',
# 'TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8',
#'WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8',
#'WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8',
#'WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8',
#'WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8',
#'WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8',
#'WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8',
#'WW_TuneCP5_13TeV-pythia8',
#'WZ_TuneCP5_13TeV-pythia8',
#'ZZ_TuneCP5_13TeV-pythia8',
#'ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8',
#'ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8',
]
            
for sample in dirList:
    print "------------ Sample:",sample,"---------------"
    outList = ['none']
    if 'Tprime' in sample: outList = ['BWBW','TZBW','THBW','TZTH','TZTZ','THTH']
    elif 'Bprime' in sample: outList = ['TWTW','BZTW','BHTW','BZBH','BZBZ','BHBH']
#    elif 'TTToSemiLeptonic' in sample: outList = ['HT0Njet0','HT500Njet9']
    #elif 'TTTo' in sample: outList = ['Mtt0to700','Mtt700to1000','Mtt1000toInf']
#    if 'TTTo' in sample or 'TT_Mtt' in sample: 
#    	if outList==['none']: outList = ['ttbb','ttcc','ttjj']
#    	else:
#    		outList_ = outList[:]
#    		outList = []
#    		for outlabel in outList_:
#    			for flv in ['ttbb','ttcc','ttjj']: outList.append(outlabel+'_'+flv)

    isData = False
    if 'Single' in sample or 'EGamma' in sample: isData = True

    for outlabel in outList:
        tmpcount = 0

        outsample = sample+'_'+outlabel
        if outlabel == 'none': outsample = sample

        os.system('mkdir -p '+outDir+outsample)
        for shift in shifts: os.system('mkdir -p '+outDir.replace('nominal',shift)+outsample)
        os.system('mkdir -p '+condorDir+outsample)

        status, dirList = xrdClient.dirlist(inDir+'/'+sample+'/'+finalStateYear+'/')
        runlist = [item.name for item in dirList]
        print "Running",len(runlist),"crab directories"

        for run in runlist:
            status, dirList = xrdClient.dirlist(inDir+'/'+sample+'/'+finalStateYear+'/'+run+'/')
            numlist = [item.name for item in dirList]
            
            for num in numlist:
                numpath = inputDir+'/'+sample+'/'+finalStateYear+'/'+run+'/'+num
                pathsuffix = numpath.split('/')[-3:]
                pathsuffix = '/'.join(pathsuffix)

                #rootfiles = os.system('xrdfs root://cmseos.fnal.gov ls '+numpath)
                status, fileList = xrdClient.dirlist(inDir+'/'+sample+'/'+finalStateYear+'/'+run+'/'+num+'/')
                rootfiles = [item.name for item in fileList if item.name.endswith('.root')]           
                basefilename = (rootfiles[0].split('.')[0]).split('_')[:-1]
                basefilename = '_'.join(basefilename)
                print "Running path:",pathsuffix,"\tBase filenames:",basefilename

                nFilesPerJob=30
                for i in range(0,len(rootfiles),nFilesPerJob):
                    count+=1
                    tmpcount += 1

                    #if tmpcount > 1: continue

                    segment1 = (rootfiles[i].split('.')[0]).split('_')[-1] ## 1-1
                    segment2 = (rootfiles[i].split('.')[0]).split('_')[-2] ## SingleElectronRun2017C

                    if isData:    # need unique IDs across eras
                        idlist = segment2[-1]+segment1+' '
                        for j in range(i+1,i+nFilesPerJob):
                            if j >= len(rootfiles): continue
                            idparts = (rootfiles[j].split('.')[0]).split('_')[-2:]
                            idlist += idparts[0][-1]+idparts[1]+' '
                    elif 'ext' in segment2:     # WON'T WORK in FWLJMET 052219, but ok since no samples need it
                        idlist = segment2[-4:]+segment1+' '
                        for j in range(i+1,i+nFilesPerJob):
                            if j >= len(rootfiles): continue
                            idparts = (rootfiles[j].split('.')[0]).split('_')[-2:]
                            idlist += idparts[0][-4:]+idparts[1]+' '
                    else:
                        idlist = segment1+' '
                        for j in range(i+1,i+nFilesPerJob):
                            if j >= len(rootfiles): continue
                            idlist += (rootfiles[j].split('.')[0]).split('_')[-1]+' '
                        
                    idlist = idlist.strip()
                    print "Running IDs",idlist
                
                    dict={'RUNDIR':runDir, 'SAMPLE':sample, 'INPATHSUFFIX':pathsuffix, 'INPUTDIR':inDir, 'FILENAME':basefilename, 'OUTFILENAME':outsample, 'OUTPUTDIR':outDir, 'LIST':idlist, 'ID':tmpcount, 'YEAR':Year}
                    jdfName=condorDir+'/%(OUTFILENAME)s/%(OUTFILENAME)s_%(ID)s.job'%dict
                    print jdfName
                    jdf=open(jdfName,'w')
                    jdf.write(
                        """use_x509userproxy = true
universe = vanilla
Executable = %(RUNDIR)s/makeStep1brux.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Transfer_Input_Files = %(RUNDIR)s/compileStep1.C, %(RUNDIR)s/makeStep1.C, %(RUNDIR)s/step1.cc, %(RUNDIR)s/step1.h, %(RUNDIR)s/BTagCalibForLJMet.cpp, %(RUNDIR)s/DeepCSV_94XSF_V5_B_F.csv, %(RUNDIR)s/BTagCalibForLJMet.h, %(RUNDIR)s/HardcodedConditions.cc, %(RUNDIR)s/HardcodedConditions.h
Output = %(OUTFILENAME)s_%(ID)s.out
Error = %(OUTFILENAME)s_%(ID)s.err
Log = %(OUTFILENAME)s_%(ID)s.log
Notification = Never
Arguments = "%(FILENAME)s %(OUTFILENAME)s %(INPUTDIR)s/%(SAMPLE)s/%(INPATHSUFFIX)s %(OUTPUTDIR)s/%(OUTFILENAME)s '%(LIST)s' %(ID)s %(YEAR)s"

Queue 1"""%dict)
                    jdf.close()
                    os.chdir('%s/%s'%(condorDir,outsample))
                    os.system('condor_submit %(OUTFILENAME)s_%(ID)s.job'%dict)
                    os.system('sleep 0.5')                                
                    os.chdir('%s'%(runDir))
                    print count, "jobs submitted!!!"
        
print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))
