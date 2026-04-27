import os,sys
from ROOT import TFile, TH1F, TCanvas, TGraphAsymmErrors, kBlack, kRed, kAzure, kOrange, kMagenta, kGray, kBlue, kGreen, THStack, gStyle, TPad, TLatex, TLegend, gROOT, TColor
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from weights import *
from utils import *

gROOT.SetBatch()

Signal =True
pull = True
Sig = 'X53H'
combine = 'False'
blind = False
yLog = True
ScaleFact =1#-0.023#-0.023# -0.0009

limitdir = sys.argv[1]
mass = sys.argv[2]
if Sig == 'X53H': massH = sys.argv[3]
Sig2 = False

sig1 = 'X53RHM'+str(mass)
sig1leg = 'X_{5/3}#bar{X}_{5/3} (tW) ('+str(mass)+' GeV)'

if Sig2: 
    sig2 = 'X53RHM700'
    sig2leg = 'X_{5/3}#bar{X}_{5/3} (tW) (700 GeV)'

if Sig == 'X53H': 
	sig1 = 'X53M'+str(mass)+'MH'+str(massH)
	sig1leg = 'X_{5/3}#bar{X}_{5/3}('+str(mass)+' GeV) H^{+}('+str(massH)+' GeV)'

path = limitdir+'/cmb/'+mass

isSR = True

os.chdir(path)

#if not isSR:
#    shapesfile = 'CRPostFitShapes.root'
#    if not os.path.exists(shapesfile):
#        print('Creating pre and post-fit histograms from CR')
#        print('Command = PostFitShapesFromWorkspace -d combined.txt.cmb -w initialFitWorkspace.root --output CRPostFitShapes.root -m '+str(mass)+' -f fitDiagnostics.root:fit_b --postfit --sampling --print')
#        os.system('PostFitShapesFromWorkspace -d combined.txt.cmb -w initialFitWorkspace.root --output CRPostFitShapes.root -m '+str(mass)+' -f fitDiagnostics.root:fit_b --postfit --sampling --print')
#else:
#    shapesfile = 'SRPostFitShapes.root'
#    if not os.path.exists(shapesfile):
#        if Sig=='X53': masks = 'mask_R16APV_X53MRHM_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R16APV=0,mask_R16APV_X53MRHM_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R16APV=0,mask_R16_X53MRHM_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R16=0,mask_R16_X53MRHM_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R16=0,mask_R17_X53MRHM_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R17=0,mask_R17_X53MRHM_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R17=0,mask_R18_X53MRHM_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R18=0,mask_R18_X53MRHM_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R18=0'
#        if Sig=='X53H': masks = 'mask_R16APV_X53M_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R16APV=0,mask_R16APV_X53M_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R16APV=0,mask_R16_X53M_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R16=0,mask_R16_X53M_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R16=0,mask_R17_X53M_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R17=0,mask_R17_X53M_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R17=0,mask_R18_X53M_isSR_isM_nT0p_nW0p_nB1p_nJ4p_0_R18=0,mask_R18_X53M_isSR_isE_nT0p_nW0p_nB1p_nJ4p_0_R18=0'
#
#        print('Command = combine -M FitDiagnostics -d workspace.root --snapshotName initialFit --saveWorkspace --bypassFrequentistFit -t -1 -n SR --setParameters (all masks 0)')
#        print('Command = PostFitShapesFromWorkspace -d combined.txt.cmb -w higgsCombineSR.FitDiagnostics.mH120.root --output SRPostFitShapes.root -m '+str(mass)+' -f fitDiagnostics.root:fit_b --postfit --print')
#
#        os.system('combine -M FitDiagnostics -d workspace.root --snapshotName initialFit --saveWorkspace -n SR --setParameters '+masks)
#        os.system('PostFitShapesFromWorkspace -d workspace.txt -w higgsCombineSR.FitDiagnostics.mH120.root --output SRPostFitShapes.root -m '+str(mass)+' -f fitDiagnostics.root:fit_b --postfit --print')
#

if Signal: shapesfile = 'SRPostFitShapes_SplusB.root'
else: shapesfile = 'SRPostFitShapes.root'

def formatUpperHist(histogram,th1hist):
    histogram.SetTitle('')
    histogram.GetXaxis().SetLabelSize(0)
    lowside = th1hist.GetBinLowEdge(1)
    th1hist.GetBinLowEdge(th1hist.GetNbinsX()+1)
    highside = th1hist.GetBinLowEdge(th1hist.GetNbinsX()+1)
    histogram.GetXaxis().SetRangeUser(lowside,highside)
    histogram.GetXaxis().SetTitle('')
    histogram.GetYaxis().SetLabelSize(0.05)
    histogram.GetYaxis().SetTitleSize(0.06)
    histogram.GetYaxis().SetTitleOffset(.82)
    histogram.GetYaxis().CenterTitle()
    #histogram.SetMinimum(50*histogram.GetMinimum())
    if blind:
        histogram.GetXaxis().SetLabelSize(0.045)
        histogram.GetXaxis().SetTitleSize(0.055)
        histogram.GetYaxis().SetLabelSize(0.04)
        histogram.GetYaxis().SetTitleSize(0.05)
        histogram.GetYaxis().SetTitleOffset(1.1)
        histogram.GetXaxis().SetNdivisions(506)
    if not yLog: 
        histogram.SetMinimum(0.000101);
    else:
        uPad.SetLogy()
        histogram.SetMaximum(500*histogram.GetMaximum())
		
def formatLowerHist(histogram):
    histogram.GetXaxis().SetLabelSize(.12)
    histogram.GetXaxis().SetTitleSize(0.15)
    histogram.GetXaxis().SetTitleOffset(0.95)
    histogram.GetXaxis().SetNdivisions(506)
    histogram.GetYaxis().SetLabelSize(0.065)
    histogram.GetYaxis().SetTitleSize(0.14)
    histogram.GetYaxis().SetTitleOffset(.37)
    if Signal:histogram.GetYaxis().SetTitle('Data/ Bkg+Signal ')
    else: histogram.GetYaxis().SetTitle('Data/Bkg')
    histogram.GetYaxis().SetNdivisions(5)
    if Signal: histogram.GetYaxis().SetRangeUser(0.01,1.99)#(-6,6)
    else: histogram.GetYaxis().SetRangeUser(0.01,1.99)
    histogram.GetYaxis().CenterTitle()
#real pull
    histogram.SetTitle('')
    histogram.GetXaxis().SetLabelSize(.15)
    histogram.GetXaxis().SetTitleSize(0.18)
    histogram.GetXaxis().SetTitleOffset(0.95)
    histogram.GetXaxis().SetNdivisions(506)
    if 'XGB1300_SR1' in iPlot: 
        histogram.GetXaxis().SetTitle("BDT score(Mass_{X_{5/3}}= 1300 GeV)")
    elif 'XGB200_SR1' in iPlot: 
        histogram.GetXaxis().SetTitle("BDT score(Mass_{H^{\pm}}= 200 GeV)")
    elif 'XGB400_SR1' in iPlot: 
        histogram.GetXaxis().SetTitle("BDT score(Mass_{H^{\pm}}= 400 GeV)")
    elif 'XGB600_SR1' in iPlot: 
        histogram.GetXaxis().SetTitle("BDT score(Mass_{H^{\pm}}= 600 GeV)")
    elif 'XGB800_SR1' in iPlot: 
        histogram.GetXaxis().SetTitle("BDT score(Mass_{H^{\pm}}= 800 GeV)")
    elif 'XGB1000_SR1' in iPlot: 
        histogram.GetXaxis().SetTitle("BDT score(Mass_{H^{\pm}}= 1000 GeV)")
    if pull:
        histogram.GetYaxis().SetLabelSize(0.15)
        histogram.GetYaxis().SetTitleSize(0.145)
        histogram.GetYaxis().SetTitleOffset(.3)
        histogram.GetYaxis().SetTitle('#frac{data-bkg}{#sqrt{bkg-#sigma_{bkg}^{2}}}')
        histogram.GetYaxis().SetNdivisions(7)
        histogram.GetYaxis().SetRangeUser(-3.99,3.99)
        histogram.GetYaxis().CenterTitle()

print(shapesfile)
tFile = TFile.Open(shapesfile)

if Sig2: newfile = '/uscms_data/d3/fsimpson/scratch/FWLJMETstuff/CMSSW_11_3_4/src/ChargedHiggs/SingleLepAnalyzer/makeTemplates/limits_combine_X53/cmb/1200/SRPostFitShapes.root'
if Sig2: tFile2 = TFile.Open(newfile)

chns = []

if Sig == 'X53H':iPlot = 'XGB'+massH+'_SR1'
else: iPlot = 'XGB1300_SR1'

chns = [k.GetName() for k in tFile.GetListOfKeys() if k.GetName().endswith('_postfit')]
print(chns)
#else:
#    iPlot = 'DnnTprime'    
#    chns = [k.GetName() for k in tFile.GetListOfKeys() if k.GetName().endswith('_prefit')]
bkgProcList = ['qcd','ewk','top','ttbb','ttnobb']
bkgHistColors = {'tt2b':kRed-4,'ttbb':TColor.GetColor("#964a8b"),'tt1b':kRed-3,'ttcc':kRed-5,'ttjj':kRed-7,'top':TColor.GetColor("#5790fc"),'ewk':TColor.GetColor("#9c9ca1"),'qcd':TColor.GetColor("#f89c20"),'ttbar':kRed,'ttnobb':TColor.GetColor("#7a21dd")} #HTB
bkghists = {}
bkghistsmerged = {}

for chn in chns:
    if 'R17_' in chn:from weights_UL17 import *
    elif 'R18_' in chn:from weights_UL18 import *
    elif 'R16APV_' in chn:from weights_UL16APV import *
    elif 'R16_' in chn:from weights_UL16 import *
 
    lumi=str(targetlumi/1000).replace('p','.') #for plots

    for proc in bkgProcList:         
        try:     
            bkghists[chn+proc] = tFile.Get(chn+'/'+proc).Clone()
        except:
            print("There is no "+proc+"!")
            print("tried to open "+chn+'/'+proc)
            pass
    hData = tFile.Get(chn+'/data_obs').Clone()
    histrange = [hData.GetBinLowEdge(1),hData.GetBinLowEdge(hData.GetNbinsX()+1)]
    gaeData = TGraphAsymmErrors(hData.Clone(hData.GetName().replace('data_obs','gaeDATA')))
    hsig1 = tFile.Get(chn+'/'+sig1).Clone(chn+'__sig')
#    hsig1.Scale(xsec[sig1]) # input is 10fb rather than 1 pb CHECK

    for binNo in range(1,hsig1.GetNbinsX()+1):
        print("sig "+str(binNo)+" "+str(hsig1.GetBinContent(binNo)))
	
    if Signal: hsig1.Scale(ScaleFact) # input is 10fb rather than 1 pb CHECK


    if Sig2: 
        sig2 = tFile2.Get(chn+'/'+sig2).Clone(chn+'__sig2')
#        hsig2.Scale(xsec[sig2]) # input is 10fb rather than 1 pb CHECK
#
#    hsig3 = tFile.Get(chn+'/'+sig3).Clone(chn+'__sig3')
#    hsig3.Scale(xsec[sig3]*100) # input is 10fb rather than 1 pb CHECK

    #poissonNormByBinWidth(gaeData,hData,perNGeV)
    #for proc in bkgProcList:
    #    try: 
    #        normByBinWidth(bkghists[chn+proc],perNGeV)
    #    except: pass
    #normByBinWidth(hsig1,perNGeV)
    #normByBinWidth(hData,perNGeV)
    # Yes, there are easier ways using the TH1's but
    # it would be rough to swap objects lower down

    bkgHT = bkghists[chn+bkgProcList[0]].Clone()
    for proc in bkgProcList:
        if proc==bkgProcList[0]: continue
        try: 
            bkgHT.Add(bkghists[chn+proc])
        except: pass

    bkgHTgerr = TGraphAsymmErrors(bkgHT.Clone("bkgHTgerrPostFit"))    

    drawQCD = True
    try: drawQCD = bkghists[chn+'qcd'].Integral()/bkgHT.Integral() > 0.005
    except: pass

    stackbkgHT = THStack("stackbkgHT","")
    for proc in bkgProcList:
        try: 
            if drawQCD or proc != 'qcd': stackbkgHT.Add(bkghists[chn+proc])
            bkghists[chn+proc].SetLineColor(bkgHistColors[proc])
            bkghists[chn+proc].SetFillColor(bkgHistColors[proc])
            bkghists[chn+proc].SetLineWidth(2)
        except:
            pass

    hsig1.SetLineColor(TColor.GetColor("#717581"))
    hsig1.SetFillStyle(0)
    hsig1.SetLineWidth(3)

    if Sig2:
        hsig2.SetLineColor(kOrange)
        hsig2.SetFillStyle(0)
        hsig2.SetLineWidth(3)
#
#    hsig3.SetLineColor(kBlue)
#    hsig3.SetFillStyle(0)
#    hsig3.SetLineWidth(3)


    gaeData.SetMarkerStyle(20)
    gaeData.SetMarkerSize(1.2)
    gaeData.SetMarkerColor(kBlack)
    gaeData.SetLineWidth(2)
    gaeData.SetLineColor(kBlack)

    bkgHTgerr.SetFillStyle(3004)
    bkgHTgerr.SetFillColor(kBlack)
                            

    gStyle.SetOptStat(0)
    c1 = TCanvas("c1","c1",1200,1000)
    gStyle.SetErrorX(0.5)
    yDiv=0.25
    if blind: yDiv=0.01
    # for some reason the markers at 0 don't show with this setting:
    uMargin = 0.00001
    if blind: uMargin = 0.12
    rMargin=.04
    # overlap the pads a little to hide the error bar gap:
    uPad={}
    if yLog and not blind: uPad=TPad("uPad","",0,yDiv-0.009,1,1) #for actual plots
    else: uPad=TPad("uPad","",0,yDiv,1,1) #for actual plots
    uPad.SetTopMargin(0.08)
    uPad.SetBottomMargin(uMargin)
    uPad.SetRightMargin(rMargin)
    uPad.SetLeftMargin(.105)
    uPad.Draw()

    if not blind:
        lPad=TPad("lPad","",0,0,1,yDiv) #for sigma runner
        lPad.SetTopMargin(0)
        lPad.SetBottomMargin(.4)
        lPad.SetRightMargin(rMargin)
        lPad.SetLeftMargin(.105)
        lPad.SetGridy()
        lPad.Draw()

    hData.SetMinimum(0.015)
    hData.SetTitle("")
    gaeData.SetMaximum(1.6*max(gaeData.GetMaximum(),bkgHT.GetMaximum()))
    gaeData.SetMinimum(0.015)
    gaeData.SetTitle("")
    gaeData.GetYaxis().SetTitle("Events")# / "+str(perNGeV)+" GeV >")

    formatUpperHist(gaeData,hData)
    uPad.cd()
    gaeData.SetTitle("")

    hData.GetYaxis().SetTitle("Events")# / "+str(perNGeV)+" GeV >")
    if blind: hsig1.GetYaxis().SetTitle("Events")# / "+str(perNGeV)+" GeV >")

    if not blind: 
        gaeData.Draw("apz")
    else:
        #hsig1.SetMinimum(0.015)
        hsig1.SetMaximum(1.5*max(hData.GetMaximum(),bkgHT.GetMaximum()))
        formatUpperHist(hsig1,hsig1)
        

    stackbkgHT.Draw("SAME HIST")
    hsig1.Draw("SAME HIST")
#    hsig1.SetFillStyle(0)
#    hsig1.SetLineWidth(3)
    if Sig2: hsig2.Draw("SAME HIST")
#    hsig3.Draw("SAME HIST")

    if not blind: gaeData.Draw("PZ") #redraw data so its not hidden
    uPad.RedrawAxis()
    bkgHTgerr.Draw("SAME E2")

    chLatex = TLatex()
    chLatex.SetNDC()
    chLatex.SetTextSize(0.06)
    if blind: chLatex.SetTextSize(0.04)
    chLatex.SetTextAlign(21) # align center
    flvString = ''
    tagString = ''
    if 'isE' in chn: flvString+='e+jets'
    else: flvString+='#mu+jets'
    tagString = chn.split('_')[3]
    chLatex.DrawLatex(0.28, 0.84, flvString)
    #chLatex.DrawLatex(0.28, 0.78, tagString)
    if 'postfit' in chn: chLatex.DrawLatex(0.28, 0.72, 'post-fit')
    elif 'prefit' in chn: chLatex.DrawLatex(0.28, 0.72, 'pre-fit')

    if drawQCD: 
        leg = TLegend(0.45,0.64,0.95,0.89)
    else:
        leg = TLegend(0.45,0.76,0.95,0.89)
    leg.SetShadowColor(0)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)
    leg.SetLineStyle(0)
    leg.SetBorderSize(0) 
    leg.SetNColumns(2)
    leg.SetTextFont(62)#42)
    if drawQCD:
        if not blind:
            if Signal and ScaleFact != 1:leg.AddEntry(hsig1,sig1leg+" x"+str(ScaleFact),"l")  #left
            elif Signal and ScaleFact == 1:leg.AddEntry(hsig1,sig1leg,"l")
            else: leg.AddEntry(hsig1,sig1leg,"l") 
            if Sig2: leg.AddEntry(hsig2,sig2leg,"l")  #left
#            leg.AddEntry(hsig3,sig3leg,"l")  #left
            try: leg.AddEntry(bkghists[chn+'ttnobb'],"t#bar{t}+ not b#bar{b}","f")
            except: pass
            try: leg.AddEntry(bkghists[chn+'ttbb'],"t#bar{t}+b#bar{b}","f")
            except: pass
            try: 
                leg.AddEntry(bkghists[chn+'top'],"single t + t#bar{t}V/H","f") #right
            except: pass
            try: 
                leg.AddEntry(bkghists[chn+'ewk'],"electroweak processes","f") #right
            except: pass
            #except: pass
            leg.AddEntry(bkghists[chn+'qcd'],"QCD multijet","f") #right
            leg.AddEntry(gaeData,"Data","pel")  #left
            leg.AddEntry(bkgHTgerr,"Bkg. uncert.","f") #left
        else:
            if Signal and ScaleFact != 1:leg.AddEntry(hsig1,sig1leg+" x"+str(ScaleFact),"l")  #left
            elif Signal and ScaleFact == 1:leg.AddEntry(hsig1,sig1leg,"l")
            else: leg.AddEntry(hsig1,sig1leg,"l") 
            if Sig2: leg.AddEntry(hsig2,sig2leg,"l")  #left
#            leg.AddEntry(hsig3,sig3leg,"l")  #left
            leg.AddEntry(bkghists[chn+'qcd'],"","f") #right
            leg.AddEntry(bkgHTgerr,"Bkg. uncert.","f") #left
            try: 
                leg.AddEntry(bkghists[chn+'top'],"single t + t#bar{t}V/H","f") #right
            except: pass
            try: 
                leg.AddEntry(bkghists[chn+'ewk'],"electroweak processes","f") #right
            except: pass
            try: leg.AddEntry(bkghists[chn+'ttnobb'],"t#bar{t}+ not b#bar{b}","f")
            except: pass
            try: leg.AddEntry(bkghists[chn+'ttbb'],"t#bar{t}+b#bar{b}","f")
            except: pass
    else:
        if not blind:
            leg.AddEntry(gaeData,"Data","pel")  #left
            if Signal and ScaleFact != 1:leg.AddEntry(hsig1,sig1leg+" x"+str(ScaleFact),"l")  #left
            elif Signal and ScaleFact == 1:leg.AddEntry(hsig1,sig1leg,"l")
            else: leg.AddEntry(hsig1,sig1leg,"l") 
            if Sig2: leg.AddEntry(hsig2,sig2leg,"l")  #left
#            leg.AddEntry(hsig3,sig3leg,"l")  #left
            try: 
                leg.AddEntry(bkghists[chn+'top'],"single t + t#bar{t}V/H","f") #right
            except: pass
            try: 
                leg.AddEntry(bkghists[chn+'ewk'],"electroweak processes","f") #right
            except: pass
            try: leg.AddEntry(bkghists[chn+'ttnobb'],"t#bar{t}+ not b#bar{b}","f")
            except: pass
            try: leg.AddEntry(bkghists[chn+'ttbb'],"t#bar{t}+b#bar{b}","f")
            except: pass
            #except: pass
            leg.AddEntry(bkghists[chn+'qcd'],"QCD multijet","f") #right
            leg.AddEntry(bkgHTgerr,"Bkg. uncert.","f") #left
        else:
            if Signal and ScaleFact != 1:leg.AddEntry(hsig1,sig1leg+" x"+str(ScaleFact),"l")  #left
            elif Signal and ScaleFact == 1:leg.AddEntry(hsig1,sig1leg,"l")
            else: leg.AddEntry(hsig1,sig1leg,"l") 
            if Sig2: leg.AddEntry(hsig2,sig2leg,"l")  #left
#            leg.AddEntry(hsig3,sig3leg,"l")  #left
            try: 
                leg.AddEntry(bkghists[chn+'top'],"single t + t#bar{t}V/H","f") #right
            except: pass
            try: 
                leg.AddEntry(bkghists[chn+'ewk'],"electroweak processes","f") #right
            except: pass
            try: leg.AddEntry(bkghists[chn+'ttnobb'],"t#bar{t}+ not b#bar{b}","f")
            except: pass
            try: leg.AddEntry(bkghists[chn+'ttbb'],"t#bar{t}+b#bar{b}","f")
            except: pass
            #except: pass
            leg.AddEntry(bkghists[chn+'qcd'],"QCD multijet","f") #right
            leg.AddEntry(bkgHTgerr,"Bkg. uncert.","f") #left

    leg.Draw("same")

    prelimTex=TLatex()
    prelimTex.SetNDC()
    prelimTex.SetTextAlign(31) # align right
    prelimTex.SetTextFont(42)
    prelimTex.SetTextSize(0.05)
    prelimTex.SetLineWidth(2)
    prelimTex.DrawLatex(0.95,0.94,str(lumi)+" fb^{-1} (13 TeV)")

    prelimTex2=TLatex()
    prelimTex2.SetNDC()
    prelimTex2.SetTextFont(61)
    prelimTex2.SetLineWidth(2)
    prelimTex2.SetTextSize(0.08)
    prelimTex2.DrawLatex(0.12,0.93,"CMS")

    prelimTex3=TLatex()
    prelimTex3.SetNDC()
    prelimTex3.SetTextAlign(12)
    prelimTex3.SetTextFont(52)
    prelimTex3.SetTextSize(0.055)
    prelimTex3.SetLineWidth(2)
    prelimTex3.DrawLatex(0.23,0.945,"Preliminary")
    if blind: prelimTex3.DrawLatex(0.26,0.945,"Preliminary")

    if not blind:
        formatUpperHist(hData,hData)
        lPad.cd()
        pull=hData.Clone(chn+"pull")
        pull.Divide(hData, bkgHT+hsig1)
        if not pull:
            for binNo in range(1,hData.GetNbinsX()+1):
                if hData.GetBinContent(binNo)!=0:
                    if Signal: pull.SetBinError(binNo,hData.GetBinError(binNo)/(bkgHT.GetBinContent(binNo)+hsig1.GetBinContent(binNo)))
                    else: pull.SetBinError(binNo,hData.GetBinError(binNo)/(bkgHT.GetBinContent(binNo)+(hsig1.GetBinContent(binNo))))
                else: pull.SetBinContent(binNo,0.)
        else:
            for binNo in range(1,hData.GetNbinsX()+1):
                # case for data < MC:
                dataerror = gaeData.GetErrorYhigh(binNo-1)
                MCerror = bkgHTgerr.GetErrorYlow(binNo-1)
                # case for data > MC: 
                if(hData.GetBinContent(binNo) > bkgHT.GetBinContent(binNo)):
                    dataerror = gaeData.GetErrorYlow(binNo-1)
                    MCerror = bkgHTgerr.GetErrorYhigh(binNo-1)
                if(bkgHT.GetBinContent(binNo)>MCerror**2): pull.SetBinContent(binNo,((hData.GetBinContent(binNo)-bkgHT.GetBinContent(binNo)))/math.sqrt(bkgHT.GetBinContent(binNo)-(MCerror**2))) 
        #pull.SetMaximum(3)
        #pull.SetMinimum(-3)
        #pull.SetMaximum(2)
        #pull.SetMaximum(0.)
        pull.SetFillColor(kGray+2)
        pull.SetLineColor(kGray+2)
        formatLowerHist(pull)
        if pull: pull.Draw("HIST")
        #pull.Draw("E1")

        if not pull:
            BkgOverBkg = pull.Clone("bkgOverbkg")
            BkgOverBkg.Divide(bkgHT, bkgHT)
            pullUncBandTot=TGraphAsymmErrors(BkgOverBkg.Clone("pulluncTot"))
            for binNo in range(1,hData.GetNbinsX()+1):
                if bkgHT.GetBinContent(binNo)!=0:
                            pullUncBandTot.SetPointEYhigh(binNo-1,bkgHTgerr.GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
                            pullUncBandTot.SetPointEYlow(binNo-1,bkgHTgerr.GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
            pullUncBandTot.SetFillStyle(3002)
            pullUncBandTot.SetFillColor(14)
            pullUncBandTot.SetLineColor(14)
            pullUncBandTot.SetMarkerSize(0)
            gStyle.SetHatchesLineWidth(1)
            pullUncBandTot.Draw("SAME E2")
            
            for binNo in range(1,bkgHT.GetNbinsX()+1):
                print("bkg "+str(binNo)+" "+str(bkgHT.GetBinContent(binNo)))
            for binNo in range(1,hsig1.GetNbinsX()+1):
                print("r x sig "+str(binNo)+" "+str(hsig1.GetBinContent(binNo)))
	
    #savePrefix = 'PostFitPlots_SpluB/'
    if Signal: savePrefix = 'PostFitPlots_SpluB/'
    else: savePrefix = 'PostFitPlots/'
    if not os.path.exists(savePrefix): os.system('mkdir -p '+savePrefix)
    savePrefix+=iPlot+'_'+str(lumi).replace('.','p')+'fb_'+chn
    if blind: savePrefix+='_blind'
    if yLog: savePrefix+='_logy'

    c1.SaveAs(savePrefix+".pdf")
    c1.SaveAs(savePrefix+".png")

    for proc in bkgProcList:
        try: 
            del bkghists[chn+proc]
        except: pass
    del c1

    if '_isM_' in chn: continue

    for proc in bkgProcList:
        try: 
            bkghistsmerged[chn.replace('isE','isL')+proc] = tFile.Get(chn+'/'+proc).Clone()
            bkghistsmerged[chn.replace('isE','isL')+proc].Add(tFile.Get(chn.replace('isE','isM')+'/'+proc))
        except: pass

    hDatamerged = tFile.Get(chn+'/data_obs').Clone()
    hsig1merged = tFile.Get(chn+'/'+sig1).Clone(chn+'__sigmerged')
    if Sig2: hsig2merged = tFile2.Get(chn+'/'+sig2).Clone(chn+'__sigmerged2')
#    hsig3merged = tFile.Get(chn+'/'+sig3).Clone(chn+'__sigmerged3')

    hDatamerged.Add(tFile.Get(chn.replace('isE','isM')+'/data_obs').Clone())
    hsig1merged.Add(tFile.Get(chn.replace('isE','isM')+'/'+sig1).Clone())
#    hsig1merged.Scale(xsec[sig1])
    if Signal: hsig1merged.Scale(ScaleFact)

    if Sig2: 
        hsig2merged.Add(tFile2.Get(chn.replace('isE','isM')+'/'+sig2).Clone())
#        hsig2merged.Scale(xsec[sig2])
#    hsig3merged.Add(tFile.Get(chn.replace('isE','isM')+'/'+sig3).Clone())
#    hsig3merged.Scale(xsec[sig3]*100)

    histrange = [hDatamerged.GetBinLowEdge(1),hDatamerged.GetBinLowEdge(hDatamerged.GetNbinsX()+1)]
    gaeDatamerged = TGraphAsymmErrors(hDatamerged.Clone(hDatamerged.GetName().replace("data_obs","gaeDATA")))

#    poissonNormByBinWidth(gaeDatamerged,hDatamerged,perNGeV)
#    for proc in bkgProcList:
#        try: 
#            normByBinWidth(bkghistsmerged[chn.replace('isE','isL')+proc],perNGeV)
#        except: pass
#    normByBinWidth(hsig1merged,perNGeV)
#    normByBinWidth(hDatamerged,perNGeV)

    bkgHTmerged = bkghistsmerged[chn.replace('isE','isL')+bkgProcList[0]].Clone()
    for proc in bkgProcList:
        if proc==bkgProcList[0]: continue
        try: 
            bkgHTmerged.Add(bkghistsmerged[chn.replace('isE','isL')+proc])
        except: pass

    bkgHTgerrmerged = TGraphAsymmErrors(bkgHTmerged.Clone("bkgHTgerrmerged"))

    drawQCDmerged = False
    try: 
        drawQCDmerged = bkghistsmerged[chn.replace('isE','isL')+'qcd'].Integral()/bkgHTmerged.Integral()>.005
    except: pass

    stackbkgHTmerged = THStack("stackbkgHTmerged","")
    for proc in bkgProcList:
        try: 
            if drawQCDmerged or proc!='qcd': stackbkgHTmerged.Add(bkghistsmerged[chn.replace('isE','isL')+proc])
            bkghistsmerged[chn.replace('isE','isL')+proc].SetLineColor(bkgHistColors[proc])
            bkghistsmerged[chn.replace('isE','isL')+proc].SetFillColor(bkgHistColors[proc])
            bkghistsmerged[chn.replace('isE','isL')+proc].SetLineWidth(2)
        except: pass

    hsig1merged.SetLineColor(TColor.GetColor("#717581"))
    hsig1merged.SetFillStyle(0)
    hsig1merged.SetLineWidth(3)

    if Sig2: 
        hsig2merged.SetLineColor(kOrange)
        hsig2merged.SetFillStyle(0)
        hsig2merged.SetLineWidth(3)
#    hsig3merged.SetLineColor(kBlue)
#    hsig3merged.SetFillStyle(0)
#    hsig3merged.SetLineWidth(3)

    gaeDatamerged.SetMarkerStyle(20)
    gaeDatamerged.SetMarkerSize(1.2)
    gaeDatamerged.SetLineWidth(2)
    gaeDatamerged.SetMarkerColor(kBlack)
    gaeDatamerged.SetLineColor(kBlack)

    bkgHTgerrmerged.SetFillStyle(3004)
    bkgHTgerrmerged.SetFillColor(kBlack)

    gStyle.SetOptStat(0)
    c1merged = TCanvas("c1merged","c1merged",1200,1000)
    gStyle.SetErrorX(0.5)
    yDiv=0.25
    if blind: yDiv = 0.01
    uMargin = 0.00001
    if blind: uMargin = 0.12
    rMargin=.04
    uPad={}
    if yLog and not blind: 
        uPad=TPad("uPad","",0,yDiv-0.009,1,1) #for actual plots
    else: uPad=TPad("uPad","",0,yDiv,1,1) #for actual plots
    uPad.SetTopMargin(0.08)
    uPad.SetBottomMargin(uMargin)
    uPad.SetRightMargin(rMargin)
    uPad.SetLeftMargin(.105)
    uPad.Draw()

    if not blind:
        lPad=TPad("lPad","",0,0,1,yDiv) #for sigma runner
        lPad.SetTopMargin(0)
        lPad.SetBottomMargin(.4)
        lPad.SetRightMargin(rMargin)
        lPad.SetLeftMargin(.105)
        lPad.SetGridy()
        lPad.Draw()

    gaeDatamerged.SetMaximum(1.6*max(gaeDatamerged.GetMaximum(),bkgHTmerged.GetMaximum()))
    #gaeDatamerged.SetMinimum(0.015)
    gaeDatamerged.SetMinimum(0.015)
    gaeDatamerged.GetYaxis().SetTitle(" Events ")#/ "+str(perNGeV)+" GeV >")
    if blind: hsig1merged.GetYaxis().SetTitle(" Events ")#/ "+str(perNGeV)+" GeV >")

    formatUpperHist(gaeDatamerged,hData)
    #gaeDatamerged.GetXaxis().SetRangeUser(0.,0.85)

    uPad.cd()
    gaeDatamerged.SetTitle("")
    stackbkgHTmerged.SetTitle("")
    if not blind: 
        gaeDatamerged.Draw("apz")
    else:
        #hsig1merged.SetMinimum(0.015)
        hsig1merged.SetMaximum(1.5*max(hDatamerged.GetMaximum(),bkgHTmerged.GetMaximum()))
        formatUpperHist(hsig1merged,hsig1merged)
        hsig1merged.Draw("HIST")

#        hsig2merged.SetMinimum(0.015)
#        hsig2merged.SetMaximum(1.5*max(hDatamerged.GetMaximum(),bkgHTmerged.GetMaximum()))
#        formatUpperHist(hsig2merged,hsig2merged)
#        hsig2merged.Draw("HIST")
#
#        hsig3merged.SetMinimum(0.015)
#        hsig3merged.SetMaximum(1.5*max(hDatamerged.GetMaximum(),bkgHTmerged.GetMaximum()))
#        formatUpperHist(hsig3merged,hsig3merged)
#        hsig3merged.Draw("HIST")


    stackbkgHTmerged.Draw("SAME HIST")
#    hsig1merged.SetLineWidth(3)
#    hsig1merged.SetFillStyle(0)
    hsig1merged.Draw("SAME HIST")
    if Sig2: hsig2merged.Draw("SAME HIST")
#    hsig3merged.Draw("SAME HIST")

    if not blind: gaeDatamerged.Draw("PZ") #redraw data so its not hidden
    uPad.RedrawAxis()
    bkgHTgerrmerged.Draw("SAME E2")

    chLatexmerged = TLatex()
    chLatexmerged.SetNDC()
    chLatexmerged.SetTextSize(0.06)
    if blind: chLatexmerged.SetTextSize(0.04)
    chLatexmerged.SetTextAlign(21) # align center
    flvString = 'e/#mu+jets'
    tagString = chn.split('_')[3]
    chLatexmerged.DrawLatex(0.28, 0.85, flvString)    
    #chLatexmerged.DrawLatex(0.28, 0.78, tagString)
    if 'postfit' in chn: chLatexmerged.DrawLatex(0.28, 0.72, 'post-fit')
    elif 'prefit' in chn: chLatexmerged.DrawLatex(0.28, 0.72, 'pre-fit')

    if drawQCDmerged: 
        legmerged = TLegend(0.45,0.64,0.95,0.89)
    else: 
        legmerged = TLegend(0.45,0.76,0.95,0.89)

    legmerged.SetShadowColor(0)
    legmerged.SetFillColor(0)
    legmerged.SetFillStyle(0)
    legmerged.SetLineColor(0)
    legmerged.SetLineStyle(0)
    legmerged.SetBorderSize(0) 
    legmerged.SetNColumns(2)
    legmerged.SetTextFont(62)#42)                                      
    if drawQCDmerged:
        if not blind:
            if Signal and ScaleFact != 1:legmerged.AddEntry(hsig1merged,sig1leg+" x"+str(ScaleFact),"l")  #left
            elif Signal and ScaleFact == 1:legmerged.AddEntry(hsig1merged,sig1leg,"l")
            else: legmerged.AddEntry(hsig1merged,sig1leg,"l") 
            if Sig2: legmerged.AddEntry(hsig2merged,sig2leg,"l")  #left
            legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'ttnobb'],"t#bar{t}+ not b#bar{b}","f")
#            legmerged.AddEntry(hsig3merged,sig3leg,"l")  #left
            legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'ttbb'],"t#bar{t}+b#bar{b}","f")
            try: 
                legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'top'],"single t + t#bar{t}V/H","f") #right
            except: pass
            try: 
                legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'ewk'],"electroweak processes","f") #right
            except: pass
            legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'qcd'],"QCD multijet","f") #right
            legmerged.AddEntry(gaeDatamerged,"Data","pel")  #left
            legmerged.AddEntry(bkgHTgerrmerged,"Bkg. uncert.","f") #left
        else:
            if Signal and ScaleFact != 1:legmerged.AddEntry(hsig1merged,sig1leg+" x"+str(ScaleFact),"l")  #left
            elif Signal and ScaleFact == 1:legmerged.AddEntry(hsig1merged,sig1leg,"l")
            else: legmerged.AddEntry(hsig1merged,sig1leg,"l") 
            if Sig2: legmerged.AddEntry(hsig2merged,sig2leg,"l")  #left
#            legmerged.AddEntry(hsig3merged,sig3leg,"l")  #left
            legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'ttnobb'],"t#bar{t}+ not b#bar{b}","f")
#            legmerged.AddEntry(hsig3merged,sig3leg,"l")  #left
            legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'ttbb'],"t#bar{t}+b#bar{b}","f")
            try: 
                legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'top'],"single t + t#bar{t}V/H","f") #right
            except: pass
            try: 
                legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'ewk'],"electroweak processes","f") #right
            except: pass
            legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'qcd'],"QCD multijet","f") #right
 
    else:
        if not blind:
            legmerged.AddEntry(gaeDatamerged,"Data","pel")  #left
            if Signal and ScaleFact != 1:legmerged.AddEntry(hsig1merged,sig1leg+" x"+str(ScaleFact),"l")  #left
            elif Signal and ScaleFact == 1:legmerged.AddEntry(hsig1merged,sig1leg,"l")
            else: legmerged.AddEntry(hsig1merged,sig1leg,"l") 
            if Sig2: legmerged.AddEntry(hsig2merged,sig2leg,"l")  #left
            legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'ttnobb'],"t#bar{t}+ not b#bar{b}","f")
#            legmerged.AddEntry(hsig3merged,sig3leg,"l")  #left
            legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'ttbb'],"t#bar{t}+b#bar{b}","f")
            try: 
                legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'top'],"single t + t#bar{t}V/H","f") #right
            except: pass
            try: 
                legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'ewk'],"electroweak processes","f") #right
            except: pass
            legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'qcd'],"QCD multijet","f") #right
            legmerged.AddEntry(bkgHTgerrmerged,"Bkg. uncert.","f") #left
        else:
            if Signal and ScaleFact != 1:legmerged.AddEntry(hsig1merged,sig1leg+" x"+str(ScaleFact),"l")  #left
            elif Signal and ScaleFact == 1:legmerged.AddEntry(hsig1merged,sig1leg,"l")  #left
            else: legmerged.AddEntry(hsig1merged,sig1leg,"l") 
            if Sig2: legmerged.AddEntry(hsig2merged,sig2leg,"l") #left
 #           legmerged.AddEntry(hsig3merged,sig3leg,"l") #left
            legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'ttnobb'],"t#bar{t}+ not b#bar{b}","f")
#            legmerged.AddEntry(hsig3merged,sig3leg,"l")  #left
            legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'ttbb'],"t#bar{t}+b#bar{b}","f")
            try: 
                legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'top'],"single t + t#bar{t}V/H","f") #right
            except: pass
            try: 
                legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'ewk'],"electroweak processes","f") #right
            except: pass
            legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'qcd'],"QCD multijet","f") #right
    legmerged.Draw("same")
 
    prelimTex=TLatex()
    prelimTex.SetNDC()
    prelimTex.SetTextAlign(31) # align right
    prelimTex.SetTextFont(42)
    prelimTex.SetTextSize(0.05)
    prelimTex.SetLineWidth(2)
    prelimTex.DrawLatex(0.95,0.94,str(lumi)+" fb^{-1} (13 TeV)")
 
    prelimTex2=TLatex()
    prelimTex2.SetNDC()
    prelimTex2.SetTextFont(61)
    prelimTex2.SetLineWidth(2)
    prelimTex2.SetTextSize(0.08)
    prelimTex2.DrawLatex(0.12,0.93,"CMS")

    prelimTex3=TLatex()
    prelimTex3.SetNDC()
    prelimTex3.SetTextAlign(12)
    prelimTex3.SetTextFont(52)
    prelimTex3.SetTextSize(0.055)
    prelimTex3.SetLineWidth(2)
    prelimTex3.DrawLatex(0.23,0.945,"Preliminary")
    if blind: prelimTex3.DrawLatex(0.26,0.945,"Preliminary")

    if not blind:
        formatUpperHist(hDatamerged,hDatamerged)
        lPad.cd()
        pullmerged=hDatamerged.Clone(chn.replace('isE','isL')+"pullmerged")
        if Signal: pullmerged.Divide(hDatamerged, bkgHTmerged+hsig1merged)
        else: pullmerged.Divide(hDatamerged, bkgHTmerged)
        if pull:
            for binNo in range(1,hDatamerged.GetNbinsX()+1):
               # case for data < MC:
                dataerror = gaeDatamerged.GetErrorYhigh(binNo-1)
                MCerror = bkgHTgerrmerged.GetErrorYlow(binNo-1)
               # case for data > MC:
                if(hDatamerged.GetBinContent(binNo) > bkgHTmerged.GetBinContent(binNo)):
                    dataerror = gaeDatamerged.GetErrorYlow(binNo-1)
                    MCerror = bkgHTgerrmerged.GetErrorYhigh(binNo-1)
                if(bkgHTmerged.GetBinContent(binNo)>MCerror**2):pullmerged.SetBinContent(binNo,((hDatamerged.GetBinContent(binNo)-bkgHTmerged.GetBinContent(binNo)))/math.sqrt(bkgHTmerged.GetBinContent(binNo)-(MCerror**2)))

#       if 1==1:
        else:
            for binNo in range(1,hDatamerged.GetNbinsX()+1):
                if hDatamerged.GetBinContent(binNo)!=0 and hDatamerged.GetBinContent(binNo) > 0:
                    if Signal: pullmerged.SetBinError(binNo,hDatamerged.GetBinError(binNo)/(bkgHTmerged.GetBinContent(binNo)+hsig1merged.GetBinContent(binNo)))
                    else: pullmerged.SetBinError(binNo,hDatamerged.GetBinError(binNo)/(bkgHTmerged.GetBinContent(binNo)))
                else: pullmerged.SetBinContent(binNo,0.)
#        pullmerged.SetMaximum(3)
#        pullmerged.SetMinimum(-3)
#        pullmerged.SetMaximum(2)
#        pullmerged.SetMinimum(0)
        pullmerged.SetFillColor(kGray+2)
        pullmerged.SetLineColor(kGray+2)
        formatLowerHist(pullmerged)
        if pull: pullmerged.Draw("HIST")
        #pullmerged.Draw("E1")

        if 1==1: #not pull:
            BkgOverBkg = pull.Clone("bkgOverbkg")
            BkgOverBkg.Divide(bkgHTmerged, bkgHTmerged)
            pullUncBandTot=TGraphAsymmErrors(BkgOverBkg.Clone("pulluncTot"))
            for binNo in range(1,hDatamerged.GetNbinsX()+1):
                if bkgHTmerged.GetBinContent(binNo)!=0:
                    pullUncBandTot.SetPointEYhigh(binNo-1,bkgHTgerrmerged.GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
                    pullUncBandTot.SetPointEYlow(binNo-1,bkgHTgerrmerged.GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
            pullUncBandTot.SetFillStyle(3002)
            pullUncBandTot.SetFillColor(14)
            pullUncBandTot.SetLineColor(14)
            pullUncBandTot.SetMarkerSize(0)
            gStyle.SetHatchesLineWidth(1)
            pullUncBandTot.Draw("SAME E2")
    #        for binNo in range(1,bkgHTmerged.GetNbinsX()+1):
    #            print(bkgHTmerged.GetBinContent(binNo))
    #        for binNo in range(1,hsig1merged.GetNbinsX()+1):
    #            print(hsig1merged.GetBinContent(binNo))
		
    if Signal: savePrefixMerged = 'PostFitPlots_SpluB/'
    else: savePrefixMerged = 'PostFitPlots/'
    if not os.path.exists(savePrefixMerged): os.system('mkdir -p '+savePrefixMerged)
    savePrefixMerged+=iPlot+'_'+str(lumi).replace('.','p')+'fb_'+chn.replace('isE','isL')
    if blind: savePrefixMerged+='_blind'
    if yLog: savePrefixMerged+='_logy'

    c1merged.SaveAs(savePrefixMerged+".pdf")
    c1merged.SaveAs(savePrefixMerged+".png")

    for proc in bkgProcList:
        try: 
            del bkghistsmerged[chn.replace('isE','isL')+proc]
        except: pass
    del c1merged
