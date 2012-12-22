from reader import Reader

class LHProcessor_Reader(Reader):

    def __init__(self, file_path, tree_name, cut_string):
        Reader.__init__(self, file_path, tree_name, cut_string)

    def get_jets(self):
        for jet in self.tree.jet_fourvect:
            self.event_jets.append((jet.Pt(), jet.Eta(), jet.Phi()))

    def get_taus(self):
        tau = self.tree.tau_fourvect
        self.event_taus.append((tau.Pt(), tau.Eta(), tau.Phi()))

    def get_muons(self):
        lep_type = self.tree.lep_leptype
        if self.tree.lep_leptype == 0:
            mu = self.tree.lep_fourvect
            self.event_muons.append((mu.Pt(), mu.Eta(), mu.Phi()))

    def get_electrons(self):
        lep_type = self.tree.lep_leptype
        if self.tree.lep_leptype == 1:
            el = self.tree.lep_fourvect
            self.event_electrons.append((el.Pt(), el.Eta(), el.Phi()))

    def get_photons(self):
        return

    def get_met(self):
        self.event_met = (self.tree.MET_vect.Mod(), self.tree.MET_vect.Phi())


            
