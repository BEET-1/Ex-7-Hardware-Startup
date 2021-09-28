import os

#os.environ['DISPLAY'] = ":0.0"
#os.environ['KIVY_WINDOW'] = 'egl_rpi'
import spidev
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.animation import AnimationTransition
from threading import Thread
from time import sleep
from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from pidev.Joystick import Joystick
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers
spi = spidev.SpiDev()


from datetime import datetime

time = datetime

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'

s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
                 steps_per_unit=200, speed=8)

class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White


class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """

    count = 0
    OnOff = True
    OnOff2 = True
    joy_x_val = 0.0
    joy_y_val = 0.0
    motor = ""
    motor2 = ""
    change = ObjectProperty(None)
    LeftRight = 0

    def motorToggle(self):
        if self.OnOff == True:
            self.motor = "off"
            s0.go_until_press(0, 6400)
            self.change.text = self.motor
            self.OnOff = False
            return
        else:
            self.motor = "on"
            self.change.text = self.motor
            s0.softStop()
            self.OnOff = True
            return

    def motorToggle2(self):
        if self.OnOff2 == True:
            self.motor2 = "Right"
            s0.go_until_press(1, 6400)
            self.direction.text = self.motor2
            self.OnOff2 = False
            return
        else:
            self.motor2 = "Left"
            self.direction.text = self.motor2
            s0.softStop()
            s0.go_until_press(0, 6400)
            self.OnOff2 = True
            return


    def Accell(self):

        if self.OnOff2 == True:
            s0.softStop()
            s0.go_until_press(0, self.motorSlider.value * 1000)


        else:
            s0.softStop()
            s0.go_until_press(1, self.motorSlider.value * 1000)




    def animationGo(self):
        anim = Animation(x=400, y=400) + Animation(size=(400,400), duration = 1.) + Animation(x=20, y=50)
        anim.start(self.move)

    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        print("Callback from MainScreen.pressed()")







"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))


"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()