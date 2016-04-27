from datetime import datetime
import pygame
from pygame.rect import Rect
from pygame.locals import *

from modules.focus import ProcessFocus
from modules.stacking import ProcessStacking
from ui import colours
from ui.widgets.background import LcarsBackgroundImage
from ui.widgets.gifimage import LcarsGifImage
from ui.widgets.lcars_widgets import LcarsText
from ui.widgets.screen import LcarsScreen
from ui.widgets.sprite import LcarsMoveToMouse


class MainScreen(LcarsScreen):
    def __init__(self, config, camera):
        self.config = config
        self.cam = camera
	LcarsScreen.__init__(self)

    def setup(self, all_sprites):
        self.image = None
        self.zoomPoint = None
        self.preview = False
        self.timer = 0

        # detect focus
        self.focus = ProcessFocus()
        self.focus.start()
        
        # stack images
        self.stack = ProcessStacking()
        self.stack.start()
        self.showStack = False

        # tracking images
        self.tracker = ProcessTracking()
        self.tracker.start()
        self.tracking = False

        
        self.focusText = LcarsText((255,0,0), (17,303), "Focus: ")
        self.trackingText = LcarsText((255,0,0), (40,303), "Track: ")

        
        all_sprites.add(LcarsBackgroundImage("assets/jarvis.png"))
        all_sprites.add(self.focusText)
        #all_sprites.add(LcarsGifImage("assets/jarvis_gadgets.gif", (83, 258)))
        # all_sprites.add(LcarsMoveToMouse(colours.BEIGE))
        
    def setImage(self, image):
        # do background processing
        self.focus.addFrame(image)
        if self.tracking:
            self.tracker.addFrame(image)
        if self.showStack: self.stack.addFrame(image)
        if self.showStack and self.stack.outputFrame is not None:
            image = self.stack.getFrame()

        if (image == None): return
        self.image = pygame.image.frombuffer(image, (len(image[0]), len(image)), 'RGB').convert()
        
    def update(self, screenSurface, fpsClock):
        if pygame.time.get_ticks() - self.timer > 100:
            self.focusText.setText("Focus: %d" % self.focus.focus)
            self.timer = pygame.time.get_ticks()
            self.trackingText.setText("Track: %s" % self.tracker.status)

            
        if (self.image != None):
            screenSurface.blit(self.image,
                # placement of preview window
                (100, 100),  
                # area of image to display
                Rect(100, 100, self.image.get_width(), self.image.get_height())) 

    def handleEvents(self, event, fpsClock):
        if (event.type == KEYUP and event.key == K_p):
           if (self.preview): 
	      self.cam.stopPreview()
              self.preview = False
           else:
	      self.cam.startPreview()
              self.preview = True

        if (event.type == KEYUP and event.key == K_s):
	   self.showStack = not self.showStack

        if (event.type == KEYUP and event.key == K_t):
	   self.tracking = not self.tracking

           
        return LcarsScreen.handleEvents(self, event, fpsClock)
    
    def timeStamped(self, fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
        return datetime.now().strftime(fmt).format(fname=fname)

    
