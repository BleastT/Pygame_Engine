from enum import Flag
from tkinter import font
from turtle import color
import pygame
import sys
import math

## BASIC FUNCTIONS

def check_key_pressed(key):
    keys = pygame.key.get_pressed()
    if keys[key]:
        return True
    else:
        return False

def encrypt_decrypt(text_to_encrypt, mode=0):
    # 0 is encrypt
    # 1 is decrypt
    return_text = []

    code = {
        'a': '1' ,
        'b': '6' ,
        'c': '"' ,
        'd': '/' ,
        'e': 'z' ,
        'f': ']' ,
        'g': '$' ,
        'h': '*' ,
        'i': ')' ,
        'j': '^' ,
        'k': '@' ,
        'l': '!' ,
        'm': '.' ,
        'n': '>' ,
        'o': '<' ,
        'p': '`' ,
        'q': '~' ,
        'r': ';' ,
        's': ':' ,
        't': '-' ,
        'u': '_' ,
        'v': '+' ,
        'w': '=' ,
        'x': '|' ,
        'y': '[' ,
        'z': '\\' ,
        '1' : 'Q' ,
        '2' : 'W' ,
        '3' : 'D' ,
        '4' : 'T' ,
        '5' : 'P' ,
        '6' : 'O' ,
        '7' : 'E' ,
        '8' : 'K' ,
        '9' : 'A' ,
        '0' : 'L' ,
        '?' : 'H' ,
        '!' : 'V' ,
        '.' : 'Z' ,
        ' ' : 'S' ,
        '\n': 'G' ,
        ',': 'X' ,
        ':': '?' ,
        '\'': 'N' ,
        '"': 'D' ,
        '_': 'U' ,
        '-': 'M' ,
        '[': 'I',
        ']': 'C',
        '{': '&',
        '}': '#',
        '/': '}',
        '\\': '{'
    }
     


    for text in text_to_encrypt:
        text_ = ''
        if mode == 0:
            for char in text.lower():
                text_ += code[char]
        else:
            for char in text:
                text_ += list(code.keys())[list(code.values()).index(char)]
        return_text.append(text_)

    # print(return_text)
    return return_text




class APPLICATION():
    
    pygame.init()

    def __init__(self, screenRes, displayRes,max_fps = 60, show_fps=False, cam_Smooth=True, edit_mode=False, editor_width=500) -> None:
             ##WINDOW PARAMETERS AND VARIABLES
        self.screenRes = screenRes
        self.displayRes = displayRes
        self.max_fps = max_fps
        self.show_fps = show_fps
        self.screenX, self.screenY = self.screenRes
        if edit_mode == True:
            self.screen = pygame.display.set_mode((self.screenX + editor_width, self.screenY))
        else:
            self.screen = pygame.display.set_mode(self.screenRes)
        self.display = pygame.Surface(self.displayRes)
            ##GAMEPLAY VARIABLES
        self.objects =  {}
        self.uiTexts = {}
        self.running = True
        self.clock = pygame.time.Clock()
        self.deltatime = 0
            ##CAMERA VARIABLES
        self.camerax = 0
        self.cameray = 0
        self.camDelayX = 1.7
        self.camDelayY = 1
        self.cameraxSpeed = 1
        self.cameraySpeed = 1
        self.camBeforeEditMode = (0,0)
        self.objToFollow = ''
        self.smooth = cam_Smooth

          ##Editor mode
        self.Editor = EDITOR(self)
        self.is_editorMode = edit_mode
        self.left_clicking = False
        self.right_clicking = False
        if self.is_editorMode == True:
            self.play = False
        else:
            self.play = True



        if self.show_fps == True:
            self.createUIElement(UITEXT(name='FPS'))
        print('[CHECK] WINDOW initialized')

    def get(self, name):
        return self.objects[name]

    def Poll_Events(self):
        self.left_clicking = False
        self.right_clicking = False
        ##Handle window events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            if self.is_editorMode == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F10:
                        if self.play == True:
                            self.play = False
                            self.camBeforeEditMode = (self.camerax, self.cameray)
                        else:
                            self.play = True
                            self.camerax, self.cameray = self.camBeforeEditMode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                   self.left_clicking = True
                elif event.button == 3:
                    self.right_clicking = True


    def update(self):
        self.display.fill((45, 175, 245))
        self.screen.fill((0,0,0))
        self.CameraMove()
        for object in self.objects:
            curr_object = self.objects[object]
            if curr_object.type != 'static' and self.play == True:
                curr_object.update(self.deltatime) # update the object
                curr_object.collider(self.objects)
            self.renderObject(curr_object)


        if self.show_fps == True and self.play == True:
            self.uiTexts['FPS'].updateText(f'FPS: {math.floor(self.clock.get_fps())}') # display fps to the screen

        if self.is_editorMode == True:
            self.Editor.update(self)


        surf = pygame.transform.scale(self.display, self.screenRes)
        self.screen.blit(surf, (0,0))

        ###ADD UI ELEMENTS
        for ui in self.uiTexts:
            currUI = self.uiTexts[ui]
            self.screen.blit(currUI.text, currUI.position())

        self.clock.tick() #update the fps
        self.deltatime = self.clock.get_time() / 1000 # calculate the deltatime
        pygame.display.update() # show the screen to the player
        

    def createObject(self, object):
        if object.name == '':
            object.name = 'object_' + str(len(self.objects))
        self.objects[object.name] = object # add new object to the list

        print(f"[CHECK] {object.name.upper()} initialized")

    def createUIElement(self, ui):
        if ui.name == '':
            ui.name = 'uiElement_' + str(len(self.objects))
        self.uiTexts[ui.name] = ui

        print(f"[CHECK] {ui.name.upper()} initialized")

    def activateCameraFollow(self,name):
        self.objToFollow = name # set the cmerafollow

    def deactivateCameraFollow(self):
        self.objToFollow = ''

    def CameraMove(self):
        if self.play == False:
            if check_key_pressed(pygame.K_a):
                self.camerax += -self.cameraxSpeed 
            elif check_key_pressed(pygame.K_d):
               self.camerax += self.cameraxSpeed 

            if check_key_pressed(pygame.K_w):
                self.cameray += -self.cameraySpeed
            elif check_key_pressed(pygame.K_s):
                self.cameray += self.cameraySpeed
        else:
            if self.objToFollow != '':
                object = self.objects[self.objToFollow]
                width, height = self.displayRes
                if self.smooth == True:
                    self.camerax += (object.rect.x - (self.camerax + (width / 2)) + object.width / 2) * self.camDelayX * self.deltatime
                    self.cameray += (object.rect.y - (self.cameray + (height / 2)) + object.height / 2) * self.camDelayY * self.deltatime
                else:
                    self.camerax += (object.rect.x - (self.camerax + (width / 2)) + object.width / 2)
                    self.cameray += (object.rect.y - (self.cameray + (height / 2)) + object.height / 2)


    def cam_position(self):
        return self.camerax, self.cameray


    def enableEditorMode(self):
        self.is_editorMode = True
    def disabelEditorMode(self):
        self.is_editorMode = False

    def is_object_inside_preview(self, object):
        x,y = self.displayRes
        if object.displayx + object.width > 0 and object.displayx < x \
            and object.displayy + object.height > 0 and object.displayy < y:
            return True
        else:
            return False

    def renderObject(self, object):
        object.displayx = object.rect.x - self.camerax
        object.displayy = object.rect.y - self.cameray

        if self.is_object_inside_preview(object) == True:
            self.display.blit(object.img, (object.displayx, object.displayy))




class OBJECT():
    def __init__(self, img_path, name,type, start_pos=(0,0), function='', animated=False, anim_path='') -> None:
        self.img = pygame.image.load(img_path)
        self.img_path = img_path
        self.name = name
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.rect = pygame.Rect(start_pos, (self.width, self.height))
        self.type = type
        self.function = function

        self.displayx = 0
        self.displayy = 0
        self.movement = [0,0]
        self.hitlist = []
        self.initialized_script = False
        if animated == True:
            self.animator = ANIMATOR()

  
    def move_by(self, x, y): # add a value to th existant position of the object
        self.rect.x += x
        self.rect.y += y

    def move_to (self, x , y): # set a new value to the position of the object
        self.rect.x = x
        self.rect.y = y

    def position(self): # return the position of the player
        return self.rect.x, self.rect.y


    def update(self, deltatime):
        if self.function != '':
            return self.function(self, deltatime)
        else:
           return 
    def collision_test(self, objects):
        hitlist = []
        for object in objects:
            curr_object = objects[object]
            if curr_object == self:
                pass
            else:
                if self.rect.colliderect(curr_object.rect):
                    hitlist.append(curr_object.rect)

        return hitlist

    def collider(self, others):
        self.collision_types = {'Top': False, 'Bottom':False, 'Left':False, 'Right':False}
        self.move_by(self.movement[0], 0)
        hitlist = self.collision_test(others)
        for other in hitlist:
            if self.movement[0] > 0:
                self.rect.right = other.left
                self.collision_types['Right'] = True
            elif self.movement[0] < 0:
                self.rect.left = other.right
                self.collision_types['Left'] = True
        self.move_by(0, self.movement[1])
        hitlist = self.collision_test(others)
        for other in hitlist:
            if self.movement[1] < 0:
                self.rect.top = other.bottom
                self.collision_types['Top'] = True
            elif self.movement[1] > 0:
                self.rect.bottom = other.top
                self.collision_types['Bottom'] = True

        self.movement = [0,0]




class EDITOR():

    def __init__(self,window) -> None:
        window.createUIElement(UITEXT(name='Titlefont', font_size=32, pos=(window.screenX, 0)))
        window.uiTexts['Titlefont'].updateText('Game Informations')
        window.createUIElement(UITEXT(name='SelectedObjectPos', font_size=24, pos=(window.screenX + 20, 60)))
        window.createUIElement(UITEXT(name='CameraPos', font_size=24, pos=(window.screenX + 20, 100)))
        window.createUIElement(UITEXT(name='GameMode', font_size=50, pos=(window.screenX / 2 - 50, 10), color=(255,0,0)))
        self.selectedObject = ''
    def update(self, window):
        if self.selectedObject != '':
            window.uiTexts['SelectedObjectPos'].updateText(f"Selected Object Position: {window.objects[self.selectedObject].position()}")
        else:
            window.uiTexts['SelectedObjectPos'].updateText(f"Selected Object Position: N/A")

        window.uiTexts['CameraPos'].updateText(f"Camera Position: ({window.camerax},{window.cameray})")
        if window.play == False:
            window.uiTexts['GameMode'].updateText(f"PAUSE")
        else:
            window.uiTexts['CameraPos'].updateText(f"")

        screenResX, screenResY = window.screenRes
        displayResX, displayResY = window.displayRes
        screenFactorX = displayResX / screenResX 
        screenFactorY = displayResY / screenResY 


        mouseX = pygame.mouse.get_pos()[0] * screenFactorX
        mouseY = pygame.mouse.get_pos()[1] * screenFactorY
        clippedX = round(mouseX/8, 1) * 8
        clippedY = round(mouseY/8,1) * 8
        camX, camY = window.cam_position()
        if window.play == False and check_key_pressed(pygame.K_LSHIFT):
            pygame.draw.rect(window.display, (0,0,0), pygame.Rect((clippedX, clippedY), (8,8)), width=1)     
            if window.left_clicking == True:
                window.createObject(OBJECT('Bin/assets/images/ground.png', '','static', start_pos=(clippedX + camX, clippedY + camY)))
            if window.right_clicking == True:     
                for object in window.objects:
                    curr_object = window.objects[object]
                    if mouseX > curr_object.displayx and mouseX < curr_object.displayx + curr_object.width \
                        and mouseY > curr_object.displayy and mouseY < curr_object.displayy + curr_object.height:
                        window.objects.pop(object, None)
                        break      
        else:
            if window.left_clicking == True:
                for object in window.objects:
                    curr_object = window.objects[object]
                    if mouseX > curr_object.displayx and mouseX < curr_object.displayx + curr_object.width \
                        and mouseY > curr_object.displayy and mouseY < curr_object.displayy + curr_object.height:
                        self.selectedObject = object
                        break




class ANIMATOR():
    pass


class UITEXT():
    def __init__(self, name='', color=(255,255,255), font_path="Bin/assets/fonts/Roboto_Regular.ttf", pos=(0,0), font_size=20) -> None:
        self.xpos, self.ypos = pos
        self.name = name
        self.color = color
        self.font = pygame.font.Font(font_path, font_size)
        self.text = self.font.render(f'', True, self.color) 


    def updateText(self, new_text):
        self.text = self.font.render(new_text, True,self.color)

    def position(self):
        return self.xpos, self.ypos