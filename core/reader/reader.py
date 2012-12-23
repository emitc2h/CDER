from ROOT import TTree, TFile, gROOT

gROOT.ProcessLine('.L addVectorToROOT.C+')

import random as rand
import copy

from ..particle.jet import Jet
from ..particle.tau import Tau
from ..particle.electron import Electron
from ..particle.muon import Muon
from ..particle.photon import Photon
from ..particle.met import MET


class Reader():

    def __init__(self, file_path, tree_name):

        ## Load the file
        self.file = TFile(file_path)

        ## Load the tree
        self.tree = self.file.Get(tree_name)

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
        
        if self.event > 1:
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


    def extra_information(self):
        pass
        

    def make_particles(self):
        
        for jet in self.event_jets:
            btag = False
            try:
                btag = jet[3]
            except IndexError:
                pass
            new_jet = Jet(jet[0], jet[1], jet[2], btag)
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
            

    def print_event(self):

        print '===='*13
        print 'Event   : {:<41d}|'.format(self.event)
        
        print '----'*13
        print 'object   | {:<12}| {:<12}| {:<12}|'.format('pt [GeV]', 'eta', 'phi')
        print '----'*13

        for el in self.event_electrons:
            print '\033[34melectron\033[0m | {:<12.2f}| {:<12.2f}| {:<12.2f}|'.format(el[0]/1000.0,
                                                                                      el[1],
                                                                                      el[2])

        for mu in self.event_muons:
            print '\033[35mmuon\033[0m     | {:<12.2f}| {:<12.2f}| {:<12.2f}|'.format(mu[0]/1000.0,
                                                                                      mu[1],
                                                                                      mu[2])
        
        for tau in self.event_taus:
            print '\033[33mtau\033[0m      | {:<12.2f}| {:<12.2f}| {:<12.2f}|'.format(tau[0]/1000.0,
                                                                                      tau[1],
                                                                                      tau[2])

        for ph in self.event_photons:
            print '\033[34mphoton\033[0m   | {:<12.2f}| {:<12.2f}| {:<12.2f}|'.format(ph[0]/1000.0,
                                                                                      ph[1],
                                                                                      ph[2])

        for jet in self.event_jets:
            try:
                if jet[3]:
                    print '\033[36mjet\033[0m      | {:<12.2f}| {:<12.2f}| {:<12.2f}|'.format(jet[0]/1000.0,
                                                                                              jet[1],
                                                                                              jet[2])
                else:
                    print '\033[31mjet\033[0m      | {:<12.2f}| {:<12.2f}| {:<12.2f}|'.format(jet[0]/1000.0,
                                                                                              jet[1],
                                                                                              jet[2])
                        
            except IndexError:
                print '\033[31mjet\033[0m      | {:<12.2f}| {:<12.2f}| {:<12.2f}|'.format(jet[0]/1000.0,
                                                                                          jet[1],
                                                                                          jet[2])

        try:
            print '\033[32mMET\033[0m      | {:<12.2f}| {:<12}| {:<12.2f}|'.format(self.event_met[0]/1000.0,
                                                                                   '----', 
                                                                                   self.event_met[1])
        except IndexError:
            pass

        print '----'*13
        print

