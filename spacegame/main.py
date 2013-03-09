#
#
#


import kivy
kivy.require('1.1.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.image import Image as ImageForTest
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.core.window import Window


from kivy.lang import Builder
from kivy.graphics import Color
import math

m = ImageForTest.load('maze_2.png',keep_data=True)

Builder.load_string("""
<PongBall>:
    size: 50, 50 
""")

class Mazy(Image):    
    def on_touch_down(self,touch):
        print "Testing...",touch.x,touch.y
        tx = touch.x
        ty = 600-touch.y 
        print m.read_pixel(tx,ty)

class PongBall(Image):
    r = NumericProperty(.5)
    g = NumericProperty(.5)
    b = NumericProperty(.5)
    color_speed = NumericProperty(0)
    
    def on_touch_down(self,touch):
        print "Touched!",touch.x,touch.y
        self.color_speed += .03


Builder.load_string("""
<Ship>:
    size: 50, 50 
""")

class ShipPlayer(Scatter):
    max_speed = NumericProperty(5)
    turn_speed = NumericProperty(2)

class SpaceGame(Widget):
    
    def key_value(self,key):
        #print self.key_dict
        if key in self.key_dict:
            if self.key_dict[key] == False:
                return 0
            else:
                return 1
        return 0
    
    def _key_down(self,keyboard, keycode, text, modifiers):
        self.key_dict[keycode[1]] = True
        #print "down",keycode
        
    def _key_up(self,keyboard, keycode):
        self.key_dict[keycode[1]] = False
        #print "up",keycode
        
    def _keyboard_closed(self):
        #print 'My keyboard have been closed!'
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None
    
    def __init__(self):
        self.key_dict = {}
        super(SpaceGame, self).__init__()
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._key_down)
        self._keyboard.bind(on_key_up=self._key_up)
        
        self.mazy = Mazy(source='maze_2.png',keep_data=True)
        self.add_widget(self.mazy)
        self.mazy.width = 800
        self.mazy.height = 600
        self.frames = 0 
        
        image = Image(source='img1.png')
        image.x += 0
        image.y += 0
        self.ship = ShipPlayer()
        self.ship.add_widget(image)
        self.add_widget(self.ship)
        
    
       
    def can_move_here(self,x,y):
        print "Testing...",x,y
        tx = x
        ty = 600 - y 
        c=m.read_pixel(tx,ty)
        if c[0] > .99:
            return True
        return False
    
    
    def update(self, *args): 
        #keep track of fames
        self.frames += 1
        self.ship.rotation += self.ship.turn_speed*self.key_value("left")
        self.ship.rotation -= self.ship.turn_speed*self.key_value("right")

        tx=self.ship.center_x + self.ship.max_speed*math.cos(self.ship.rotation*.0174532925)*self.key_value("up")
        ty=self.ship.center_y + self.ship.max_speed*math.sin(self.ship.rotation*.0174532925)*self.key_value("up")
        if self.can_move_here(tx,ty):
            self.ship.center_x = tx
            self.ship.center_y = ty

class SpaceApp(App):
    def build(self):
        game = SpaceGame()
        Clock.schedule_interval(game.update, 1.0/60.0)#called 1 in 60
        return game


if __name__ in ('__android__', '__main__'):
    SpaceApp().run()
