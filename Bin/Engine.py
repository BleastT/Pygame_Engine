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
        '"': 'R' ,
        '_': 'U' ,
        '-': 'M' ,
        '[': 'I',
        ']': 'C',
        '{': '&',
        '}': '#',
        '/': '}',
        '\\': '{',
        '(' : '\'',
        ')' : '(',
        '<' : 'Y',
        '>' : 'F'
    }
     
    def get_key_by_value(value):
        result = ''
        for key in code:
            curr_item = code[key]
            if curr_item == value:
               result = key
               break

        return result

    for text in text_to_encrypt:
        text_ = ''
        if mode == 0:
            for char in text.lower():
                text_ += code[char]
        else:
            for char in text:
                text_ += str(get_key_by_value(char))
        return_text.append(text_)

    return return_text

def convert_to_text(objects):
    text = []
    for object in objects:
        curr_object = objects[object]
        function_info = ''
        if curr_object.function != None:
            function_info = curr_object.function.__name__
        else:
            function_info = 'None'
        x,y = curr_object.start_pos
        text.append(f'{curr_object.img_path}, {curr_object.name}, {curr_object.type}, {x}, {y}, {function_info}, {curr_object.animated}, {curr_object.anim_path}')

    return text

def write_to_file(path, lines):
    file = open(path, 'w')
    final = ''

    for line in lines:
        final += line + '\n'

    file.writelines(final)

    file.close()

def read_from_file(path):
    file = open(path, 'r')
    final = []

    for line in file.readlines():
        line.replace('\n', '')
        final.append(line)

    file.close()
    return final

class APPLICATION():
    
    pygame.init()

    def __init__(self, screenRes, displayRes,max_fps = 60, show_fps=False, cam_Smooth=True, edit_mode=False, editor_width=400, editor_height=100, deltatime_used=False, window_name='pygame window') -> None:
             ##WINDOW PARAMETERS AND VARIABLES
        self.screenRes = screenRes
        self.displayRes = displayRes
        self.max_fps = max_fps
        self.show_fps = show_fps
        self.screenX, self.screenY = self.screenRes
        if edit_mode == True:
            self.screen = pygame.display.set_mode((self.screenX + editor_width, self.screenY + editor_height))
        else:
            self.screen = pygame.display.set_mode(self.screenRes)
        self.display = pygame.Surface(self.displayRes)
        pygame.display.set_caption(window_name)
            ##GAMEPLAY VARIABLES
        self.objects =  {}
        self.uiElements = {}
        self.functions = []
        self.editoruiElements = {}
        self.running = True
        self.clock = pygame.time.Clock()
        self.deltatime = 1
        self.deltatime_used = deltatime_used
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
            self.createUIElement(UITEXT(name='FPS', font_size=9))
        print(f'{bcolors.OKGREEN}[CHECK] WINDOW initialized{bcolors.ENDC}')

    def get(self, name):
        return self.objects[name]

    def load_functions(self, functions):
        for function in functions:
            self.functions.append(function)

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
            self.uiElements['FPS'].updateText(f'FPS: {math.floor(self.clock.get_fps())}') # display fps to the screen

        if self.is_editorMode == True:
            self.Editor.update(self)

        ###ADD Game UI ELEMENTS
        for ui in self.uiElements:
            currUI = self.uiElements[ui]
            self.display.blit(currUI.text, currUI.position())
        surf = pygame.transform.scale(self.display, self.screenRes)
        self.screen.blit(surf, (0,0))


        ###ADD Editor UI ELEMENTS
        for editorui in self.editoruiElements:
            currUI = self.editoruiElements[editorui]
            if type(currUI) == UIBUTTON:
                currUI.check_click(self)
                pygame.draw.rect(self.screen, (255,0,200), pygame.Rect(currUI.position(), (currUI.button_width, currUI.button_height)))
            self.screen.blit(currUI.text, currUI.position())

        self.clock.tick(self.max_fps) #update the fps
        if self.deltatime_used == True:
            self.deltatime = self.clock.get_time() / 1000 # calculate the deltatime
        pygame.display.update() # show the screen to the player
        

    def createObject(self, object):
        if object.name == '':
            object.name = 'object_' + str(object.rect.x) + str(object.rect.y)

        if object.function != None:
            for function in self.functions:
                if object.function == function.__name__:
                    object.function = function
        
        self.objects[object.name] = object # add new object to the list


        print(f"{bcolors.OKGREEN}[CHECK] {object.name.upper()} initialized{bcolors.ENDC}")

    def createUIElement(self, ui):
        if ui.name == '':
            ui.name = 'uiElement_' + str(ui.xpos) + str(ui.ypos)
        self.uiElements[ui.name] = ui

        print(f"{bcolors.OKGREEN}[CHECK] {ui.name.upper()} initialized{bcolors.ENDC}")
    def createEditorUIElement(self, ui):
        if ui.name == '':
            ui.name = 'editoruiElement_' + str(ui.xpos) + str(ui.ypos)
        self.editoruiElements[ui.name] = ui

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

    def save_map(self, file_path):
        try:
            write_to_file(file_path,encrypt_decrypt(convert_to_text(self.objects)))
            print(f'{bcolors.OKGREEN}[CHECK] - Map successfully saved{bcolors.ENDC}')
        except Exception as e:     
            print(f"{bcolors.FAIL}\n\n\n[ERROR] - During map save event{bcolors.ENDC}")
            print(f'{bcolors.FAIL}        {e}{bcolors.ENDC}')

    def load_map(self,file_path):
        try:
            objects = encrypt_decrypt(read_from_file(file_path), 1)
            self.objects.clear()
            for object in objects:
                parameter = object.replace(',', ' ').split()
                self.createObject(OBJECT(parameter[0], parameter[1], parameter[2], (float(parameter[3]), float(parameter[4])), parameter[5], parameter[6], parameter[7]))
            print(f'{bcolors.OKGREEN}[CHECK] - Map successfully loaded{bcolors.ENDC}')
        except Exception as e:
            print(f"{bcolors.FAIL}\n\n\n[ERROR] - During map load event{bcolors.ENDC}")
            print(f'        {e}')





class OBJECT():
    def __init__(self, img_path, name,type, start_pos=(0,0), function=None, animated=False, anim_path=None) -> None:
        self.img = pygame.image.load(img_path)
        self.img_path = img_path
        self.name = name
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.rect = pygame.Rect(start_pos, (self.width, self.height))
        self.start_pos = start_pos
        self.type = type
        self.function = function

        self.displayx = 0
        self.displayy = 0
        self.movement = [0,0]
        self.hitlist = []
        self.initialized_script = False
        self.animated = animated
        self.anim_path = anim_path
        if self.animated == True:
            self.animator = ANIMATOR()

  
    def move_by(self, x, y): # add a value to th existant position of the object
        self.rect.x += x
        self.rect.y += y

    def move_to (self, x , y): # set a new value to the position of the object
        self.rect.x = x
        self.rect.y = y

    def position(self): # return the position of the player
        return self.rect.x, self.rect.y
    def size(self):
        return self.width, self.height


    def update(self, deltatime):
        if self.function != None:
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
        window.createEditorUIElement(UITEXT(name='Titlefont', font_size=32, pos=(window.screenX, 0)))
        window.createEditorUIElement(UITEXT(name='SelectedObjectPos', font_size=24, pos=(window.screenX + 20, 60)))
        window.createEditorUIElement(UITEXT(name='CameraPos', font_size=24, pos=(window.screenX + 20, 100)))
        window.createEditorUIElement(UITEXT(name='GameMode', font_size=50, pos=(window.screenX / 2 - 50, 10), color=(255,0,0)))
        window.createEditorUIElement(UITEXT(name='Object type', font_size=20, pos=(window.screenX + 20, 150)))
        window.createEditorUIElement(UITEXT(name='Object function', font_size=20, pos=(window.screenX + 20, 200)))
        window.createEditorUIElement(UITEXT(name='Object name', font_size=20, pos=(window.screenX + 20, 250)))


        window.createEditorUIElement(UIBUTTON(name='Save_MAP', font_size=20 , pos=(window.screenX +20, 300)))
        window.createEditorUIElement(UIBUTTON(name='Load_MAP', font_size=20 , pos=(window.screenX +20, 350)))
        window.createEditorUIElement(UIBUTTON(name='Bind_Function', font_size=20 , pos=(window.screenX +20, 400), button_width=130))
        window.createEditorUIElement(UIBUTTON(name='Remove_Function', font_size=20 , pos=(window.screenX +160, 400), button_width=160))
        window.createEditorUIElement(UIBUTTON(name='Static', font_size=20 , pos=(window.screenX +20, 450)))
        window.createEditorUIElement(UIBUTTON(name='Fluid', font_size=20 , pos=(window.screenX +140, 450)))
        window.createEditorUIElement(UIBUTTON(name='Add_Name', font_size=20 , pos=(window.screenX +20, 500)))
        window.createEditorUIElement(UIBUTTON(name='Remove_Name', font_size=20 , pos=(window.screenX +140, 500), button_width=140))

        window.editoruiElements['Save_MAP'].updateText('Save Map')
        window.editoruiElements['Load_MAP'].updateText('Load Map')
        window.editoruiElements['Bind_Function'].updateText('Bind Function')
        window.editoruiElements['Remove_Function'].updateText('Remove Function')
        window.editoruiElements['Static'].updateText('Static')
        window.editoruiElements['Fluid'].updateText('Fluid')
        window.editoruiElements['Titlefont'].updateText('Game Informations')
        window.editoruiElements['Add_Name'].updateText('Add Name')
        window.editoruiElements['Remove_Name'].updateText('Remove Name')

        self.selectedObject = ''
        self.selectedImageToAdd = 'ground.png'
        self.img = pygame.image.load(f'Bin/assets/images/{self.selectedImageToAdd}')

        ## create Object parameters
        self.objectType = 'static'
        self.objectFunction = None
        self.objectName = ''
    def update(self, window):
        window.editoruiElements['Object type'].updateText(f'Object type: {self.objectType}')
        window.editoruiElements['Object function'].updateText(f'Object function: {self.objectFunction}')
        window.editoruiElements['Object name'].updateText(f'Object name: {self.objectName}')

        if self.selectedObject != '':
            window.editoruiElements['SelectedObjectPos'].updateText(f"Selected Object Position: {window.objects[self.selectedObject].position()}")
        else:
            window.editoruiElements['SelectedObjectPos'].updateText(f"Selected Object Position: N/A")

        window.editoruiElements['CameraPos'].updateText(f"Camera Position: ({window.camerax},{window.cameray})")
        if window.play == False:
            window.editoruiElements['GameMode'].updateText(f"PAUSE")
        else:
            window.editoruiElements['GameMode'].updateText(f"")

        screenResX, screenResY = window.screenRes
        displayResX, displayResY = window.displayRes
        screenFactorX = displayResX / screenResX 
        screenFactorY = displayResY / screenResY 


        mouseX = pygame.mouse.get_pos()[0] * screenFactorX
        mouseY = pygame.mouse.get_pos()[1] * screenFactorY
        clippedX = math.ceil(round(mouseX/10, 1) * 10)
        clippedY = math.ceil(round(mouseY/10,1) * 10)
        camX, camY = window.cam_position()

        objectPreviewRect = pygame.Rect((clippedX - self.img.get_height() / 2, clippedY - self.img.get_height() / 2), (self.img.get_width(), self.img.get_height()))
        if window.play == False and check_key_pressed(pygame.K_LSHIFT):
            # window.display.blit(self.img, (clippedX - self.img.get_height() / 2, clippedY - self.img.get_height() / 2))  
            pygame.draw.rect(window.display, (0,0,0), objectPreviewRect, 1) 
            if window.left_clicking == True:
                if len(window.objects) == 0:
                    window.createObject(OBJECT(f'Bin/assets/images/{self.selectedImageToAdd}', self.objectName,self.objectType, start_pos=(clippedX + camX - self.img.get_width() / 2, clippedY + camY - self.img.get_height() / 2), function=self.objectFunction))
                else:
                    for object in window.objects:
                        curr_object = window.objects[object]
                        if  self.check_mouse_inside(mouseX, mouseY, curr_object) == False:
                            window.createObject(OBJECT(f'Bin/assets/images/{self.selectedImageToAdd}', self.objectName ,self.objectType, start_pos=(clippedX + camX - self.img.get_width() / 2, clippedY + camY - self.img.get_height() / 2), function=self.objectFunction))
                            break
            elif window.right_clicking == True:
                for object in window.objects:
                    curr_object = window.objects[object]
                    if self.check_mouse_inside(mouseX, mouseY, curr_object):
                        window.objects.pop(object, None)
                        break      
        else:
            if window.left_clicking == True:
                for object in window.objects:
                    curr_object = window.objects[object]
                    if self.check_mouse_inside(mouseX, mouseY, curr_object):
                        self.selectedObject = object
                        break

        self.check_editor_buttons(window)

    def check_mouse_inside(self, mouseX, mouseY, object):
        if mouseX > object.displayx and mouseX < object.displayx + object.width \
            and mouseY > object.displayy and mouseY < object.displayy + object.height:
            return True
        else:
            return False


    def check_editor_buttons(self, window):
        for buttonNBR in window.editoruiElements:
            button = window.editoruiElements[buttonNBR]
            if type(button) == UIBUTTON:
                if button.check_click(window):          
                    if button.name == 'Save_MAP':
                        file = input(f'{bcolors.HEADER}Save file name: {bcolors.ENDC}')
                        window.save_map(f'Bin/assets/data/{file}')
                    elif button.name == 'Load_MAP':
                        file = input(f'{bcolors.HEADER}Load file name: {bcolors.ENDC}')
                        window.load_map(f'Bin/assets/data/{file}')
                    elif button.name == 'Bind_Function':
                        function = input(f'{bcolors.HEADER}Function name: {bcolors.ENDC}')
                        self.objectFunction = function
                    elif button.name == 'Remove_Function':
                        self.objectFunction = None
                    elif button.name == 'Static':
                        self.objectType = 'static'
                    elif button.name == 'Fluid':
                        self.objectType = 'fluid'
                    elif button.name == 'Add_Name':
                        name = input(f"{bcolors.HEADER}Object's name: {bcolors.ENDC}")
                        self.objectName = name
                    elif button.name == 'Remove_Name':
                        self.objectName = ''


        


class ANIMATOR():
    pass

class UI:
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

class UITEXT(UI):
    def __init__(self, name='', color=(255,255,255), font_path="Bin/assets/fonts/Roboto_Regular.ttf", pos=(0,0), font_size=20) -> None:
        super().__init__(name, color, font_path, pos, font_size)


class UIBUTTON(UI):
    def __init__(self, name='', color=(255,255,255), font_path="Bin/assets/fonts/Roboto_Regular.ttf", pos=(0,0), font_size=20, button_width=100, button_heigth=30) -> None:
        super().__init__(name, color, font_path, pos, font_size)
        self.x, self.y  = pos
        self.button_width = button_width
        self.button_height = button_heigth

    def check_click(self, window):
        if window.left_clicking == True:
            mouseX, mouseY = pygame.mouse.get_pos()
            if mouseX > self.x and mouseX < self.x + self.button_width \
                and mouseY > self.y and mouseY < self.y + self.button_height:
                return True
            else:
                return False



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'