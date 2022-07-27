from enum import Flag
import pygame
import sys
import math





#### BASIC FUNCTIONS
def check_key_pressed(key):
    keys = pygame.key.get_pressed()
    if keys[key]:
        return True
    else:
        return False

def encrypt_decrypt(text_to_encrypt, mode=0):
    # 0 is encrypt
    # 1 is decrypt
    return_text = ''

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
        ']': 'C'
    }
     


    if mode == 0:
        for char in text_to_encrypt.lower():
            return_text += code[char]
    else:
        for char in text_to_encrypt:
            return_text += list(code.keys())[list(code.values()).index(char)]


    return return_text





class APPLICATION():
    
    pygame.init()

    def __init__(self, screenRes, displayRes,max_fps = 60, show_fps = False) -> None:
             ##WINDOW PARAMETERS AND VARIABLES
        self.screenRes = screenRes
        self.displayRes = displayRes
        self.max_fps = max_fps
        self.show_fps = show_fps
        self.screen = pygame.display.set_mode(self.screenRes)
        self.display = pygame.Surface(self.displayRes)
            ##GAMEPLAY VARIABLES
        self.objects =  {}
        self.running = True
        self.clock = pygame.time.Clock()
        self.deltatime = 0
            ##CAMERA VARIABLES
        self.camerax = 0
        self.cameray = 0
        self.camDelayX = 1.7
        self.camDelayY = 1
        self.cameraxSpeed = 500
        self.cameraySpeed = 500
        self.objToFollow = ''

          ##Editor mode
        self.Editor = EDITOR()
        self.is_editorMode = False
        self.left_clicking = False


        print('[CHECK] WINDOW initialized')

    def get(self, name):
        return self.objects[name]

    def Poll_Events(self):
        self.left_clicking = False
        ##Handle window events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F10:
                    if self.is_editorMode == True:
                        self.disabelEditorMode()
                    else:
                        self.enableEditorMode()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                   self.left_clicking = True


    def update(self):
        self.display.fill((45, 175, 245))
        camOffset = self.CameraMove()
        for object in self.objects:
            curr_object = self.objects[object]
            if curr_object.type != 'static' and self.is_editorMode == False:
                curr_object.update(self.deltatime) # update the object
            if self.is_inside_preview(curr_object) == True:
                curr_object.draw(self.display, camOffset) # draw objects


        if self.show_fps == True and self.is_editorMode == False:
            self.fps_counter(math.floor(self.clock.get_fps())) # display fps to the screen

        if self.is_editorMode == True:
            self.Editor.update(self)
        

    def flip(self): # display the frame to the screen
        surf = pygame.transform.scale(self.display, self.screenRes) # scale the display
        self.screen.blit(surf, (0,0)) 
        self.clock.tick(self.max_fps) #update the fps
        self.deltatime = self.clock.get_time() / 1000 # calculate the deltatime
        pygame.display.flip() # show the screen to the player

    def createObject(self, object):
        if object.name == '':
            object.name = 'object_' + str(len(self.objects))
        self.objects[object.name] = object # add new object to the list
        print(f"[CHECK] {object.name.upper()} initialized")

    def fps_counter(self, fps):
        if self.show_fps == True:
            font = pygame.font.Font("Bin/assets/fonts/Roboto_Regular.ttf", 32)
            text = font.render(f'fps: {fps} ', True,(255,255,255))
            self.display.blit(text, (0,0))   #diplay fps on demand

    def activateCameraFollow(self,name):
        self.objToFollow = name # set the cmerafollow

    def deactivateCameraFollow(self):
        self.objToFollow = ''

    def CameraMove(self):
        if self.is_editorMode == True:
            if check_key_pressed(pygame.K_a):
                self.camerax += -self.cameraxSpeed * self.deltatime
            elif check_key_pressed(pygame.K_d):
               self.camerax += self.cameraxSpeed * self.deltatime

            if check_key_pressed(pygame.K_w):
                self.cameray += -self.cameraySpeed * self.deltatime
            elif check_key_pressed(pygame.K_s):
                self.cameray += self.cameraySpeed * self.deltatime

            return self.camerax, self.cameray
        else:
            if self.objToFollow != '':
                object = self.objects[self.objToFollow]
                width, height = self.displayRes
                self.camerax += (object.rect.x - (self.camerax + (width / 2)) + object.width / 2) * self.camDelayX * self.deltatime
                self.cameray += (object.rect.y - (self.cameray + (height / 2)) + object.height / 2) * self.camDelayY * self.deltatime
                return self.camerax, self.cameray
            else:
                return 0,0

    def cam_position(self):
        return self.camerax, self.cameray


    def enableEditorMode(self):
        self.is_editorMode = True
    def disabelEditorMode(self):
        self.is_editorMode = False

    def is_inside_preview(self, object):
        x,y = self.displayRes
        if object.rect.x + object.width > 0 and object.rect.x < x \
            and object.rect.y + object.height > 0 and object.rect.y < y:
            return True
        else:
            return False


class OBJECT():
    def __init__(self, img_path, name,type, start_pos=(0,0), function='') -> None:
        self.img = pygame.image.load(img_path)
        self.name = name
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.rect = pygame.Rect(start_pos, (self.width, self.height))
        self.type = type
        self.function = function

        self.displayx = 0
        self.displayy = 0
    def draw(self,screen, camOffset):
        xCamOffset, yCamOffset = camOffset
        self.displayx = self.rect.x - xCamOffset 
        self.displayy = self.rect.y - yCamOffset 
        screen.blit(self.img, (self.displayx,self.displayy))

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
            self.function(self, deltatime)
        else:
           pass



class EDITOR():
    def __init__(self) -> None:
        pass
    def update(self, window):
        for object in window.objects:
            curr_object = window.objects[object]
            pygame.draw.rect(window.display, (124,252,0), pygame.Rect((curr_object.displayx,curr_object.displayy), (curr_object.width,curr_object.height)), width=2)

        displayResX, displayResY = window.displayRes
        self.editorWindow = pygame.Rect((0,0), (displayResX / 4, displayResY))

        screenResX, screenResY = window.screenRes

        screenFactorX = displayResX / screenResX 
        screenFactorY = displayResY / screenResY 


        mouseX = pygame.mouse.get_pos()[0] * screenFactorX
        mouseY = pygame.mouse.get_pos()[1] * screenFactorY
        camX, camY = window.cam_position()
        pygame.draw.rect(window.display, (0,0,0), pygame.Rect((mouseX, mouseY), (64,64)))

        
        if window.left_clicking == True:
            window.createObject(OBJECT('Bin/assets/images/player_prototype.png', '','static', start_pos=(mouseX + camX, mouseY + camY)))
        

        pygame.draw.rect(window.display, (0,0,0), self.editorWindow)



