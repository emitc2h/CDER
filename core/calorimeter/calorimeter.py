import math

####################################################
## An assemblage of rings making a calorimeter    ##
## component                                      ##
####################################################
CALO_EM  = 'em'
CALO_HAD = 'had'
class Calorimeter():

    def __init__(self):
        """
        Constructor
        """

        self.rings = []
        self.theta_camera = 0.0
        self.r_camera = 0.0
        self.phi_camera = 0.0
        self.transparency = 0.1
        self.modified_cells = []
        self.calo_type = None


    def draw(self):

        ## Calculate the perspective y angle with respect to transverse plane
        a = abs(self.theta_camera)-math.pi/2

        ## Draw negative side rings
        for ring in self.rings:

            ## Find out where the camera is looking at in a perpendicular direction to the beamline
            split_angle = math.atan2(ring.radius_outer,
                                     -self.r_camera*math.sin(a)) - math.pi/2

            ## Draw all rings after that point
            if ring.y_angle > split_angle:
                ring.phi_camera = self.phi_camera
                ring.draw()

        ## Draw negative side rings
        for ring in reversed(self.rings):

            ## Find out where the camera is looking at in a perpendicular direction to the beamline
            split_angle = math.atan2(ring.radius_outer,
                                     -self.r_camera*math.sin(a)) - math.pi/2

            ## Draw all rings before that point
            if ring.y_angle < split_angle:
                ring.phi_camera = self.phi_camera
                ring.draw()

        ## If looking straight in the middle, draw the middle ring at the end
        n_rings = len(self.rings)
        if a == 0.0 and n_rings%2 > 0:
            self.rings[n_rings/2].draw()
    
            
    def update(self, dt):

        for ring in self.rings:
            ring.update(dt)


    def energize(self, particles):
        
        for particle in particles:
            target_cells = []
            for ring in self.rings:
                for cell in ring.cells:
                    if particle.isEM and self.calo_type == CALO_EM or \
                      particle.isHAD and self.calo_type == CALO_HAD:
                        if particle.in_barrel:
                            dphi = particle.dphi(cell)
                            if particle.r < cell.radius_outer and particle.r > cell.radius_inner and \
                              dphi < cell.phi_width/1.8:
                                target_cells.append(cell)
                        else:
                            deta = particle.deta(cell)
                            dphi = particle.dphi(cell)
                            if deta < cell.eta_width/1.7 and dphi < cell.phi_width/1.8:
                                target_cells.append(cell)
                        
            pt = math.log(particle.pt/10000.0)
            for cell in target_cells:
                dR   = particle.dR(cell)
                max_transparency = 0.7
                if self.calo_type == CALO_HAD:
                    max_transparency = 0.2
                cell.transparency += (max_transparency - cell.transparency)*(pt/(pt + 1))*(1/(dR+1))
                cell.build()
                self.modified_cells.append(cell)


    def reset(self):
        for cell in self.modified_cells:
            cell.transparency = self.transparency
            cell.build()
        self.modified_cells = []
