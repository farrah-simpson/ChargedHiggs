#include "step2.cc"
#include "Davismt2.cc"
#include "S2HardcodedConditions.cc"

using namespace std;

void testStep2(){
  TString inputFile=
     "/eos/uscms/store/user/fsimpson/FWLJMET106X_1lep2017UL_step1_new_hadds/nominal/DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root";//tH_tH_x53x53_narrow_MX900_MH200_TuneCP5_13TeV-madgraph-pythia8_hadd.root";
//TTToHadronic_TuneCP5_13TeV-powheg-pythia8_Mtt0to700_hadd.root";
//"tH_tH_x53x53_narrow_MX900_MH200_TuneCP5_13TeV-madgraph-pythia8_hadd.root";
   //"/eos/uscms/store/user/lpcbril/MC_test/FWLJMET106X_1lep2017_UL_step1_reweight_b0_Sys_haddsnominal/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_ttbb_3_hadd.root";
    //"/eos/uscms/store/user/lpcbril/MC_test/FWLJMET106X_1lep2017_UL_step1_reweight_b0_hadds/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root";
    //"/eos/uscms/store/user/lpcbril/MC_test/FWLJMET106X_1lep2017_UL_step1/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8_1.root"; 
    //"/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_031520_step1hadds/nominal/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_hadd.root"; 
//   "/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_121919_step1hadds/nominal/TTToSemiLepton_HT500Njet9_TuneCP5_PSweights_13TeV-powheg-pythia8_ttjj_hadd.root";
//  TString inputFile="/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_121919_step1hadds/nominal/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_HT0Njet0_ttbb_hadd.root";
  TString outputFile="step2test_X53.root";

  gSystem->AddIncludePath("-I$CMSSW_BASE/src/");

  step2 t(inputFile,outputFile);
  t.Loop();
}

