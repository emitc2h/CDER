#**************************************************#
# file   : core/reader/lhprocessor_reader.py       #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# A reader to read LHProcessor.*.root files        #
#**************************************************#

## ROOT imports
from ROOT import gROOT

## CDER imports
from reader import Reader

## Enable ROOT to read std::vectors
gROOT.ProcessLine('.L core/reader/addVectorToROOT.C+')

####################################################
class Custom_Reader(Reader):

    ## --------------------------------------- ##
    def __init__(self, file_path, tree_name):
        """
        Constructor
        """
        
        Reader.__init__(self, file_path, tree_name)


        
    ## --------------------------------------- ##
    def get_jets(self):
        """
        Jets
        """
        
        njets = len( self.tree.jet_fourvect )
        for i in range(njets):
            jet = self.tree.jet_fourvect[i]
            btag = (self.tree.jet_btag[i] > 0.722)
            self.event_jets.append((jet.Pt(), jet.Eta(), jet.Phi(), btag))


            
    ## --------------------------------------- ##
    def get_taus(self):
        """
        Taus
        """
        
        tau = self.tree.tau_fourvect
        self.event_taus.append((tau.Pt(), tau.Eta(), tau.Phi()))


        
    ## --------------------------------------- ##
    def get_muons(self):
        """
        Muons
        """
        
        lep_type = self.tree.lep_leptype
        if self.tree.lep_leptype == 0:
            mu = self.tree.lep_fourvect
            self.event_muons.append((mu.Pt(), mu.Eta(), mu.Phi()))


            
    ## --------------------------------------- ##
    def get_electrons(self):
        """
        Electrons
        """
        
        lep_type = self.tree.lep_leptype
        if self.tree.lep_leptype == 1:
            el = self.tree.lep_fourvect
            self.event_electrons.append((el.Pt(), el.Eta(), el.Phi()))


            
    ## --------------------------------------- ##
    def get_photons(self):
        """
        Photons (no photons in this analysis)
        """
        
        return


    
    ## --------------------------------------- ##
    def get_met(self):
        """
        MET
        """
        
        self.event_met = (self.tree.MET_vect.Mod(), self.tree.MET_vect.Phi())


        
    ## --------------------------------------- ##
    def get_extra_information(self):
        """
        Extra information
        """

        ## Sphericity
        self.extra_information['sphericity'] = (self.tree.sphericity, '.3f')

        ## Met Phi Centrality
        self.extra_information['MET phi centrality'] = (self.tree.met_phi_centrality, '.3f')

        ## Resonance Pt
        self.extra_information['tau-lep resonance Pt'] = (self.tree.resonance_pt_tau_lep, '.3f')

        ## dR
        self.extra_information['tau-lep dR'] = (self.tree.dr_tau_lep, '.3f')

        ## MMC mass
        self.extra_information['tau-lep MMC mass'] = (self.tree.mass_mmc_tau_lep, '.3f')

        ## transverse mass
        self.extra_information['MET-lep transverse mass'] = (self.tree.mass_transverse_met_lep/1000.0, '.3f')

        ## lepton eta centrality
        self.extra_information['Lepton eta centrality'] = (self.tree.lep_centrality_j1_j2, '.3f')

        ## Mjj
        self.extra_information['VBF jets mass'] = (self.tree.mass_j1_j2/1000.0, '.3f')

        ## eta product
        self.extra_information['VBF jets eta product'] = (self.tree.eta_product_j1_j2, '.3f')

        ## eta delta
        self.extra_information['VBF jets eta delta'] = (self.tree.eta_delta_j1_j2, '.3f')

        ## sum Pt
        self.extra_information['Scalar sum visible Pt'] = (self.tree.sumPt/1000.0, '.3f')


            
