#include "step1.cc"
#include "BTagCalibForLJMet.cpp"
#include "HardcodedConditions.cc"
#include<vector>
using namespace std;

void testStep1(){
 // TString inputFile="root://cmseos.fnal.gov//store/user/lpcljm/FWLJMET102X_1lep2017_Oct2019/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/singleLep2017/191029_235508/0000/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_59.root";
  TString inputFile="root://cmseos.fnal.gov//store/user/lpcljm/FWLJMET102X_1lep2017UL_X53/tH_tH_x53x53_narrow_MX1000_MH400_TuneCP5_13TeV-madgraph-pythia8/singleLep2017/210905_184256/0000/tH_tH_x53x53_narrow_MX1000_MH400_TuneCP5_13TeV-madgraph-pythia8_12.root";//"root://cmseos.fnal.gov//store/group/lpcljm/FWLJMET_crab_1lep2017_UL_fixed_new/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/singleLep2017_TTTo2L2Nu_fixed/210622_015054/0000/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_90.root";
//  TString inputFile="root://cmseos.fnal.gov//store/user/lpcljm/FWLJMET102X_1lep2018_Oct2019/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/singleLep2018/191121_205009/0001/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8_1664.root";
  TString outputFile="test.root";
  Int_t Year=2017;
  
  gSystem->AddIncludePath("-I$CMSSW_BASE/src/");
  
  if ( inputFile.Contains("Run2017") || inputFile.Contains("Run2018") || inputFile.Contains("Single") || inputFile.Contains("Double") || inputFile.Contains("MuonEG") || inputFile.Contains("EGamma") || inputFile.Contains("JetHT") ) { 
    step1 t(inputFile,outputFile.ReplaceAll(".root","nominal.root"),Year);
    t.Loop("ljmet", "ljmet"); 
    }

  else {
    vector<TString> shifts = { "nominal" };//, "JECup", "JECdown", "JERup", "JERdown" };
    for (size_t i =0; i<shifts.size(); ++i) {
      cout << endl << "Running shift " << shifts[i] << endl;
      TString tName = "ljmet";
      if ( !shifts[i].Contains("nominal") ) { tName.Append("_"); tName.Append(shifts[i]); }
      step1 t(inputFile,outputFile.ReplaceAll(".root",shifts[i].Append(".root")),Year); //"shifts[i]" is now changed to "shifts[i].root"
      t.saveHistograms();
      t.Loop(tName, "ljmet");
      outputFile.ReplaceAll(shifts[i],".root"); //Change outputFile back to its original name.
      }
    }

}
