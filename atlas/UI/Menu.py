'''
This is Menu.py. It holds the definition and implememtation of the Menu class
'''
import pyglet
from pyglet.window import key


from Entity.Square import Square
from Entity.Circle import Circle
from Util.Vector2 import Vector2
from Util.Geometry import is_in_polygon


class Menu(pyglet.window.Window):
    '''
    This is the Menu class. It is used for selecting the size, shape, and mass 
    of the next object created by mouse click in the simulation.

    It is derived from pyglet.window.Window for the event handling
    '''
    def __init__(self, parent, **kwargs):
        self.parent = parent
        super(Menu, self).__init__(**kwargs)

        self.entities = [Square(size=50, 
            position=Vector2(x=self.parent.gen_size, y=100)), 
            Square(size=50, 
                position=Vector2(x=self.parent.gen_mass / 10, y=200)), 
            Square(size=50, position=Vector2(x=200, y=300)), 
            Circle(radius=25, position=Vector2(x=300, y=300))]

        self.labels = [pyglet.text.Label('Choose your size:', x=175, y=450, 
            color=(255, 255, 255, 255)), 
            pyglet.text.Label('50:', x=50, y=433, color=(255, 255, 255, 255)),
            pyglet.text.Label('450:', x=433, y=433, color=(255, 255, 255, 255)),
            pyglet.text.Label('Choose your mass:', x=175, y=350, 
                color=(255, 255, 255, 255)), 
            pyglet.text.Label('500:', x=50, y=333, color=(255, 255, 255, 255)),
            pyglet.text.Label('4500:', x=433, y=333, 
                color=(255, 255, 255, 255)),
            pyglet.text.Label('Choose your shape:', x=175, y=250, 
                color=(255, 255, 255, 255)), 
            pyglet.text.Label('Current selection: shape: ' + 
                self.parent.gen_entity + ' size: ' 
                + str(int(self.parent.gen_size)) + ' mass: ' + 
                str(int(self.parent.gen_mass)), x=100, y=150, 
                color=(255, 255, 255, 255))
            ]

        self.clicked_object = None
        self.min_x = 50
        self.max_x = 450


    def on_draw(self):
        '''
        This method overwrites the same method in the superclass.

        It clears the screen and then draws all of the items in the entities 
        and labels lists
        '''
        self.clear()

        for label in self.labels:
            label.draw()

        for entity in self.entities:
            entity.draw(0, 0, 500)
        
    def on_mouse_press(self, x, y, button, modifiers):
        '''
        This method overwrites the same method in the superclass.

        It adds in the checking for a click on the shape or on the size/mass 
        sliders
        '''

        for entity in self.entities:
            if is_in_polygon(entity.get_screen_relative_vertices_vectors(
                0, 0, 500), Vector2(x=x, y=y)):
                self.clicked_object = entity

        if self.clicked_object is self.entities[2]:
            self.parent.gen_entity = 'SQUARE'
            self.clicked_object = None
        elif self.clicked_object is self.entities[3]:
            self.parent.gen_entity = 'CIRCLE'
            self.clicked_object = None


    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        '''
        This method overwrites the same method in the superclass.

        It updates position of the entities on the sliders. The movement is 
        restricted to the x direction as well as within the preset min and max
        '''
        if self.clicked_object is not None:
            if x < self.min_x:
                self.clicked_object.set_position(Vector2(x=self.min_x, 
                    y=self.clicked_object.position.y))
            elif x > self.max_x:
                self.clicked_object.set_position(Vector2(x=self.max_x, 
                    y=self.clicked_object.position.y))
            else:
                self.clicked_object.translate_vector(Vector2(x=dx, y=0))


    def on_mouse_release(self, x, y, button, modifiers):
        '''
        This method overwrites the same method in the superclass.

        It updates the current status slider and finalizes the information 
        for the future objects to be created in the simulation.
        '''
        self.clicked_object = None
        self.parent.gen_size = self.entities[0].position.x
        self.parent.gen_mass = self.entities[1].position.x * 10

        self.labels[-1] = pyglet.text.Label('Current selection: shape: ' + 
            self.parent.gen_entity + ' size: ' + 
            str(int(self.parent.gen_size)) + ' mass: ' + 
            str(int(self.parent.gen_mass)), 
            x=100, y=150, color=(255, 255, 255, 255))

    def on_key_press(self, symbol, modifiers):
        '''
        This method overwrites the same method in the superclass.

        It is part of a guard against opening multiple menu windows at once.
        '''
        if symbol == key.ESCAPE:
            self.parent.menu_window = False
            pyglet.clock.schedule_interval(self.parent.tick, 1.0/60.0) 
            self.close()