import pygame
import sys
import math


#### BASIC FUNCTIONS
# def read_file(path):
#     file = open(path, 'r')
#     lines  = []
#     for line in file.readlines():
#         lines.append(line)
#     file.close()

#     return lines

# def write_file(path, text):
#     # print(text)
#     file = open(path, 'w')
#     final = []
#     for text_ in text:
#         text_ += '\n'
#         final.append(text_)
#     file.writelines(final)

#     file.close()

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

    def __init__(self, screenRes,max_fps = 60, show_fps = False) -> None:
             ##WINDOW PARAMETERS AND VARIABLES
        self.screenRes = screenRes
        self.max_fps = max_fps
        self.show_fps = show_fps
        self.screen = pygame.display.set_mode(self.screenRes)
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
        self.screen.fill((45, 175, 245))
        self.CameraMove()
        for object in self.objects:
            curr_object = self.objects[object]
            if curr_object.type != 'static' and self.is_editorMode == False:
                curr_object.update(self.deltatime) # update the object
                curr_object.collider(self.objects)
            self.renderObject(curr_object)


        if self.show_fps == True and self.is_editorMode == False:
            self.fps_counter(math.floor(self.clock.get_fps())) # display fps to the screen

        if self.is_editorMode == True:
            self.Editor.update(self)
        

    def flip(self): # display the frame to the screen
        self.clock.tick() #update the fps
        self.deltatime = self.clock.get_time() / 1000 # calculate the deltatime
        pygame.display.update() # show the screen to the player

    def createObject(self, object):
        if object.name == '':
            object.name = 'object_' + str(len(self.objects))
        self.objects[object.name] = object # add new object to the list

        print(f"[CHECK] {object.name.upper()} initialized")

    def fps_counter(self, fps):
        if self.show_fps == True:
            font = pygame.font.Font("Bin/assets/fonts/Roboto_Regular.ttf", 32)
            text = font.render(f'fps: {fps} ', True,(255,255,255))
            self.screen.blit(text, (0,0))   #diplay fps on demand

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
        else:
            if self.objToFollow != '':
                object = self.objects[self.objToFollow]
                width, height = self.screenRes
                self.camerax += (object.rect.x - (self.camerax + (width / 2)) + object.width / 2) * self.camDelayX * self.deltatime
                self.cameray += (object.rect.y - (self.cameray + (height / 2)) + object.height / 2) * self.camDelayY * self.deltatime


    def cam_position(self):
        return self.camerax, self.cameray


    def enableEditorMode(self):
        self.is_editorMode = True
    def disabelEditorMode(self):
        self.is_editorMode = False

    def is_object_inside_preview(self, object):
        x,y = self.screenRes
        if object.displayx + object.width > 0 and object.displayx < x \
            and object.displayy + object.height > 0 and object.displayy < y:
            return True
        else:
            return False

    def renderObject(self, object):
        object.displayx = object.rect.x - self.camerax
        object.displayy = object.rect.y - self.cameray

        if self.is_object_inside_preview(object) == True:
            self.screen.blit(object.img, (object.displayx, object.displayy))




class OBJECT():
    def __init__(self, img_path, name,type, start_pos=(0,0), function='') -> None:
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

    def __init__(self) -> None:
        self.Titlefont = pygame.font.Font('Bin/assets/fonts/Roboto_Regular.ttf', 32)
        self.Textfont = pygame.font.Font('Bin/assets/fonts/Roboto_Regular.ttf', 24)
    def update(self, window):
        for object in window.objects:
            curr_object = window.objects[object]
            pygame.draw.rect(window.screen, (124,252,0), pygame.Rect((curr_object.displayx,curr_object.displayy), (curr_object.width,curr_object.height)), width=2)

        self.CurrObjectTitle = self.Titlefont.render(f'player', True, (255,255,255))
        self.CurrObjectPos = self.Textfont.render(f"Position: {window.objects['player'].position()}", True, (255,255,255))

        displayResX, displayResY = window.screenRes
        self.editorWindow = pygame.Rect((0,0), (displayResX / 4, displayResY))

        screenResX, screenResY = window.screenRes

        screenFactorX = displayResX / screenResX 
        screenFactorY = displayResY / screenResY 


        mouseX = pygame.mouse.get_pos()[0] * screenFactorX
        mouseY = pygame.mouse.get_pos()[1] * screenFactorY
        clippedX = round(mouseX/100, 1) * 100
        clippedY = round(mouseY/100,1) * 100
        camX, camY = window.cam_position()
        pygame.draw.rect(window.screen, (0,0,0), pygame.Rect((clippedX, clippedY), (64,64)), width=2)

        
        if window.left_clicking == True:
            window.createObject(OBJECT('Bin/assets/images/player_prototype.png', '','static', start_pos=(clippedX + camX, clippedY + camY)))
        

        pygame.draw.rect(window.screen, (0,0,0), self.editorWindow)
        window.screen.blit(self.CurrObjectTitle ,(0,0))
        window.screen.blit(self.CurrObjectPos, (20 , 60))


