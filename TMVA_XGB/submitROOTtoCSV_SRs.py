import os,shutil,datetime,time
import getpass
import varsList
from ROOT import *
from XRootD import client
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument( "-s", "--SR", required = True, help = "Options: 1, 2, 3" )
parser.add_argument( "-y", "--year",  help = "Options: 16APV, 16, 17, 18" )

args = parser.parse_args()

if args.year not in ['16', '17', '18', '16APV']: quit( "[ERR] Invalid option used for -y (--year). Quitting." )
if args.SR not in ['1', '2', '3']: quit( "[ERR] Invalid option used for -s (--SR). Quitting." )
###############################################

runDir = os.getcwd()
start_time = time.time()

outputDir= '/isilon/hadoop/store/group/bruxljm/FWLJMET106XUL_singleLep20{}UL_RunIISummer20_3t_step2CSV/XGB_CSV/SR{}'.format(args.year, args.SR)
condorDir= runDir+'/logs/condor_logs_CSV_UL{}_SR{}/'.format(args.year, args.SR)

print 'Starting submission'
count=0

#inDir=inputDir[10:]
#outDir=outputDir[10:]

os.system('mkdir -p '+outputDir)
os.system('mkdir -p '+condorDir)

#eosoutdir = outputDir[outputDir.find("/store"):]
#eosoutdir = "root://cmseos.fnal.gov/"+eosoutdir

Masses = [200, 220, 250, 300, 350, 400, 500, 600, 700,  800, 1000, 1250, 1500, 1750, 2000, 2500, 3000]

for mass in Masses:
    count+=1
    dict={'RUNDIR':runDir, 'CONDORDIR':condorDir, 'MASS':mass, 'OUTPUTDIR':outputDir, 'YEAR':args.year, 'SR':args.SR}
    jdfName=condorDir+'/M%(MASS)s.job'%dict
    print jdfName
    jdf=open(jdfName,'w')
    jdf.write(
"""universe = vanilla
Executable = %(RUNDIR)s/submitROOTtoCSV_SRs.sh
Request_memory = 8000
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Transfer_Input_Files = %(RUNDIR)s/UpROOTtoCSV_SRs.py, %(RUNDIR)s/varsList.py 
Output = M%(MASS)s.out
Error = M%(MASS)s.err
Log = M%(MASS)s.log
Notification = Never
Arguments =  %(OUTPUTDIR)s  %(MASS)s  NewVar_added  %(YEAR)s  %(SR)s

Queue 1"""%dict)
    jdf.close()
    os.chdir('%s/'%(condorDir))
    os.system('condor_submit M%(MASS)s.job'%dict)
    os.system('sleep 0.5')
    os.chdir('%s'%(runDir))
    print count, "jobs submitted!!!"

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))


