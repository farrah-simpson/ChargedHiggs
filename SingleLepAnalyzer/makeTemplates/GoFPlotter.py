import os,sys
from ROOT import TFile, TCanvas, TLine, TTree, TChain
execfile("/uscms_data/d3/jmanagan/EOSSafeUtils.py")

limitdir = sys.argv[1]
mass = sys.argv[2]
#datachi2 = float(sys.argv[3])

name = limitdir.replace('limits_combine_X53','').replace('limits_CR_combine_X53','')
path = limitdir+'/cmb/'+mass

os.chdir(path)

RFile=TFile.Open('root://cmseos.fnal.gov//store/user/fsimpson/Combine_GOF/'+limitdir+'_'+mass+'/higgsCombineTest.GoodnessOfFit.mH120.root')
#uscms/home/fsimpson/nobackup/scratch/FWLJMETstuff/CMSSW_11_3_4/src/ChargedHiggs/SingleLepAnalyzer/makeTemplates/fsimpson/limits_SRCR_combine_X53/cmb/1400/higgsCombineTest.GoodnessOfFit.mH120.root
data = RFile.Get('limit')
data.GetEntry(0)
datachi2 = data.limit

rootfiles =  EOSlist_root_files('/store/user/fsimpson/Combine_GOF/'+limitdir+'_'+mass+'/')

limit1 = TChain('limit')
for i in range(0,len(rootfiles)):
    if 'higgsCombineTest.GoodnessOfFit' not in rootfiles[i]: continue
    if 'higgsCombineTest.GoodnessOfFit.mH120.root' in rootfiles[i]: continue
    limit1.Add('root://cmseos.fnal.gov//store/user/fsimpson/Combine_GOF/'+limitdir+'_'+mass+'/'+rootfiles[i])

#RFile1=TFile.Open('higgsCombineTest.GoodnessOfFit.mH120.123456.root')
#limit1=RFile1.Get('limit')
GoF_can=TCanvas('GoodnessOfFit','GoodnessOfFit',800,600)
limit1.Draw('limit','','pe')
line=TLine(datachi2,0,datachi2,25)
line.SetLineColor(2)
line.SetLineWidth(2)
GoF_can.Update()
line.Draw('Draw')

GoF_can.SaveAs('GoodnessOfFit.png')
GoF_can.SaveAs('GoodnessOfFit.pdf')

