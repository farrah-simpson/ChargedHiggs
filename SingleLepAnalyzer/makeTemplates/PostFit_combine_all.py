#!/usr/bin/env python3

import os, sys, time, math
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
import ROOT as rt
from utils import *
from weights import *

rt.gROOT.SetBatch(1)
start_time = time.time()

# -------------------------
# Basic configuration
# -------------------------
# Usage:
#   python3 PostFit_simple_py3_template_order.py <limitdir> <mass> [Sig] [massH] [iPlot] [doNormByBinWidth:0/1] [calc_pull:0/1]
# Example:
#   python3 PostFit_simple_py3_template_order.py limits_combine_X53 1200 X53

limitdir = sys.argv[1]
massPt = str(sys.argv[2])
Sig = 'X53'

if Sig == 'X53H':
    if len(sys.argv) > 3:
        mH = str(sys.argv[3])

iPlot = 'XGB1300_SR1'
if Sig == 'X53H':
    iPlot = 'XGB'+mH+'_SR1'
if len(sys.argv) > 5:
    iPlot = str(sys.argv[5])

doNormByBinWidth = True
if len(sys.argv) > 6:
    doNormByBinWidth = bool(int(sys.argv[6]))

calc_pull = True
if len(sys.argv) > 7:
    calc_pull = bool(int(sys.argv[7]))

Signal = True
blind = False
blindYLD = False
yLog = True
doBkg = True
doSig = True
doOneBand = True
drawYields = False
scaleSignals = False
scaleFact1 = 1
plotbkg = ''
region = 'SR'
isRebinned = '_postfit_'
saveKey = ''
lumi = '138'
lumiInTemplates = '138'
dataName = 'data_obs'

if Sig == 'X53':
    sig1 = 'X53RHM'+massPt
    sig1leg = 'X_{5/3} (tW, '+massPt+' GeV)'
elif Sig == 'X53H':
    sig1 = 'X53M'+massPt+'MH'+mH
    sig1leg = '#splitline{X_{5/3} #rightarrow tH^{+}}{(m_{X}, m_{H^{+}}) = ('+massPt+', '+mH+') GeV}'


path = os.path.join(limitdir, 'cmb', massPt)
os.chdir(path)

# -------------------------
# Input from postfit shapes
# -------------------------
shapesfile = 'SRPostFitShapes_SplusB.root'
print('shapesfile :', shapesfile)
tFile = rt.TFile.Open(shapesfile)
if not tFile or tFile.IsZombie():
    raise RuntimeError('Could not open '+shapesfile)

allchns = [k.GetName() for k in tFile.GetListOfKeys() if k.GetName().endswith('_postfit')]
print('postfit channels:')
for ch in allchns:
    print('  ', ch)

chn = 'all_postfit'
catStr = 'isL'
histPrefix = iPlot+'_'+lumiInTemplates+'fb_'+catStr

def getCombinedHist(proc, name=None):
    hist = None
    for ch in allchns:
        h = tFile.Get(ch+'/'+proc)
        if not h:
            continue
        if hist is None:
            hist = h.Clone(name if name else proc+'_combined')
            hist.SetDirectory(0)
        else:
            hist.Add(h)
    if hist is None:
        print('Missing all channels for process:', proc)
    return hist

def getCombinedSignal(iPlot, sig1):
    files = {
        'R16APV': f'../../../kinematics_R16APV_final_SR_2025_6_24/templates_{iPlot}_19p52fb_wNegBinsCorrec__rebinned_stat0p2.root',
        'R16':    f'../../../kinematics_R16_final_SR_2025_6_24/templates_{iPlot}_16p81fb_wNegBinsCorrec__rebinned_stat0p2.root',
        'R17':    f'../../../kinematics_R17_final_SR_2025_6_24/templates_{iPlot}_41p48fb_wNegBinsCorrec__rebinned_stat0p2.root',
        'R18':    f'../../../kinematics_R18_final_SR_2025_6_24/templates_{iPlot}_59p83fb_wNegBinsCorrec__rebinned_stat0p2.root',
    }

    channels = [
        'isE_nT0p_nW0p_nB1p_nJ4p',
        'isM_nT0p_nW0p_nB1p_nJ4p',
    ]

    hsig = None

    for year, filepath in files.items():
        f = rt.TFile.Open(filepath)
        if not f or f.IsZombie():
            print(f"Could not open {filepath}")
            continue

        lumi = {
            'R16APV': '19p52',
            'R16': '16p81',
            'R17': '41p48',
            'R18': '59p83',
        }[year]

        for ch in channels:
            hname = f"{iPlot}_{lumi}fb_isSR_{ch}__{sig1}"
            h = f.Get(hname)

            if not h:
                print(f"Missing {hname}")
                continue

            if hsig is None:
                hsig = h.Clone("hsig1_combined_templates")
                hsig.SetDirectory(0)
            else:
                hsig.Add(h)

        f.Close()

    if hsig is None:
        raise RuntimeError("Could not build combined signal from template files")

    return hsig

# -------------------------
# Processes and colors from the template
# -------------------------
bkgProcList = ['qcd','ewk','top','ttbb','ttnobb']
bkgHistColors = {
    'tt2b': rt.kRed-4,
    'ttbb': rt.TColor.GetColor('#964a8b'),
    'tt1b': rt.kRed-3,
    'ttcc': rt.kRed-5,
    'ttjj': rt.kRed-7,
    'top': rt.TColor.GetColor('#5790fc'),
    'ewk': rt.TColor.GetColor('#9c9ca1'),
    'qcd': rt.TColor.GetColor('#f89c20'),
    'ttbar': rt.kRed,
    'ttnobb': rt.TColor.GetColor('#7a21dd'),
}

# -------------------------
# Formatting helpers
# -------------------------
def formatUpperHist(histogram):
    histogram.GetXaxis().SetLabelSize(0)
    if blind:
        histogram.GetXaxis().SetLabelSize(0.05)
        histogram.GetXaxis().SetTitleSize(0.06)
        histogram.GetXaxis().SetTitleOffset(0.95)

        histogram.GetYaxis().SetLabelSize(0.05)
        histogram.GetYaxis().SetTitleSize(0.06)
        histogram.GetYaxis().SetTitleOffset(0.82)

        histogram.GetXaxis().SetNdivisions(506)
    else:
        histogram.GetXaxis().SetLabelSize(0)
        histogram.GetXaxis().SetTitleSize(0)

        histogram.GetYaxis().SetLabelSize(0.036)
        histogram.GetYaxis().SetTitleSize(0.068)
        histogram.GetYaxis().SetTitleOffset(0.72)

        histogram.GetXaxis().SetNdivisions(506)

    histogram.GetYaxis().CenterTitle()
    histogram.SetMinimum(1.0)

    if iPlot == 'ST':
        histogram.GetXaxis().SetRangeUser(500,3000)
    if not yLog:
        histogram.SetMaximum(1.4*histogram.GetMaximum())
    if yLog:
        uPad.SetLogy()
        if not doNormByBinWidth:
            histogram.SetMaximum(500*histogram.GetMaximum())
        else:
            histogram.SetMaximum(2000000*histogram.GetMaximum())
        if region == 'SR':
            histogram.SetMaximum(20*histogram.GetMaximum())
        else:
            histogram.SetMaximum(700*histogram.GetMaximum())

def formatLowerHist(histogram):
    histogram.SetTitle('')
    histogram.GetXaxis().SetLabelSize(.12)
    histogram.GetXaxis().SetTitleSize(0.15)
    histogram.GetXaxis().SetTitleOffset(0.95)
    histogram.GetXaxis().SetNdivisions(506)


    if 'XGB1300_SR1' in iPlot:
        histogram.GetXaxis().SetTitle('BDT score(Mass_{X_{5/3}}= 1300 GeV)')
    elif 'XGB200_SR1' in iPlot:
        histogram.GetXaxis().SetTitle('BDT score(Mass_{H^{\pm}}= 200 GeV)')
    elif 'XGB400_SR1' in iPlot:
        histogram.GetXaxis().SetTitle('BDT score(Mass_{H^{\pm}}= 400 GeV)')
    elif 'XGB600_SR1' in iPlot:
        histogram.GetXaxis().SetTitle('BDT score(Mass_{H^{\pm}}= 600 GeV)')
    elif 'XGB800_SR1' in iPlot:
        histogram.GetXaxis().SetTitle('BDT score(Mass_{H^{\pm}}= 800 GeV)')
    elif 'XGB1000_SR1' in iPlot:
        histogram.GetXaxis().SetTitle('BDT score(Mass_{H^{\pm}}= 1000 GeV)')

    if calc_pull:
        histogram.GetXaxis().SetLabelSize(0.011)
        histogram.GetXaxis().SetTitleSize(0.18)
        histogram.GetXaxis().SetTitleOffset(0.90)
        
        histogram.GetYaxis().SetLabelSize(0.11)
        histogram.GetYaxis().SetTitleSize(0.16)
        histogram.GetYaxis().SetTitleOffset(0.32)
        
        histogram.GetYaxis().SetTitle('#frac{(Data-Bkg)}{Error}')#sqrt{bkg-#sigma_{bkg}^{2}}}')
        histogram.GetYaxis().SetNdivisions(7)
        histogram.GetYaxis().SetRangeUser(-3.99,3.99)
    else:
        histogram.GetYaxis().SetLabelSize(0.065)
        histogram.GetYaxis().SetTitleSize(0.15)
        histogram.GetYaxis().SetTitleOffset(.37)
        histogram.GetYaxis().SetTitle('#frac{Data}{Bkg+Sig}')
        histogram.GetYaxis().SetNdivisions(5)
        histogram.GetYaxis().SetRangeUser(0.01,1.99)
    histogram.GetYaxis().CenterTitle()

# -------------------------
# Canvas dimensions from the template
# -------------------------
H_ref = 600
W_ref = 800
W = W_ref
H = H_ref

T = 0.10*H_ref
B = 0.35*H_ref 
if blind == True: B = 0.12*H_ref
L = 0.12*W_ref #0.12*W_ref
R = 0.04*W_ref#0.49*W_ref #0.49 0.38*W_ref

bkghists = {}
totBkgTemp1 = {}
totBkgTemp2 = {}
totBkgTemp3 = {}

# ============================================================
# Template ordering preserved:
# 1. load hists
# 2. normByBinWidth, if requested
# 3. build bkgHT and error band
# 4. apply plotting signal scale
# 5. stack/style
# 6. canvas/draw in template order
# 7. ratio/pull
# ============================================================

# 1. Load inputs
for proc in bkgProcList:
    bkghists[proc+catStr] = getCombinedHist(proc, proc+catStr)
    if bkghists[proc+catStr] is None:
        raise RuntimeError('Missing histogram for '+proc)

hData = getCombinedHist(dataName, dataName+catStr)
if hData is None:
    raise RuntimeError('Missing data_obs')

hsig1 = getCombinedSignal(iPlot, sig1)
hsig1.Scale(xsec[sig1])
if hsig1 is None:
    raise RuntimeError('Missing signal '+sig1)

hData_forPull = hData.Clone("hData_forPull")

bkgHT_forPull = None
for proc in bkgProcList:
    try:
        if bkgHT_forPull is None:
            bkgHT_forPull = bkghists[proc+catStr].Clone("bkgHT_forPull")
        else:
            bkgHT_forPull.Add(bkghists[proc+catStr])
    except:
        pass

if bkgHT_forPull is None:
    raise RuntimeError("bkgHT_forPull was never built!")

# 2. Normalize by bin width before building bkgHT, exactly like the template
if doNormByBinWidth:
    for proc in bkgProcList:
        try:
            normByBinWidth(bkghists[proc+catStr])
        except Exception:
            pass
    normByBinWidth(hsig1)
    normByBinWidth(hData)

# 3. Build total background and error band after normalization
bkgHT = bkghists[bkgProcList[0]+catStr].Clone('bkgHT')
for proc in bkgProcList:
    if proc == bkgProcList[0]:
        continue
    #try:
    bkgHT.Add(bkghists[proc+catStr])
    #except Exception:
    #    pass

totBkgTemp1[catStr] = rt.TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapeOnly'))
totBkgTemp2[catStr] = rt.TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapePlusNorm'))
totBkgTemp3[catStr] = rt.TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'All'))

for ibin in range(1,bkgHT.GetNbinsX()+1):
    errorStatOnly = bkgHT.GetBinError(ibin)**2
    totBkgTemp1[catStr].SetPointEYhigh(ibin-1,0.)
    totBkgTemp1[catStr].SetPointEYlow(ibin-1,0.)
    totBkgTemp2[catStr].SetPointEYhigh(ibin-1,0.)
    totBkgTemp2[catStr].SetPointEYlow(ibin-1,0.)
    totBkgTemp3[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorStatOnly))
    totBkgTemp3[catStr].SetPointEYlow(ibin-1,math.sqrt(errorStatOnly))

bkgHTgerr = totBkgTemp3[catStr].Clone("bkgHTgerrPostFit")
#bkgHTgerr = rt.TGraphAsymmErrors(bkgHT.Clone("bkgHTgerrPostFit"))

# 4. Apply plotting signal scale after bkgHT/errors, as in the template
if not scaleSignals:
    scaleFact1 = 1
hsig1.Scale(scaleFact1)

# 5. Stack and style

drawQCD = False
try:
    drawQCD = bkghists['qcd'+catStr].Integral()/bkgHT.Integral() > .005
except Exception:
    pass

stackbkgHT = rt.THStack('stackbkgHT','')
for proc in bkgProcList:
    try:
        if drawQCD or proc != 'qcd':
            stackbkgHT.Add(bkghists[proc+catStr])
    except Exception:
        pass

sig1Color = rt.kBlack
for proc in bkgProcList:
    try:
        bkghists[proc+catStr].SetLineColor(bkgHistColors[proc])
        bkghists[proc+catStr].SetFillColor(bkgHistColors[proc])
        bkghists[proc+catStr].SetLineWidth(2)
    except Exception:
        pass

hsig1.SetLineColor(sig1Color)
hsig1.SetFillStyle(0)
hsig1.SetLineWidth(3)

if not drawYields:
    hData.SetMarkerStyle(20)
hData.SetMarkerSize(1.2)
hData.SetMarkerColor(rt.kBlack)
hData.SetLineWidth(2)
hData.SetLineColor(rt.kBlack)
if drawYields:
    hData.SetMarkerSize(4)

c1 = rt.TCanvas('c1','c1',50,50,W,H)
c1.SetFillColor(0)
c1.SetBorderMode(0)
c1.SetFrameFillStyle(0)
c1.SetFrameBorderMode(0)
c1.SetTickx()
c1.SetTicky()

uMargin = 0.00001
if blind: uMargin = 0.12
rMargin=.06

yDiv=0.25#0.35
if blind == True: yDiv=0.01#0.0
uPad=rt.TPad("uPad","",0,yDiv,1,1) #for actual plots

if yLog and not blind: 
    uPad=rt.TPad("uPad","",0,yDiv-0.009,1,1) #for actual plots
else: uPad=rt.TPad("uPad","",0,yDiv,1,1) #for actual plots

uPad.SetLeftMargin( L/W )#(.105)#( L/W )
uPad.SetRightMargin( R/W )#(rMargin)#( R/W )
uPad.SetTopMargin( T/H )#(0.08)#( T/H )
uPad.SetBottomMargin(0)
#if blind == True: uPad.SetBottomMargin( B/H )

uPad.SetFillColor(0)
uPad.SetBorderMode(0)
uPad.SetFrameFillStyle(0)
uPad.SetFrameBorderMode(0)
#uPad.SetTickx(0)
#uPad.SetTicky(0)
uPad.SetTickx()
uPad.SetTicky()
uPad.Draw()

if blind == False:
    lPad=rt.TPad("lPad","",0,0,1,yDiv) #for sigma runner

    lPad.SetFixedAspectRatio()
    lPad.SetLeftMargin( L/W )#(.105)#( L/W )
    lPad.SetRightMargin( R/W )#(rMargin)#( R/W )
    lPad.SetTopMargin( 0.01 )#(T/H)#( 0 )
    lPad.SetBottomMargin( (B/H)+0.04 )#(.4)#( B/H )

    lPad.SetGridy()
    lPad.SetFillColor(0)
    lPad.SetBorderMode(0)
    lPad.SetFrameFillStyle(0)
    lPad.SetFrameBorderMode(0)

    lPad.SetTickx()
    lPad.SetTicky()
    lPad.Draw()


for ibin in range(1, bkgHT.GetNbinsX()+1):
    print(
        ibin,
        "bkg =", bkgHT.GetBinContent(ibin),
        "bkg err =", bkgHT.GetBinError(ibin),
        "graph err =", bkgHTgerr.GetErrorYhigh(ibin-1)
    )
if not doNormByBinWidth:
    hData.SetMaximum(1.6*max(hData.GetMaximum(),bkgHT.GetMaximum()))

if doNormByBinWidth:
    hData.GetYaxis().SetTitle('< Events / GeV >')
    if 'XGB' in iPlot:
        hData.GetYaxis().SetTitle('< Events / 1.0 units >')
elif isRebinned != '':
    hData.GetYaxis().SetTitle('Events / bin')
else:
    hData.GetYaxis().SetTitle('Events / bin')

formatUpperHist(hData)
uPad.cd()
hData.SetTitle('')
stackbkgHT.SetTitle('')

if not blind:
    hData.Draw('esamex0')
if blind:
    hsig1.SetMinimum(0.1)
    if doNormByBinWidth:
        hsig1.GetYaxis().SetTitle('< Events / GeV >')
        if 'XGB' in iPlot:
            hsig1.GetYaxis().SetTitle('< Events / 1.0 units >')
    elif isRebinned != '':
        hsig1.GetYaxis().SetTitle('Events / bin')
    else:
        hsig1.GetYaxis().SetTitle('Events / bin')
    formatUpperHist(hsig1)
    hsig1.SetMaximum(1.6*hData.GetMaximum())
    hsig1.Draw('SAME HIST')

bkgHTgerr.SetFillStyle(3004)
bkgHTgerr.SetFillColor(rt.kBlack)
bkgHTgerr.SetLineColor(rt.kBlack)
bkgHTgerr.SetMarkerSize(0)

if doBkg:
    stackbkgHT.Draw("SAME HIST")

if doSig:
    hsig1.Draw("SAME HIST")

if doBkg:
    bkgHTgerr.Draw("SAME E2")

if not blind:
    hData.Draw("esamex0")

uPad.RedrawAxis()

rt.gStyle.SetOptTitle(0)
rt.gStyle.SetOptStat(0)

# Labels, without CMS_lumi dependency
chLatex = rt.TLatex()
chLatex.SetNDC()
chLatex.SetTextSize(0.04)
chLatex.SetTextAlign(21)
tagPosX = 0.88
tagPosY = 0.6
chLatex.DrawLatex(tagPosX, tagPosY, 'e/#mu+jets')
#chLatex.DrawLatex(tagPosX, tagPosY-0.06, 'post-fit')

leg = rt.TLegend(0.33,0.41,0.92,0.88)
leg.SetShadowColor(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetLineColor(0)
leg.SetLineStyle(0)
leg.SetBorderSize(0)
leg.SetNColumns(2)
leg.SetTextFont(42)

scaleFact1Str = ' x'+str(scaleFact1)
if not scaleSignals:
    scaleFact1Str = ''

if not blind:
    leg.AddEntry(hData,'Data','ep')
if doBkg:
    try: leg.AddEntry(bkghists['ewk'+catStr],'EW','f')
    except Exception: pass
    try: leg.AddEntry(bkghists['ttnobb'+catStr],'t#bar{t}+non-b#bar{b}','f')
    except Exception: pass
    try: leg.AddEntry(bkghists['qcd'+catStr],'QCD','f')
    except Exception: pass
    try: leg.AddEntry(bkghists['ttbb'+catStr],'t#bar{t}+b#bar{b}','f')
    except Exception: pass
    leg.AddEntry(bkgHTgerr,'Bkg uncert','f')
    try: leg.AddEntry(bkghists['top'+catStr],'other top','f')
    except Exception: pass
    if doSig:
        leg.AddEntry(hsig1,sig1leg+scaleFact1Str,'l')
 
leg.SetTextSize(0.035)
leg.Draw('same')

prelimTex = rt.TLatex()
prelimTex.SetNDC()
prelimTex.SetTextAlign(31)
prelimTex.SetTextFont(42)
prelimTex.SetTextSize(0.06)#5)
prelimTex.SetLineWidth(2)
prelimTex.DrawLatex(0.94,0.94,str(lumi)+' fb^{-1} (13 TeV)')

prelimTex2 = rt.TLatex()
prelimTex2.SetNDC()
prelimTex2.SetTextFont(61)
prelimTex2.SetLineWidth(2)
prelimTex2.SetTextSize(0.08)#(0.059)#0.08
prelimTex2.DrawLatex(0.12,0.93,'CMS')

prelimTex3 = rt.TLatex()
prelimTex3.SetNDC()
prelimTex3.SetTextAlign(12)
prelimTex3.SetTextFont(52)
prelimTex3.SetTextSize(0.0608)#454)#55)
prelimTex3.SetLineWidth(2)
prelimTex3.DrawLatex(0.23,0.945,'Preliminary')

uPad.Update()
uPad.RedrawAxis()
uPad.Draw()

# 7. Pull/ratio plot from the simple script
if not blind:
    lPad.cd()
    pull = hData.Clone('pull')

    if calc_pull:
        pull = hData_forPull.Clone("pull")
        bkgPullErr = rt.TGraphAsymmErrors(bkgHT_forPull.Clone("bkgPullErr"))
    
        for binNo in range(1, hData_forPull.GetNbinsX()+1):
            MCerror = bkgPullErr.GetErrorYlow(binNo-1)
            if hData_forPull.GetBinContent(binNo) > bkgHT_forPull.GetBinContent(binNo):
                MCerror = bkgPullErr.GetErrorYhigh(binNo-1)
    
            if bkgHT_forPull.GetBinContent(binNo) > MCerror**2:
                pull.SetBinContent(
                    binNo,
                    (hData_forPull.GetBinContent(binNo)-bkgHT_forPull.GetBinContent(binNo))
                    / math.sqrt(bkgHT_forPull.GetBinContent(binNo)-MCerror**2)
                )
            else:
                pull.SetBinContent(binNo, 0.)
    
            pull.SetBinError(binNo, 0.)

    else:
        denom = bkgHT.Clone('denom_bkg_plus_sig')
        if doSig:
            denom.Add(hsig1)
        pull.Divide(hData, denom)
        for binNo in range(1,hData.GetNbinsX()+1):
            if denom.GetBinContent(binNo) != 0:
                pull.SetBinError(binNo,hData.GetBinError(binNo)/denom.GetBinContent(binNo))
            else:
                pull.SetBinContent(binNo,0.)
                pull.SetBinError(binNo,0.)

    pull.SetFillColor(rt.kGray+2 if calc_pull else rt.kBlack)
    pull.SetLineColor(rt.kGray+2 if calc_pull else rt.kBlack)
    formatLowerHist(pull)
    if calc_pull:
        pull.Draw('HIST')
    else:
        pull.Draw('E1')

    if not calc_pull:
        BkgOverBkg = denom.Clone('bkgOverbkg')
        BkgOverBkg.Divide(denom, denom)
        pullUncBandTot = rt.TGraphAsymmErrors(BkgOverBkg.Clone('pulluncTot'))
        for binNo in range(1,hData.GetNbinsX()+1):
            if denom.GetBinContent(binNo) != 0:
                #pullUncBandTot.SetPointEYhigh(binNo-1,bkgHTgerr.GetErrorYhigh(binNo-1)/denom.GetBinContent(binNo))
                #pullUncBandTot.SetPointEYlow(binNo-1,bkgHTgerr.GetErrorYlow(binNo-1)/denom.GetBinContent(binNo))
                scaleErr = 1.0
                pullUncBandTot.SetPointEYhigh(binNo-1, scaleErr*bkgHTgerr.GetErrorYhigh(binNo-1)/denom.GetBinContent(binNo))
                pullUncBandTot.SetPointEYlow(binNo-1, scaleErr*bkgHTgerr.GetErrorYlow(binNo-1)/denom.GetBinContent(binNo))
        pullUncBandTot.SetFillStyle(3002)
        pullUncBandTot.SetFillColor(14)
        pullUncBandTot.SetLineColor(14)
        pullUncBandTot.SetMarkerSize(0)
        rt.gStyle.SetHatchesLineWidth(1)
        pullUncBandTot.Draw('SAME E2')
        pull.Draw('SAME E1')

    lPad.RedrawAxis()

savePrefix = 'plots_Run2/'
if not os.path.exists(savePrefix):
    os.system('mkdir '+savePrefix)
savePrefix += histPrefix+isRebinned.replace('_rebinned_stat1p1','')+saveKey
if calc_pull: savePrefix += '_pull'
if doNormByBinWidth: savePrefix += '_NBBW'
if yLog: savePrefix += '_logy'
if blind or blindYLD: savePrefix += '_blind'
c1.Update()

if doOneBand:
    c1.SaveAs(savePrefix+plotbkg+'totBand.pdf')
    c1.SaveAs(savePrefix+plotbkg+'totBand.png')
else:
    c1.SaveAs(savePrefix+plotbkg+'.pdf')
    c1.SaveAs(savePrefix+plotbkg+'.png')

tFile.Close()
print('--- %s minutes ---' % (round(time.time() - start_time, 2)/60))

