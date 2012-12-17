from pyglet.gl import *
from ..utils import *
import math

####################################################
## A simple polyhedron with 8 faces that serves   ##
## as the basic calorimeter cell. Arrange several ##
## of these to determine calormeter geometry      ##
####################################################

## Geometry types
GEO_PROJECTIVE  = 'projective'
GEO_CYLINDRICAL = 'cylindrical'

class Cell():

    def __init__(self, parameters, geometry, color_inner, color_outer, transparency=0.3):
        """
        Constructor
        """

        n_parameters = len(parameters)
        if n_parameters != 6:
            raise ValueError('There should be 6 parameters to define the cell. Only %d provided' % n_parameters)

        self.geometry = geometry
        
        if self.geometry == GEO_PROJECTIVE:
            self.radius_inner = parameters[0]
            self.radius_outer = parameters[1]
            self.eta_center   = parameters[2]
            self.eta_width    = parameters[3]
            self.phi_center   = parameters[4]
            self.phi_width    = parameters[5]
            self.calculate_coordinates_projective()

        elif self.geometry == GEO_CYLINDRICAL:
            self.radius_inner = parameters[0]
            self.radius_outer = parameters[1]
            self.z_center     = parameters[2]
            self.z_width      = parameters[3]
            self.phi_center   = parameters[4]
            self.phi_width    = parameters[5]
            self.calculate_coordinates_cylindrical()

        self.color_outer = color_outer #(0.2, 0.4, 0.7)
        self.color_inner = color_inner #(0.1, 0.2, 0.35)
        self.transparency = transparency

        self.distance = 0.0

        self.display_list = None
        self.build()

            
    def calculate_coordinates_projective(self):

        ## Calculate the coordinates of the 8 corners
        raw_outer_1 = (self.radius_outer, self.eta_center-self.eta_width/2.0, self.phi_center-self.phi_width/2.0)
        raw_outer_2 = (self.radius_outer, self.eta_center+self.eta_width/2.0, self.phi_center-self.phi_width/2.0)
        raw_outer_3 = (self.radius_outer, self.eta_center+self.eta_width/2.0, self.phi_center+self.phi_width/2.0)
        raw_outer_4 = (self.radius_outer, self.eta_center-self.eta_width/2.0, self.phi_center+self.phi_width/2.0)

        raw_inner_1 = (self.radius_inner, self.eta_center-self.eta_width/2.0, self.phi_center-self.phi_width/2.0)
        raw_inner_2 = (self.radius_inner, self.eta_center+self.eta_width/2.0, self.phi_center-self.phi_width/2.0)
        raw_inner_3 = (self.radius_inner, self.eta_center+self.eta_width/2.0, self.phi_center+self.phi_width/2.0)
        raw_inner_4 = (self.radius_inner, self.eta_center-self.eta_width/2.0, self.phi_center+self.phi_width/2.0)

        self.outer_1 = rap_to_cart(raw_outer_1)
        self.outer_2 = rap_to_cart(raw_outer_2)
        self.outer_3 = rap_to_cart(raw_outer_3)
        self.outer_4 = rap_to_cart(raw_outer_4)

        self.inner_1 = rap_to_cart(raw_inner_1)
        self.inner_2 = rap_to_cart(raw_inner_2)
        self.inner_3 = rap_to_cart(raw_inner_3)
        self.inner_4 = rap_to_cart(raw_inner_4)


    def calculate_coordinates_cylindrical(self):

        ## Calculate the coordinates of the 8 corners
        raw_outer_1 = (self.radius_outer, self.z_center-self.z_width/2.0, self.phi_center-self.phi_width/2.0)
        raw_outer_2 = (self.radius_outer, self.z_center+self.z_width/2.0, self.phi_center-self.phi_width/2.0)
        raw_outer_3 = (self.radius_outer, self.z_center+self.z_width/2.0, self.phi_center+self.phi_width/2.0)
        raw_outer_4 = (self.radius_outer, self.z_center-self.z_width/2.0, self.phi_center+self.phi_width/2.0)

        raw_inner_1 = (self.radius_inner, self.z_center-self.z_width/2.0, self.phi_center-self.phi_width/2.0)
        raw_inner_2 = (self.radius_inner, self.z_center+self.z_width/2.0, self.phi_center-self.phi_width/2.0)
        raw_inner_3 = (self.radius_inner, self.z_center+self.z_width/2.0, self.phi_center+self.phi_width/2.0)
        raw_inner_4 = (self.radius_inner, self.z_center-self.z_width/2.0, self.phi_center+self.phi_width/2.0)

        self.outer_1 = cyl_to_cart(raw_outer_1)
        self.outer_2 = cyl_to_cart(raw_outer_2)
        self.outer_3 = cyl_to_cart(raw_outer_3)
        self.outer_4 = cyl_to_cart(raw_outer_4)

        self.inner_1 = cyl_to_cart(raw_inner_1)
        self.inner_2 = cyl_to_cart(raw_inner_2)
        self.inner_3 = cyl_to_cart(raw_inner_3)
        self.inner_4 = cyl_to_cart(raw_inner_4)


    def build(self):

        self.display_list = glGenLists(1)
        glNewList(self.display_list,GL_COMPILE)
        glBegin(GL_QUADS)

        ## Top
        glColor4f( self.color_outer[0], self.color_outer[1], self.color_outer[2], self.transparency )
        glVertex3f( self.outer_1[0], self.outer_1[1], self.outer_1[2] )
        glVertex3f( self.outer_2[0], self.outer_2[1], self.outer_2[2] )
        glVertex3f( self.outer_3[0], self.outer_3[1], self.outer_3[2] )
        glVertex3f( self.outer_4[0], self.outer_4[1], self.outer_4[2] )

        ## Bottom
        glColor4f( self.color_inner[0], self.color_inner[1], self.color_inner[2], self.transparency )
        glVertex3f( self.inner_1[0], self.inner_1[1], self.inner_1[2] )
        glVertex3f( self.inner_2[0], self.inner_2[1], self.inner_2[2] )
        glVertex3f( self.inner_3[0], self.inner_3[1], self.inner_3[2] )
        glVertex3f( self.inner_4[0], self.inner_4[1], self.inner_4[2] )

        ## Front
        glColor4f( self.color_outer[0], self.color_outer[1], self.color_outer[2], self.transparency )
        glVertex3f( self.outer_1[0], self.outer_1[1], self.outer_1[2] )
        glVertex3f( self.outer_2[0], self.outer_2[1], self.outer_2[2] )
        glColor4f( self.color_inner[0], self.color_inner[1], self.color_inner[2], self.transparency )
        glVertex3f( self.inner_2[0], self.inner_2[1], self.inner_2[2] )
        glVertex3f( self.inner_1[0], self.inner_1[1], self.inner_1[2] )

        ## Back
        glColor4f( self.color_outer[0], self.color_outer[1], self.color_outer[2], self.transparency )
        glVertex3f( self.outer_4[0], self.outer_4[1], self.outer_4[2] )
        glVertex3f( self.outer_3[0], self.outer_3[1], self.outer_3[2] )
        glColor4f( self.color_inner[0], self.color_inner[1], self.color_inner[2], self.transparency )
        glVertex3f( self.inner_3[0], self.inner_3[1], self.inner_3[2] )
        glVertex3f( self.inner_4[0], self.inner_4[1], self.inner_4[2] )

        ## Left
        glColor4f( self.color_outer[0], self.color_outer[1], self.color_outer[2], self.transparency )
        glVertex3f( self.outer_1[0], self.outer_1[1], self.outer_1[2] )
        glVertex3f( self.outer_4[0], self.outer_4[1], self.outer_4[2] )
        glColor4f( self.color_inner[0], self.color_inner[1], self.color_inner[2], self.transparency )
        glVertex3f( self.inner_4[0], self.inner_4[1], self.inner_4[2] )
        glVertex3f( self.inner_1[0], self.inner_1[1], self.inner_1[2] )

        ## Right
        glColor4f( self.color_outer[0], self.color_outer[1], self.color_outer[2], self.transparency )
        glVertex3f( self.outer_3[0], self.outer_3[1], self.outer_3[2] )
        glVertex3f( self.outer_2[0], self.outer_2[1], self.outer_2[2] )
        glColor4f( self.color_inner[0], self.color_inner[1], self.color_inner[2], self.transparency )
        glVertex3f( self.inner_2[0], self.inner_2[1], self.inner_2[2] )
        glVertex3f( self.inner_3[0], self.inner_3[1], self.inner_3[2] )

        glEnd()
        glEndList()

        


    def draw(self):

        ## Add distance from the z-axis
        move_x = self.distance*math.cos(self.phi_center)
        move_y = self.distance*math.sin(self.phi_center)
        
        glTranslatef(move_x, move_y, 0.0)
        glCallList(self.display_list)
        glTranslatef(-move_x, -move_y, 0.0)



        
