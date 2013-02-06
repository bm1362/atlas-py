import math
from entity.entity import entity


"""
This works but isn't ideal- we should make the character a rigid body object and add forces to him appropriately for movement( like a spaceship etc )


"""
class character(entity):
    def __init__(self, **kwargs):
        super(character, self).__init__(**kwargs)
        self.forces = []
        self.acceleration = []
        self.momentum = 0
        self.velocity = 0
        self.governing_body = None
        self.theta = 90

    def update(self, radius, offset_x, offset_y):
        # add constant gravitational force
        gravForce = 100
        distFromPlanet = radius + 5
        self.position['x'] = distFromPlanet*(math.cos(self.theta)) + offset_x
        self.position['y'] = distFromPlanet*(math.sin(self.theta)) + offset_y

    def impulse(v):
        pass

    def move_left(self, dx):
        self.theta += dx

    def move_right(self, dx):
        self.theta -= dx