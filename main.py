#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from functools import partial
import os
import random

import kivy
kivy.require('1.8.0')

from kivy.config import Config
Config.set('graphics', 'width', '1400')
Config.set('graphics', 'height', '400')

from kivy.app import App
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.metrics import sp
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.accordion import AccordionItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.codeinput import CodeInput
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.scatter import Scatter
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import SlideTransition
from kivy.properties import StringProperty
from kivy.base import EventLoop
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.graphics import Color, Rectangle, Line
from kivy.atlas import Atlas
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from functools import partial

import os
EventLoop.ensure_window()
__version__ = '0.2.4'

# Constant declaration
CHAR_WIDTH = 32
CHAR_HEIGHT = CHAR_WIDTH

screens = ["Title", "CreateScreen", "ViewScreen"]
for screen in screens:
    kv_file = "{}.kv".format(screen.lower())
    Builder.load_file(os.path.join("screens", kv_file))

class LoadDialog(FloatLayout):
    curdir = os.path.dirname(os.path.realpath(__file__))
    # Need to use curdir to open THIS folder location
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    #text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class TitleScreen(Screen):
    pass

class CreateScreen(Screen):
    def on_enter(self):
        print('Enter create screen')

class ViewScreen(Screen):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    tabarea = ObjectProperty(None)
    curDirectory = os.path.dirname(os.path.realpath(__file__))

    def on_enter(self):
        # starts the file manager when this screen is entered
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.4, 0.8))
        self._popup.open()

    def dismiss_popup(self):
        self._popup.dismiss()
        self.manager.current = 'Title'

    def load(self, path, filename):
        #loads the file
        tab = open(os.path.join(path, filename[0]))
        self._popup.dismiss()

        # Draws tab in the ViewScreen's tabArea
        self.tabarea.drawtab(tab)

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        print(self.save)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()


class TabArea(BoxLayout):
    tabCanvas = ObjectProperty(None)
    slide = ObjectProperty(None)

    def drawtab(self, tab):
        # Required tab pre-processing:
        # 1. Between brackets (|) enforce a bar width (set number of characters)

        wid = self.tabCanvas

        lineheight = 32
        startheight = 6 * lineheight

        # Get path to current file to find atlas file
        curdir = os.path.dirname(os.path.realpath(__file__))
        #test print
        print(curdir + r"/Assets/main.atlas")
        atlas = Atlas(curdir + r"/Assets/main.atlas")

        i = 0
        for line in tab:
            # Parse by character, translating input to graphical output
            with wid.canvas:
                for j in range(len(line)):
                    print(j)
                    thischar = line[j]
                    #print(thischar)
                    if thischar == '\n' or thischar == ':':
                        pass
                    elif j == 0:
                        # T bar
                        Rectangle(source='atlas://Assets/main/tbar',
                                  pos=(0, startheight-(i*lineheight)),
                                  size=(32, 32))
                    elif thischar == "|" and j > 0:
                        # Plus bar
                        #print("Making vertical line")
                        Rectangle(source='atlas://Assets/main/plusbar',
                                  pos=(j*CHAR_WIDTH, startheight-(i*lineheight)),
                                  size=(32, 32))
                    elif thischar == "-":
                        # Horizontal line
                        #print("Making horizontal line")
                        Rectangle(source='atlas://Assets/main/bar',
                                  pos=(j*CHAR_WIDTH, startheight-(i*lineheight)),
                                  size=(32, 32))
                    # Look for digits
                    else:
                        found = False
                        thisdigit = -1

                        # See if this character is in range (0-9)
                        for num in range(10):
                            if str(num) == thischar and not found:
                                found = True
                                thisdigit = num
                        # Get next and last character for 2-digit notes
                        lastchar = ''
                        nextchar = ''
                        if found:
                            if j-1 >= 0:
                                lastchar = line[j-1]
                            if j+1 < len(line):
                                nextchar = line[j+1]

                        if found and lastchar != '1' and lastchar != '2':
                            # Could be a double digit note
                            if thischar == '1' or thischar =='2':
                                nextfound = False
                                nextchar = line[j+1]
                                for num in range(10):
                                    if str(num) == nextchar and not nextfound:
                                        nextfound = True
                                        combo = thischar + nextchar
                                        print("Making " + combo)
                                        Rectangle(source=('atlas://Assets/main/norm' + combo),
                                                  pos=(j*CHAR_WIDTH, startheight-(i*lineheight)),
                                                  size=(32, 32))

                                # Wasn't double digit, draw it alone
                                if not nextfound:
                                    #print("Making " + thischar)
                                    Rectangle(source=('atlas://Assets/main/norm' + thischar),
                                              pos=(j*CHAR_WIDTH, startheight-(i*lineheight)),
                                              size=(32, 32))

                            # It's just a lonely single digit, draw it
                            else:
                                #print("Making " + thischar)
                                Rectangle(source=('atlas://Assets/main/norm' + thischar),
                                          pos=(j*CHAR_WIDTH, startheight-(i*lineheight)),
                                          size=(32, 32))
                        else:
                            print("Unknown symbol or second digit")
                            Rectangle(source='atlas://Assets/main/bar',
                                      pos=(j*CHAR_WIDTH, startheight-(i*lineheight)),
                                      size=(32, 32))

            # Increment counter
            i += 1

    def scroll_change(self, scrl, instance, value):
        scrl.scroll_x = value

    def slider_change(self, slide, instance, value):
        if value >= 0:
            slide.value = value

#main widget of the app
class TabMachine(BoxLayout):
    def __init__(self, **kwargs):
        super(TabMachine, self).__init__(**kwargs)
        self.orientation = 'vertical'
        # Adds the screen manager to the main app
        self.root = ScreenManager()
        # Displays in the order of adds
        # Add the nav bar to the top
        self.root.add_widget(TitleScreen(name='Title'))
        self.root.add_widget(CreateScreen(name='CreateScreen'))
        self.root.add_widget(ViewScreen(name='ViewScreen'))

        self.slide_menu = NavMenu(root=self)
        self.add_widget(self.slide_menu)
        # Add the screen to the middle.
        #self.add_widget(self.content)
        self.add_widget(self.root)

    def set_current_screen(self, jump_to):
        self.root.current = jump_to

Builder.load_file("navmenu.kv")
class NavMenu(BoxLayout):
    slide_spinner = ObjectProperty(None)

    def __init__(self, root, **kwargs):
        super(NavMenu, self).__init__(**kwargs)
        self.root = root
        #self.slide_spinner.values = screens

    #def go_slide(self, spinner):
    #    if spinner.text in screens:
    #        self.root.set_current_slide(spinner.text)

    def go_create(self):
        self.root.set_current_screen('CreateScreen')

    def go_view(self):
        self.root.set_current_screen('ViewScreen')

class TabMachineApp(App):
    font_size_regular = sp(25)

    curDirectory = os.path.dirname(os.path.realpath(__file__))
    def build(self):
        return TabMachine()

if __name__ == '__main__':
    TabMachineApp().run()
