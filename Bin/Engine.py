import pygame
import sys
import math
import os

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

def convert_to_text(objects, uis):
    text = []
    for object in objects:
        curr_object = objects[object]
        function_info = ''
        if curr_object.function != None and curr_object.function != 'none':
            function_info = curr_object.function.__name__
        else:
            function_info = 'None'
        x,y = curr_object.start_pos
        text.append(f'object, {curr_object.img_path}, {curr_object.name}, {curr_object.type}, {curr_object.category}, {x}, {y}, {curr_object.width}, {curr_object.height}, {function_info}, {curr_object.animated}, {curr_object.anim_path}, {curr_object.collideable}')

    for ui in uis:
        curr_ui = uis[ui]
        # name='', color=(255,255,255), font_path="Bin/assets/fonts/Roboto_Regular.ttf", pos=(0,0), font_size=20, button_width=100, button_heigth=30
        if type(curr_ui) == UIBUTTON:
            text.append(f'button, {curr_ui.name}, {curr_ui.font_path}, {curr_ui.x}, {curr_ui.y}, {curr_ui.font_size}, {curr_ui.button_width}, {curr_ui.button_height}')
        elif type(curr_ui) == UITEXT:
            text.append(f'text, {curr_ui.name}, {curr_ui.font_path}, {curr_ui.x}, {curr_ui.y}, {curr_ui.font_size}')


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


    def __init__(self, screenRes, displayRes,max_fps = 60, show_fps=False, edit_mode=False, editor_width=430, editor_height=220  , window_name='pygame window') -> None:
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
        self.objects_to_add = {}
        self.objects_to_remove = []
        self.uiElements = {}
        self.functions = []
        self.editoruiElements = {}
        self.running = True
        self.clock = pygame.time.Clock()
        self.deltatime = 1
            ##CAMERA VARIABLES
        self.camerax = 0
        self.cameray = 0
        self.camDelayX = 1.7
        self.camDelayY = 1
        self.cameraxSpeed = 1
        self.cameraySpeed = 1
        self.follow_axis = (True, True)
        self.yView = 'center'
        self.xView = 'center'
        self.camBeforeEditMode = (0,0)
        self.objToFollow = ''
        self.cam_smooth = False
        self.loaded_map = ''

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
                    elif event.key == pygame.K_F11 and self.loaded_map != '':
                        self.play = False
                        self.load_map(f'Bin/assets/data/{self.loaded_map}')
                        self.camerax, self.cameray = (0,0)
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
            if curr_object.enabled:
                if self.play == True:
                    # try:
                    curr_object.update(self) # update the object
                    if curr_object.animated == True:
                        curr_object.img = curr_object.animator.updateAnimations(self.deltatime)
                    # except Exception as e:
                    #     print(f"{bcolors.FAIL}\n\n\n[ERROR] - During {curr_object.name} update function {bcolors.ENDC}")
                    #     print(f'        {e}')
                self.renderObject(curr_object)

        for obj in self.objects_to_add:
            curr_obj = self.objects_to_add[obj]
            self.objects[curr_obj.name] = curr_obj
        self.objects_to_add.clear()

        if self.is_editorMode == True:
            self.Editor.update(self)

        for obj in self.objects_to_remove:
            self.objects.pop(obj)
        self.objects_to_remove = []


        if self.show_fps == True and self.play == True:
            self.uiElements['FPS'].updateText(f'FPS: {math.floor(self.clock.get_fps())}') # display fps to the screen

        ###ADD Game UI ELEMENTS
        for ui in self.uiElements:
            currUI = self.uiElements[ui]
            if currUI.enabled == True:
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
        # print(self.clock.get_tick())
        self.deltatime = self.clock.get_time() / 1000 # calculate the deltatime
        pygame.display.update() # show the screen to the player
        

    def createObject(self, object):
        new_name = object.name
        curr_nbr = 0

        if new_name == '':
            new_name = 'object'

        if object.function != None and object.function != 'none':
            for function in self.functions:
                if object.function == function.__name__:
                    object.function = function
                    break

        while True:
            if new_name in self.objects:
                curr_nbr += 1
                if '_' in new_name:
                    new_name = new_name.split('_')[0] + '_' + str(curr_nbr)
                else:
                    new_name = new_name + '_' + str(curr_nbr)
                
            else:
                object.name = new_name
                self.objects_to_add[new_name] = object
                print(f"{bcolors.OKGREEN}[CHECK] {object.name.upper()} initialized{bcolors.ENDC}")
                break

    def createUIElement(self, ui):
        new_name = ui.name
        curr_nbr = 0

        if new_name == '':
            new_name = 'ui'

        while True:
            if new_name in self.objects:
                curr_nbr += 1
                if '_' in new_name:
                    new_name = new_name.split('_')[0] + '_' + str(curr_nbr)
                else:
                    new_name = new_name + '_' + str(curr_nbr)
            else:
                ui.name = new_name
                self.uiElements[new_name] = ui
                print(f"{bcolors.OKGREEN}[CHECK] {ui.name.upper()} initialized{bcolors.ENDC}")
                break

    def createEditorUIElement(self, ui):
        new_name = ui.name
        curr_nbr = 0

        if new_name == '':
            new_name = 'ui'

        while True:
            if new_name in self.objects:
                curr_nbr += 1
                if '_' in new_name:
                    new_name = new_name.split('_')[0] + '_' + str(curr_nbr)
                else:
                    new_name = new_name + '_' + str(curr_nbr)
            else:
                ui.name = new_name
                self.editoruiElements[new_name] = ui
                break


    def activateCameraFollow(self,name, follow_axis=(True, True), yView='center', xView='center', camDelay=(1,1)):
        self.objToFollow = name # set the cmerafollow
        self.follow_axis = follow_axis
        self.yView = yView
        self.xView = xView
        self.camDelayX, self.camDelayY = camDelay
    def deactivateCameraFollow(self):
        self.objToFollow = ''

    def CameraMove(self):
        if self.play == False and self.is_editorMode == True:
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
                x,y = self.follow_axis
                if x == True:
                    if self.xView == 'center':
                        self.camerax += (object.rect.x - (self.camerax + (width / 2)) + object.width / 2) * self.camDelayX
                    if self.xView == 'right':
                        self.camerax += (object.rect.x - (self.camerax + (width / 2)) + object.width / 2 + (width / 4)) * self.camDelayX
                    if self.xView == 'left':
                        self.camerax += (object.rect.x - (self.camerax + (width / 2)) + object.width / 2 - (width / 4)) * self.camDelayX
                    
                if y == True:
                    if self.yView == 'center':
                        self.cameray += (object.rect.y - (self.cameray + (height / 2)) + object.height / 2) * self.camDelayY
                    elif self.yView == 'top':
                        self.cameray += (object.rect.y - (self.cameray + (height / 2)) + object.height / 2  - (height / 4)) * self.camDelayY
                    elif self.yView == 'bottom':
                        self.cameray += (object.rect.y - (self.cameray + (height / 2)) + object.height / 2  + (height / 4)) * self.camDelayY


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
        if object.img != None:
            object.displayx = object.rect.x - self.camerax
            object.displayy = object.rect.y - self.cameray

            if self.is_object_inside_preview(object) == True:
                self.display.blit(object.img, (object.displayx, object.displayy))

    def save_map(self, file_path):
        try:
            write_to_file(file_path,encrypt_decrypt(convert_to_text(self.objects, self.uiElements)))
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
                if parameter[0] == 'object':
                    if parameter[10] == 'true':
                        parameter[10] = True
                    elif parameter[10] == 'false':
                        parameter[10] = False

                    if parameter[8] == 'true':
                        parameter[8] = True
                    elif parameter[8] == 'false':
                        parameter[8] = False
                    # text.append(f'{curr_object.img_path}, {curr_object.name}, {curr_object.type}, {x}, {y}, {curr_object.width}, {curr_object.height}, {function_info}, {curr_object.animated}, {curr_object.anim_path}, {curr_object.collideable}')
                    self.createObject(OBJECT(parameter[1], parameter[2], parameter[3],parameter[4], (float(parameter[5]), float(parameter[6])), (float(parameter[7]), float(parameter[8])), parameter[9], parameter[10], parameter[11], parameter[12]))
                elif parameter[0] == 'button':
                    pass
                elif parameter[0] == 'text':
                    pass
            print(f'{bcolors.OKGREEN}[CHECK] - Map successfully loaded{bcolors.ENDC}')
        except Exception as e:
            print(f"{bcolors.FAIL}\n\n\n[ERROR] - During map load event{bcolors.ENDC}")
            print(f'        {e}')

class OBJECT():
    def __init__(self, img_path, name='',type='static',category=None, start_pos=(0,0), size=(0,0), function=None, animated=False, anim_path=None, collideable=False) -> None:
        self.img = pygame.image.load(img_path)
        if size != (0,0):
            self.image = pygame.transform.scale(self.img, size)
        self.img_path = img_path
        self.name = name
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.rect = pygame.Rect(start_pos, (self.width, self.height))
        self.start_pos = start_pos
        self.type = type
        self.function = function
        self.collideable = collideable
        self.enabled = True
        self.category = category

        self.displayx = 0
        self.displayy = 0
        self.movement = [0,0]
        self.hitlist = []
        self.initialized_script = False
        self.animated = animated
        self.anim_path = anim_path
        if self.animated == True:
            self.animator = ANIMATOR(anim_path, (self.width, self.height))

        self.all_collision = []
        
        self.appRef = None

  
    def move_by(self, x, y): # add a value to th existant position of the object
        self.all_collision = []
        self.collision_types = {'Top': False, 'Bottom':False, 'Left':False, 'Right':False}
        self.rect.x += x
        hitlist = self.collision_test(self.appRef.objects)
        if self.collideable == True:
            for other in hitlist:
                    if x > 0:
                        self.rect.right = other.left
                        self.collision_types['Right'] = True
                    elif x < 0:
                        self.rect.left = other.right
                        self.collision_types['Left'] = True

        self.rect.y += y
        hitlist = self.collision_test(self.appRef.objects)
        if self.collideable == True:
            for other in hitlist:
                    if y > 0:
                        self.rect.right = other.left
                        self.collision_types['Right'] = True
                    elif y < 0:
                        self.rect.left = other.right
                        self.collision_types['Left'] = True




        self.rect.y += y

    def move_to (self, x , y): # set a new value to the position of the object
        self.rect.x = x
        self.rect.y = y

    def position(self): # return the position of the player
        return self.rect.x, self.rect.y
    def size(self):
        return self.width, self.height


    def update(self, app):
        self.appRef = app

        if self.function != None and self.function != 'none':
            return self.function(self)
        else:
           return 

    def delete(self):
        self.appRef.objects_to_remove.append(self.name)
    def collision_test(self, objects):
        hitlist = []
        for object in objects:
            curr_object = objects[object]
            if curr_object == self:
                pass
            else:
                if self.rect.colliderect(curr_object.rect):
                    self.all_collision.append([curr_object.name, curr_object.category])
                    if curr_object.collideable == True:
                        hitlist.append(curr_object.rect)

        return hitlist


    def collided_with(self, name, type=0, delete=False):
        for col in self.all_collision:
            if col[type] == name:
                if delete == True:
                    self.appRef.objects[col[0]].delete()
                    return True
class EDITOR():

    def __init__(self,window) -> None:
        window.createEditorUIElement(UITEXT(name='Titlefont', font_size=32, pos=(window.screenX, 0)))
        window.createEditorUIElement(UITEXT(name='CameraPos', font_size=24, pos=(window.screenX + 20, 60)))
        window.createEditorUIElement(UITEXT(name='ObjectPos', font_size=20, pos=(window.screenX + 20, 110)))
        window.createEditorUIElement(UITEXT(name='ObjectName', font_size=20, pos=(window.screenX + 20, 160)))
        window.createEditorUIElement(UITEXT(name='GameMode', font_size=50, pos=(window.screenX / 2 - 50, 10), color=(255,0,0)))
        window.createEditorUIElement(UITEXT(name='Object type', font_size=20, pos=(window.screenX + 20, 210)))
        window.createEditorUIElement(UITEXT(name='Object function', font_size=20, pos=(window.screenX + 20, 260)))
        window.createEditorUIElement(UITEXT(name='Object name', font_size=20, pos=(window.screenX + 20, 310)))
        window.createEditorUIElement(UITEXT(name='Object image', font_size=20, pos=(window.screenX + 20, 360)))
        window.createEditorUIElement(UITEXT(name='CollideableText', font_size=20, pos=(window.screenX + 20, 410)))
        window.createEditorUIElement(UITEXT(name='AnimatedText', font_size=20, pos=(window.screenX + 20, 460)))


        window.createEditorUIElement(UIBUTTON(name='Save_MAP', font_size=20 , pos=(window.screenX +20, 510)))
        window.createEditorUIElement(UIBUTTON(name='Load_MAP', font_size=20 , pos=(window.screenX +140, 510)))
        window.createEditorUIElement(UIBUTTON(name='Modify_Object', font_size=20 , pos=(window.screenX +20, 710), button_width=130))
        window.createEditorUIElement(UIBUTTON(name='Modify_tile_Object', font_size=20 , pos=(window.screenX +140, 710), button_width=130))
        window.createEditorUIElement(UIBUTTON(name='Images_Left', font_size=20 , pos=(10, window.screenY + 20)))
        window.createEditorUIElement(UIBUTTON(name='Images_Right', font_size=20 , pos=(600, window.screenY + 20)))


        window.editoruiElements['Save_MAP'].updateText('Save Map')
        window.editoruiElements['Load_MAP'].updateText('Load Map')
        window.editoruiElements['Titlefont'].updateText('Game Informations')
        window.editoruiElements['Modify_Object'].updateText('Modify Object')
        window.editoruiElements['Images_Left'].updateText('Left')
        window.editoruiElements['Images_Right'].updateText('Right')
        window.editoruiElements['Modify_tile_Object'].updateText('Modify tile properties')

            
        self.images = []
        self.currImageList = 0
        
        images_names = os.listdir('Bin/assets/images')
        images_array = []
        image_int = 1
        for image in images_names:
            if image_int > 6:
                self.images.append(images_array)
                images_array = []
                image_int = 0

            images_array.append(image)
            image_int += 1

        self.images.append(images_array)


        self.selectedObject = ''
        self.selectedImageToAdd = self.images[self.currImageList][0]
        self.img = pygame.image.load(f'Bin/assets/images/{self.selectedImageToAdd}')
        window.editoruiElements['Object image'].updateText(f'Object image: {self.selectedImageToAdd}')

        ## create Object parameters
        self.obj_Category = ''
        self.objectType = 'static'
        self.anim_path = None
        self.animated = False
        self.objectFunction = None
        self.is_Collideable = False
        self.objectName = ''
        self.loaded_MAP = ''
    def update(self, window):

        if self.selectedObject != '':
            window.editoruiElements['ObjectPos'].updateText(f"Object Position: {window.get(self.selectedObject).position()}")
            window.editoruiElements['ObjectName'].updateText(f"Object Name: {self.selectedObject}")
            window.editoruiElements['Object type'].updateText(f'Object type: {window.get(self.selectedObject).type}')
            if type(window.get(self.selectedObject).function).__name__ == 'function':
                window.editoruiElements['Object function'].updateText(f'Object function: {window.get(self.selectedObject).function.__name__}')
            else:
                window.editoruiElements['Object function'].updateText(f'Object function: {window.get(self.selectedObject).function}')

            window.editoruiElements['Object name'].updateText(f'Object name: {window.get(self.selectedObject).name}')
            window.editoruiElements['CollideableText'].updateText(f'Is Object Collideable: {window.get(self.selectedObject).collideable}')
            window.editoruiElements['AnimatedText'].updateText(f'Is Object Animated: {window.get(self.selectedObject).animated}')
        else:
            window.editoruiElements['ObjectPos'].updateText(f"Object Position: N/A")
            window.editoruiElements['ObjectName'].updateText(f"Object Name: N/A")
            window.editoruiElements['Object type'].updateText(f'Object type: N/A')
            window.editoruiElements['Object function'].updateText(f'Object function: N/A')
            window.editoruiElements['Object name'].updateText(f'Object name: N/A')
            window.editoruiElements['CollideableText'].updateText(f'Is Object Collideable: N/A')
            window.editoruiElements['AnimatedText'].updateText(f'Is Object Animated: N/A')

        window.editoruiElements['CameraPos'].updateText(f"Camera Position: ({round(window.camerax)},{round(window.cameray)})")
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
        clippedX = math.ceil(round(mouseX/80, 1) * 80)
        clippedY = math.ceil(round(mouseY/80,1) * 80)
        camX, camY = window.cam_position()

        objectPreviewRect = pygame.Rect((clippedX - self.img.get_height() / 2, clippedY - self.img.get_height() / 2), (self.img.get_width(), self.img.get_height()))
        if window.play == False and check_key_pressed(pygame.K_LSHIFT):
            # window.display.blit(self.img, (clippedX - self.img.get_height() / 2, clippedY - self.img.get_height() / 2))  
            pygame.draw.rect(window.display, (0,0,0), objectPreviewRect, 1) 

            if window.left_clicking == True:
                window.createObject(OBJECT(f'Bin/assets/images/{self.selectedImageToAdd}', self.objectName ,self.objectType,self.obj_Category, start_pos=(clippedX + camX - self.img.get_width() / 2, clippedY + camY - self.img.get_height() / 2), function=self.objectFunction,animated=self.animated, anim_path=self.anim_path, collideable=self.is_Collideable))
            elif window.right_clicking == True:
                for object in window.objects:
                    curr_object = window.objects[object]
                    if self.check_mouse_inside(mouseX, mouseY, curr_object):
                        window.objects.pop(object, None)
                        self.selectedObject = ''
                        break      
        else:
            if window.left_clicking == True:
                for object in window.objects:
                    curr_object = window.objects[object]
                    if self.check_mouse_inside(mouseX, mouseY, curr_object):
                        self.selectedObject = object
                        break

        ## draw tiles images preview
        mX, my = pygame.mouse.get_pos()
        xOffset = 100
        for image in self.images[self.currImageList]:
            image_ = pygame.image.load(f'Bin/assets/images/{image}')
            image_ = pygame.transform.scale(image_, (64,64))
            if window.left_clicking == True:
                if mX > xOffset + 30 and mX < xOffset + 30 + image_.get_width() \
                and my > window.screenY + 20 and my < window.screenY + 20 + image_.get_height():
                    print('changed preview image')
                    self.selectedImageToAdd = image
                    self.img = pygame.image.load(f'Bin/assets/images/{self.selectedImageToAdd}')
                    window.editoruiElements['Object image'].updateText(f'Object image: {self.selectedImageToAdd}')
            rect = pygame.Rect((xOffset + 30, window.screenY + 20), image_.get_size())
            window.screen.blit(image_, (rect.x, rect.y))
            pygame.draw.rect(window.screen, (255,255,255), rect, 1)
            xOffset += image_.get_width() + 15

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
                        window.loaded_map = input(f'{bcolors.HEADER}Load file name: {bcolors.ENDC}')
                        window.load_map(f'Bin/assets/data/{window.loaded_map}')
                    elif button.name == 'Images_Left':
                        if len(self.images) > 1:
                            if self.currImageList == 0:
                                self.currImageList = len(self.images) - 1
                            else:
                                self.currImageList -= 1
                    elif button.name == 'Images_Right':
                        if len(self.images) > 1:
                            if self.currImageList == len(self.images) - 1:
                                self.currImageList = 0
                            else:
                                self.currImageList += 1
                    elif button.name == 'Modify_Object':
                        if self.selectedObject != '':
                            propertie = input(f'{bcolors.HEADER}Property to modify(name/function/type/pos/collision/anim/category/image): {bcolors.ENDC}')
                            if propertie == 'name':
                                window.objects[self.selectedObject].name = input(f'{bcolors.HEADER}Enter a new name(lower Case): {bcolors.ENDC}')
                            elif propertie == 'type':
                                window.objects[self.selectedObject].type = input(f'{bcolors.HEADER}Enter a new type(static, fluid): {bcolors.ENDC}')
                            elif propertie == 'function':
                                function =  input(f'{bcolors.HEADER}Enter a new function(lower Case): {bcolors.ENDC}')
                                for function_ in window.functions:
                                    if function == function_.__name__:
                                        window.objects[self.selectedObject].function = function_
                                        break
                            elif propertie == 'pos':
                                window.objects[self.selectedObject].start_pos = (float(input(f'{bcolors.HEADER}Enter a new X coordinate: {bcolors.ENDC}')), float(input(f'{bcolors.HEADER}Enter a new Y coordinate: {bcolors.ENDC}')))
                            elif propertie == 'collision':
                                col = input(f'{bcolors.HEADER}Is object collideable(True=1/False=2): {bcolors.ENDC}')
                                if col == '1':
                                    col = True
                                else:
                                    col = False
                                window.objects[self.selectedObject].colldeable = col
                            elif propertie == 'anim':
                                anim = input(f"{bcolors.HEADER}Animation folder name: {bcolors.ENDC}")
                                if anim == '':
                                    window.objects[self.selectedObject].animated = False
                                else:
                                    window.objects[self.selectedObject].animated = anim
                                    window.objects[self.selectedObject].anim_path = False
                            elif propertie == 'category':
                                window.objects[self.selectedObject].category = input(f'{bcolors.HEADER}Object Category(lowercase): {bcolors.ENDC}')
                            elif propertie == 'image':
                                window.objects[self.selectedObject].img_path = input('Image Path: ')
                                window.objects[self.selectedObject].image = pygame.image.load(window.objects[self.selectedObject].img_path)
                            window.save_map(f'Bin/assets/data/{window.loaded_map}')
                            window.load_map(f'Bin/assets/data/{window.loaded_map}')

                        else:
                            print(f'{bcolors.WARNING}No object was selectionned.{bcolors.ENDC}')
                            print(f'{bcolors.WARNING}Please select an object to continue{bcolors.ENDC}')
                        
                    elif button.name == 'Modify_tile_Object':
                        self.objectName = input(f"{bcolors.HEADER}Object Name(lowercase): {bcolors.ENDC}")
                        self.anim_path = input(f'{bcolors.HEADER}Animation folder path: {bcolors.ENDC}')
                        if self.anim_path == '':
                            self.anim_path = None
                        else:
                            self.animated = True
                        self.objectFunction = input(f"{bcolors.HEADER}Function Name: {bcolors.ENDC}")
                        if self.objectFunction == '':
                            self.objectFunction = None
                        self.is_Collideable = input(f"{bcolors.HEADER}Is object collideable(True=1/False=2): {bcolors.ENDC}")
                        if self.is_Collideable == '1':
                            self.is_Collideable = True
                        else:
                            self.is_Collideable = False
                        self.objectType = input(f"{bcolors.HEADER}Object type(static or not): {bcolors.ENDC}")
                        self.obj_Category = input(f"{bcolors.HEADER}Object Category: {bcolors.ENDC}")
                        

class ANIMATOR():
    def __init__(self, anim_path, size) -> None:
        self.size = size
        self.anim_path = anim_path
        self.animStates = {}
        for folder in os.listdir(self.anim_path):
            array = []
            for file in os.listdir(self.anim_path + '/' + folder):
                array.append(pygame.image.load(self.anim_path + '/' + folder + '/' + file))
            self.animStates[folder] = array
        self.currAnimState = None
        self.currFrame = 0
        self.timeperFrame = 1
        self.currTime = 0

    def changeAnimState(self, state, time=1):
        self.currAnimState = state
        self.timeperFrame = time

    def updateAnimations(self, deltatime):
        frame = self.animStates[self.currAnimState][self.currFrame]
        frame = pygame.transform.scale(frame, self.size)
        self.currTime += deltatime
        # print(self.currTime)
        if self.currTime > self.timeperFrame:
            self.currFrame += 1
            if self.currFrame > len(self.animStates[self.currAnimState]) - 1:
                self.currFrame = 0
            self.currTime = 0
        return frame


class UI:
    def __init__(self, name='', color=(255,255,255), font_path="Bin/assets/fonts/Roboto_Regular.ttf", pos=(0,0), font_size=20) -> None:
        self.x, self.y = pos
        self.name = name
        self.color = color
        self.font_size = font_size
        self.font_path = font_path
        self.font = pygame.font.Font(font_path, font_size)
        self.text_content = ''
        self.text = self.font.render(self.text_content, True, self.color) 
        self.enabled = True

    def updateText(self, new_text):
        self.text_content = new_text
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.text = self.font.render(self.text_content, True,self.color)

    def position(self):
        return self.x, self.y

class UITEXT(UI):
    def __init__(self, name='', color=(255,255,255), font_path="Bin/assets/fonts/Roboto_Regular.ttf", pos=(0,0), font_size=20) -> None:
        super().__init__(name, color, font_path, pos, font_size)


class UIBUTTON(UI):
    def __init__(self, name='', color=(255,255,255), font_path="Bin/assets/fonts/Roboto_Regular.ttf", pos=(0,0), font_size=20, button_width=100, button_heigth=30) -> None:
        super().__init__(name, color, font_path, pos, font_size)
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