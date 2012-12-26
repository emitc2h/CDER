## Enable ROOT to read vectors
from ROOT import gROOT
gROOT.ProcessLine('.L core/reader/addVectorToROOT.C+')

## Define accessors
from reader import Reader
class Custom_Reader(Reader):

    def __init__(self, file_path, tree_name):
        Reader.__init__(self, file_path, tree_name)

    def get_jets(self):
        for i in range(len(self.tree.jet_pt)):
            self.event_jets.append((self.tree.jet_pt[i],
                                    self.tree.jet_eta[i],
                                    self.tree.jet_phi[i],
                                    self.tree.jet_btag[i]))

    def get_taus(self):
        for i in range(len(self.tree.tau_pt)):
            self.event_taus.append((self.tree.tau_pt[i],
                                    self.tree.tau_eta[i],
                                    self.tree.tau_phi[i]))

    def get_muons(self):
        for i in range(len(self.tree.mu_pt)):
            self.event_muons.append((self.tree.mu_pt[i],
                                     self.tree.mu_eta[i],
                                     self.tree.mu_phi[i]))

    def get_electrons(self):
        for i in range(len(self.tree.el_pt)):
            self.event_electrons.append((self.tree.el_pt[i],
                                         self.tree.el_eta[i],
                                         self.tree.el_phi[i]))

    def get_photons(self):
        for i in range(len(self.tree.ph_pt)):
            self.event_photons.append((self.tree.ph_pt[i],
                                       self.tree.ph_eta[i],
                                       self.tree.ph_phi[i]))

    def get_met(self):
        for i in range(len(self.tree.MET)):
            self.event_met = (self.tree.MET[i], self.tree.MET_phi[0])

    def get_extra_information(self):
        nFlebles = 0
        for i in range(len(self.tree.Flebles)):
            nFlebles += self.tree.Flebles[i]

        self.extra_information['flebles'] = (nFlebles, 'd')

            


            
