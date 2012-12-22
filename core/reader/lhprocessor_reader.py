from reader import Reader

class LHProcessor_Reader(Reader):

    def get_jets(self):
        for jet in self.tree.jet_fourvect:
            self.event_jets.append((jet.pt, jet.eta, jet.phi))
