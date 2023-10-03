import os,sys
import ROOT as rt

shift = sys.argv[1]
inputDir  = '/eos/uscms/store/user/fsimpson/FWLJMET106XUL_singleLep2017UL_RunIISummer20v2_step2/'+shift+'/'#'/mnt/hadoop/store/group/bruxljm/FWLJMET106X_1lep'+str(Year)+'_X53_step1hadds/'+shift+'/'
rootfiles = os.popen('ls '+inputDir)

for file in rootfiles:
    if 'SingleElectron' in file: continue
    if 'SingleMuon' in file: continue
    if 'JetHT' in file: continue
    if 'EGamma' in file: continue
    print file
    RFile = rt.TFile(inputDir+file.strip(),'READ')
    hist1 = RFile.Get("NumTrueHist").Clone("NumTrueHist")
    hist2 = RFile.Get("weightHist").Clone("weightHist")
    print hist1.Integral(),hist2.GetBinContent(1),file.strip()
