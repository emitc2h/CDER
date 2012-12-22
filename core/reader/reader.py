from ROOT import TTree, TFile, gROOT

gROOT.ProcessLine('.L addVectorToROOT.C+')

import random as rand

from ..particle.jet import Jet
from ..particle.tau import Tau
from ..particle.electron import Electron
from ..particle.muon import Muon
from ..particle.photon import Photon
from ..particle.met import MET


class Reader():

    def __init__(self, file_path, tree_name, cut_string):

        ## Load the file
        self.file = TFile(file_path)

        ## Load the tree
        self.tree = self.file.Get(tree_name)

        ## Apply cuts
        #self.tree = self.full_tree.CopyTree(cut_string)

        ## Tree navigation
        self.entries = self.tree.GetEntries()
        self.event = 0

        ## Particles to display
        self.event_particles = []

        ## particle data holders
        self.event_jets      = []
        self.event_taus      = []
        self.event_electrons = []
        self.event_muons     = []
        self.event_photons   = []
        self.event_met       = None


    def reset(self):
        ## Empty the event particles
        self.event_particles = []

        ## Empty particle data holders
        self.event_jets      = []
        self.event_taus      = []
        self.event_electrons = []
        self.event_muons     = []
        self.event_photons   = []
        self.event_met       = None
        

    def next(self):

        self.reset()
        
        if self.event < self.entries:
            self.event += 1
            self.tree.GetEntry(self.event)

        ## Get new particle kinematics
        self.get_particles()
        self.make_particles()

        return self.event_particles
        

            
    def previous(self):

        self.reset()
        
        if self.event > 0:
            self.event -= 1
            self.tree.GetEntry(self.event)

        ## Get new particle kinematics
        self.get_particles()
        self.make_particles()

        return self.event_particles


    def random(self):

        self.reset()
        
        self.event = rand.randint(0, self.entries)
        self.tree.GetEntry(self.event)

        ## Get new particle kinematics
        self.get_particles()
        self.make_particles()

        return self.event_particles

        
    def get_jets(self):
        print 'WARNING : get_jets() method not imlemented in current Reader'

    def get_taus(self):
        print 'WARNING : get_taus() method not imlemented in current Reader'

    def get_electrons(self):
        print 'WARNING : get_electrons() method not imlemented in current Reader'

    def get_muons(self):
        print 'WARNING : get_muons() method not imlemented in current Reader'

    def get_photons(self):
        print 'WARNING : get_photons() method not imlemented in current Reader'

    def get_met(self):
        print 'WARNING : get_met() method not imlemented in current Reader'

    def get_particles(self):
        self.get_jets()
        self.get_taus()
        self.get_electrons()
        self.get_muons()
        self.get_photons()
        self.get_met()
        

    def make_particles(self):
        
        for jet in self.event_jets:
            new_jet = Jet(jet[0], jet[1], jet[2])
            self.event_particles += new_jet.particles

        for tau in self.event_taus:
            new_tau = Tau(tau[0], tau[1], tau[2])
            self.event_particles += new_tau.particles

        for el in self.event_electrons:
            new_el = Electron(el[0], el[1], el[2])
            self.event_particles += new_el.particles

        for mu in self.event_muons:
            new_mu = Muon(mu[0], mu[1], mu[2])
            self.event_particles += new_mu.particles

        for ph in self.event_photons:
            new_ph = Photon(ph[0], ph[1], ph[2])
            self.event_particles += new_ph.particles

        try:
            met = MET(self.event_met[0], self.event_met[1])
            self.event_particles += met.particles
        except TypeError:
            pass
            

