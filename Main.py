import os

#os.environ['DISPLAY'] = ":0.0"
#os.environ['KIVY_WINDOW'] = 'egl_rpi'
import spidev
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus
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
cyprus.initialize()
cyprus.setup_servo(1)
cyprus.set_servo_position(1, 0)
s0 = stepper(port=3, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
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
            cyprus.set_pwm_values(2, period_value=100000, compare_value=10000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
            self.change.text = self.motor
            self.OnOff = False
            return
        else:
            self.motor = "on"
            self.change.text = self.motor
            cyprus.set_pwm_values(2, period_value=100000, compare_value=0, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
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
            s0.go_until_press(0, int(self.motorSlider.value * 500))


        else:
            s0.softStop()
            s0.go_until_press(1, int(self.motorSlider.value * 500))

    def start_showtime_thread(self):
        Thread(target=self.showtime).start()

    def showtime(self):
        print(str(s0.get_position_in_units()))
        s0.set_speed(1.0)
        s0.relative_move(15.0)
        self.pos1.text = str(s0.get_position_in_units())
        sleep(10.0)
        s0.set_speed(5.0)
        s0.relative_move(10.0)
        self.pos1.text = str(s0.get_position_in_units())
        sleep(8.0)
        s0.relative_move(-25.0)
        sleep(30.0)
        s0.set_speed(8.0)
        s0.relative_move(-100.0)
        while s0.isBusy() == True:
            sleep(0.01)
        self.pos1.text = str(s0.get_position_in_units())
        s0.relative_move(100.0)

    stateCheck = True
    def switchStates(self):
        cyprus.set_pwm_values(2, period_value=100000, compare_value=1000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
        sleep(2.0)
        cyprus.set_pwm_values(2, period_value=100000, compare_value=2000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
        sleep(2.0)
        cyprus.set_pwm_values(2, period_value=100000, compare_value=3000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
        sleep(2.0)
        cyprus.set_pwm_values(2, period_value=100000, compare_value=4000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
        sleep(2.0)
        cyprus.set_pwm_values(2, period_value=100000, compare_value=5000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
        sleep(2.0)
        cyprus.set_pwm_values(2, period_value=100000, compare_value=6000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
        sleep(2.0)
        cyprus.set_pwm_values(2, period_value=100000, compare_value=7000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
        sleep(2.0)
        cyprus.set_pwm_values(2, period_value=100000, compare_value=8000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
        sleep(2.0)
        cyprus.set_pwm_values(2, period_value=100000, compare_value=9000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
        sleep(2.0)
        cyprus.set_pwm_values(2, period_value=100000, compare_value=10000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
        sleep(2.0)
        cyprus.set_pwm_values(2, period_value=100000, compare_value=0, compare_mode=cyprus.LESS_THAN_OR_EQUAL)






    pos3= 0
    def buttonSense(self):

        while True:
            if self.pos3 == 0:
                if cyprus.read_gpio() & 0b0001 == 0:
                    cyprus.set_pwm_values(2, period_value=100000, compare_value=10000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
                    self.pos3 = 1
            else:
                if cyprus.read_gpio() & 0b0001 == 0:
                    cyprus.set_pwm_values(2, period_value=100000, compare_value=0, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
                    self.pos3 = 0
            sleep(1.0)
    def start_button_thread(self):
        Thread(target=self.buttonSense).start()

    pos4 = 0
    def buttonSense2(self):

        while True:
            if self.pos4 == 0:
                if cyprus.read_gpio() & 0b0010 == 0:
                    cyprus.set_servo_position(2, 1)
                    self.pos4 = 1
            else:
                if cyprus.read_gpio() & 0b0010 == 0:
                        cyprus.set_servo_position(2, 0.5)
                        self.pos4 = 0
            sleep(1.0)

    def start_button_thread2(self):
        Thread(target=self.buttonSense2).start()





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