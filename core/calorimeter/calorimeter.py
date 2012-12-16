import math

####################################################
## An assemblage of rings making a calorimeter    ##
## component                                      ##
####################################################

class Calorimeter():

    def __init__(self):
        """
        Constructor
        """

        self.rings = []
        self.theta_camera = 0.0
        self.r_camera = 0.0
        self.phi_camera = 0.0


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
