import os,shutil,datetime,time
import getpass
import varsList
from ROOT import *
from XRootD import client

###############################################

runDir = os.getcwd()
start_time = time.time()

#inputDir='/eos/uscms/store/user/lpcbril/MC_test/FWLJMET102X_1lep2017_Oct2019_4t_080420_step2_newvar_updated_Pt40_Eta2p4'
outputDir= '/eos/uscms/store/user/fsimpson/FWLJMET106X_1lep2017_UL_step2_CSV_added'
condorDir= runDir+'/condor_logs_CSV_SR1/'

print 'Starting submission'
count=0

#inDir=inputDir[10:]
#outDir=outputDir[10:]

os.system('mkdir -p '+outputDir)
os.system('mkdir -p '+condorDir)

eosoutdir = outputDir[outputDir.find("/store"):]
eosoutdir = "root://cmseos.fnal.gov/"+eosoutdir

Masses = [1000]#,  800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600]

for mass in Masses:
    count+=1
    dict={'RUNDIR':runDir, 'CONDORDIR':condorDir, 'MASS':mass, 'OUTPUTDIR':eosoutdir}
    jdfName=condorDir+'/M%(MASS)s.job'%dict
    print jdfName
    jdf=open(jdfName,'w')
    jdf.write(
"""universe = vanilla
Executable = %(RUNDIR)s/submitROOTtoCSV_SR1.sh
Request_memory = 8000
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Transfer_Input_Files = %(RUNDIR)s/UpROOTtoCSV_SR1.py, %(RUNDIR)s/varsList.py 
Output = M%(MASS)s.out
Error = M%(MASS)s.err
Log = M%(MASS)s.log
Notification = Never
Arguments =  %(OUTPUTDIR)s  %(MASS)s  BigComb

Queue 1"""%dict)
    jdf.close()
    os.chdir('%s/'%(condorDir))
    os.system('condor_submit M%(MASS)s.job'%dict)
    os.system('sleep 0.5')
    os.chdir('%s'%(runDir))
    print count, "jobs submitted!!!"

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))


