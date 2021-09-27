import os,sys,shutil,datetime,time
import getpass
from ROOT import *
from XRootD import client

start_time = time.time()
shift = sys.argv[1]

#IO directories must be full paths
foldnum = '-1'
relbase   = '/uscms/home/fsimpson/nobackup/scratch/FWLJMETstuff/CMSSW_10_6_19/' #'/home/wzhang/work/fwljmet_201905/CMSSW_10_2_16_UL/'
# inputDir  = '/mnt/hadoop/users/ssagir/LJMet94X_1lepTT_020619_step1hadds/'+shift+'/'
inputDir  = '/eos/uscms/store/user/fsimpson/FWLJMET106X_1lep2017UL_step1_new_hadds/'+shift+'/' #'/eos/uscms/store/user/lpcbril/MC_test/FWLJMET106X_1lep2017_UL_step1_reweight_b0_Sys_hadds/'+shift+'/'#'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_031920_step1hadds/'+shift+'/'
# outputDir = '/mnt/hadoop/users/jlee/TTTT/LJMet94X_1lepTT_022219_step2/'+shift+'/'
outputDir = '/eos/uscms/store/user/fsimpson/FWLJMET106X_1lep2017UL_step2_new/'+shift+'/'#'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_03302020_step2/'+shift+'/'
runDir=os.getcwd()
gROOT.ProcessLine('.x compileStep2.C')

cTime=datetime.datetime.now()
date='%i_%i_%i_%i_%i_%i'%(cTime.year,cTime.month,cTime.day,cTime.hour,cTime.minute,cTime.second)

condorDir=runDir+'/'+outputDir.split('/')[-3]+'_condorLogs/'+shift+'/'
print 'Starting submission'
count=0

rootfiles = os.popen('ls '+inputDir)
os.system('mkdir -p '+outputDir)
os.system('mkdir -p '+condorDir)
eosindir = inputDir[inputDir.find("/store"):]
eosindir = "root://cmseos.fnal.gov/"+eosindir

eosoutdir = outputDir[outputDir.find("/store"):]
eosoutdir = "root://cmseos.fnal.gov/"+eosoutdir

for file in rootfiles:
    if 'root' not in file: continue
#    if not 'QCD_HT200to300_' in file: continue
#    if 'TTTo' in file: continue
    rawname = file[:-6]
    count+=1
    dict={'RUNDIR':runDir, 'CONDORDIR':condorDir, 'INPUTDIR':eosindir, 'FILENAME':rawname, 'CMSSWBASE':relbase, 'OUTPUTDIR':eosoutdir}
    jdfName=condorDir+'/%(FILENAME)s.job'%dict
    print jdfName
    jdf=open(jdfName,'w')
    jdf.write(
"""universe = vanilla
Executable = %(RUNDIR)s/makeStep2.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
request_memory = 3072
Transfer_Input_Files = %(RUNDIR)s/makeStep2.C, %(RUNDIR)s/step2.cc, %(RUNDIR)s/step2.h, %(RUNDIR)s/step2_cc.d, %(RUNDIR)s/step2_cc.so, %(RUNDIR)s/Davismt2.cc, %(RUNDIR)s/Davismt2.h, %(RUNDIR)s/Davismt2_cc.d, %(RUNDIR)s/Davismt2_cc.so, %(RUNDIR)s/S2HardcodedConditions.cc, %(RUNDIR)s/S2HardcodedConditions.h, %(RUNDIR)s/S2HardcodedConditions_cc.d, %(RUNDIR)s/S2HardcodedConditions_cc.so, %(RUNDIR)s/HT_njets_SF_sys.root, %(RUNDIR)s/X53_HT_njets_SF_sys.root
  
Output = %(FILENAME)s.out
Error = %(FILENAME)s.err
Log = %(FILENAME)s.log
Notification = Never
Arguments = %(FILENAME)s.root %(FILENAME)s.root %(INPUTDIR)s %(OUTPUTDIR)s

Queue 1"""%dict)
    jdf.close()
    os.chdir('%s/'%(condorDir))
    os.system('condor_submit %(FILENAME)s.job'%dict)
    os.system('sleep 0.5')                                
    os.chdir('%s'%(runDir))
    print count, "jobs submitted!!!"

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))

