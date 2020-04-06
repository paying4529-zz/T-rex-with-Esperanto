import os
import sys
import pygame
import random
from pygame import *

pygame.init()

scr_size = (width,height) = (1000,300)
FPS = 60
gravity = 0.4

black = (0,0,0)
white = (255,255,255)

background_col = (235,235,235)
background_col1 = (235,235,235)
background_col2 = (235,190,200)
background_col3 = (180,200,235)
background_col0 = (255,250,240)
background_col4 = (255,40,40)
background_col5 = (225,190,150)
background_col6 = (44,141,181)

high_score = 0

screen = pygame.display.set_mode(scr_size)
clock = pygame.time.Clock()
pygame.display.set_caption("T-Rex with Esperanto")

jump_sound = pygame.mixer.Sound('sprites/jump.wav')
die_sound = pygame.mixer.Sound('sprites/die.wav')
checkPoint_sound = pygame.mixer.Sound('sprites/checkPoint.wav')

def load_image(
    name,
    sizex=-1,
    sizey=-1,
    colorkey=None,
    folder='sprites'
    ):

    fullname = os.path.join(folder, name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))

    return (image, image.get_rect())

def load_sprite_sheet(
        sheetname,
        nx,
        ny,
        scalex = -1,
        scaley = -1,
        colorkey = None,
        folder='sprites'
        ):
    fullname = os.path.join(folder,sheetname)
    sheet = pygame.image.load(fullname)
    sheet = sheet.convert()

    sheet_rect = sheet.get_rect()

    sprites = []

    sizex = sheet_rect.width/nx
    sizey = sheet_rect.height/ny

    for i in range(0,ny):
        for j in range(0,nx):
            rect = pygame.Rect((j*sizex,i*sizey,sizex,sizey))
            image = pygame.Surface(rect.size)
            image = image.convert()
            image.blit(sheet,(0,0),rect)

            if colorkey is not None:
                if colorkey is -1:
                    colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey,RLEACCEL)

            if scalex != -1 or scaley != -1:
                image = pygame.transform.scale(image,(scalex,scaley))

            sprites.append(image)

    sprite_rect = sprites[0].get_rect()

    return sprites,sprite_rect

def disp_gameOver_msg(retbutton_image,gameover_image):
    image = pygame.Surface((420,65))
    image_rect=image.get_rect()
    image.fill(background_col4)
    image_rect.centerx = width / 2
    image_rect.centery = height*0.35

    image2 = pygame.Surface((390,45))
    image2_rect=image2.get_rect()
    image2.fill(background_col0)
    image2_rect.centerx = width / 2
    image2_rect.centery = height*0.35
    
    retbutton_rect = retbutton_image.get_rect()
    retbutton_rect.centerx = width / 2
    retbutton_rect.top = height*0.52

    gameover_rect = gameover_image.get_rect()
    gameover_rect.centerx = width / 2
    gameover_rect.centery = height*0.35

    screen.blit(image, image_rect)
    screen.blit(image2, image2_rect)
    screen.blit(retbutton_image, retbutton_rect)
    screen.blit(gameover_image, gameover_rect)

def disp_intro_msg(intro_image,n=0.1):
    intro_rect = intro_image.get_rect()
    intro_rect.centerx = width*0.57
    intro_rect.top = height*n

    screen.blit(intro_image, intro_rect)
    pygame.display.update()

def disp_question(question_image):
    image = pygame.Surface((750,200))
    image_rect=image.get_rect()
    image.fill(background_col6)
    image_rect.centerx = width / 2
    image_rect.centery = height*0.55

    image2 = pygame.Surface((720,170))
    image2_rect=image2.get_rect()
    image2.fill(background_col5)
    image2_rect.centerx = width / 2
    image2_rect.centery = height*0.55
    
    screen.blit(image, image_rect)
    screen.blit(image2, image2_rect)
    
    comet_image,comet_rect = load_image('stone.png',100,100,-1)
    x=random.randrange(0,20)
    #if x==0:
    question_image,question_rect = load_image('3.png',700,100,-1,folder="question")

    a_image,a_rect = load_image('A.png',75,96,-1,folder="question")
    b_image,b_rect = load_image('B.png',75,96,-1,folder="question")
    c_image,c_rect = load_image('C.png',75,96,-1,folder="question")

    q=random.randrange(1,26)
    verb_image,verb_rect = load_image('%d.png' % q,150,100,-1,folder="verb")

    t=random.randrange(1,4)
    qtype_image,qtype_rect = load_image('%d.png' % t,250,100,-1,folder="type")

    l=[1,2,3]
    random.shuffle(l)
    #print(l)
    c=1
    for ll in l:
        if ll==1:
            abc_image,abc_rect = load_image("%d.png" % q,150,90,-1,folder="verb_now")
        elif ll==2:
            abc_image,abc_rect = load_image("%d.png" % q,150,90,-1,folder="verb_past")
        elif ll==3:
            abc_image,abc_rect = load_image("%d.png" % q,150,90,-1,folder="verb_future")
        abc_rect = abc_image.get_rect()
        abc_rect.centery = height*0.68
        if c==1:
            abc_rect.left = width*0.2
        elif c==2:
            abc_rect.left = width*0.45
        elif c==3:
            abc_rect.left = width*0.7

        c+=1        
        screen.blit(abc_image,abc_rect)
        
    question_rect = question_image.get_rect()
    question_rect.centerx = width / 2
    question_rect.centery = height*0.45

    a_rect = a_image.get_rect()
    a_rect.centerx = width*0.172
    a_rect.centery = height*0.68

    b_rect = b_image.get_rect()
    b_rect.centerx = width*0.431
    b_rect.centery = height*0.68

    c_rect = c_image.get_rect()
    c_rect.centerx = width*0.68
    c_rect.centery = height*0.68

    verb_rect = verb_image.get_rect()
    verb_rect.centerx = width*0.76
    verb_rect.centery = height*0.45

    qtype_rect = qtype_image.get_rect()
    qtype_rect.centerx = width*0.51
    qtype_rect.centery = height*0.45
    
    comet_rect = comet_image.get_rect()
    comet_rect.centerx = width*0.85
    comet_rect.centery = height*0.3

    
    screen.blit(question_image, question_rect)
    screen.blit(a_image, a_rect)
    screen.blit(b_image, b_rect)
    screen.blit(c_image, c_rect)
    screen.blit(verb_image, verb_rect)
    screen.blit(qtype_image, qtype_rect)
    screen.blit(comet_image, comet_rect)

    #print(l.index(t))
    return l.index(t)
    
def extractDigits(number):
    if number > -1:
        digits = []
        i = 0
        while(number/10 != 0):
            digits.append(number%10)
            number = int(number/10)

        digits.append(number%10)
        for i in range(len(digits),5):
            digits.append(0)
        digits.reverse()
        return digits

class Dino():
    def __init__(self,sizex=-1,sizey=-1):
        self.images,self.rect = load_sprite_sheet('dino.png',5,1,sizex,sizey,-1)
        self.images1,self.rect1 = load_sprite_sheet('dino_ducking.png',2,1,118,sizey,-1)
        self.rect.bottom = int(0.98*height)
        self.rect.left = width/15
        self.image = self.images[0]
        self.index = 0
        self.counter = 0
        self.score = 0
        self.isJumping = False
        self.isDead = False
        self.isDucking = False
        self.isBlinking = False
        self.movement = [0,0]
        self.jumpSpeed = 15

        self.stand_pos_width = self.rect.width
        self.duck_pos_width = self.rect1.width

    def draw(self):
        screen.blit(self.image,self.rect)

    def checkbounds(self):
        if self.rect.bottom > int(0.98*height):
            self.rect.bottom = int(0.98*height)
            self.isJumping = False

    def update(self):
        if self.isJumping:
            self.movement[1] = self.movement[1] + gravity

        if self.isJumping:
            self.index = 0
        elif self.isBlinking:
            if self.index == 0:
                if self.counter % 400 == 399:
                    self.index = (self.index + 1)%2
            else:
                if self.counter % 20 == 19:
                    self.index = (self.index + 1)%2

        elif self.isDucking:
            if self.counter % 5 == 0:
                self.index = (self.index + 1)%2
        else:
            if self.counter % 5 == 0:
                self.index = (self.index + 1)%2 + 2

        if self.isDead:
           self.index = 4

        if not self.isDucking:
            self.image = self.images[self.index]
            self.rect.width = self.stand_pos_width
        else:
            self.image = self.images1[(self.index)%2]
            self.rect.width = self.duck_pos_width

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

        if not self.isDead and self.counter % 7 == 6 and self.isBlinking == False:
            self.score += 1
            if self.score % 100 == 0 and self.score != 0:
                if pygame.mixer.get_init() != None:
                    checkPoint_sound.play()

        self.counter = (self.counter + 1)


verb_now_sounds=[]
class Verb_now(pygame.sprite.Sprite):
    def __init__(self,speed=3.5,sizex=-1,sizey=-1):
        global verb_now_sounds
        pygame.sprite.Sprite.__init__(self,self.containers)
        x=random.randrange(1,26)
        self.images,self.rect = load_sprite_sheet('%d.png' % x,1,1,sizex,sizey,-1,folder="verb_now")
        self.image=self.images[0]
        self.rect.bottom = int(0.98*height)
        self.rect.left = width + self.rect.width
        self.movement = [-1*speed,0]
        self.mask = pygame.mask.from_surface(self.image)
        self.act=0
        
        verb_now_sound = pygame.mixer.Sound('verb_now/sound/%d.wav' % x)
        verb_now_sounds.append(verb_now_sound)

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:   
            self.kill()
    def overlap(self):
        self.kill()    

verb_future_sounds=[]
class Verb_future(pygame.sprite.Sprite):
    def __init__(self,speed=3.5,sizex=-1,sizey=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        x=random.randrange(1,26)
        self.images,self.rect = load_sprite_sheet('%d.png' % x,1,1,sizex,sizey,-1,folder="verb_future")
        self.image=self.images[0]
        self.rect.bottom = int(0.98*height)
        self.height = [height*0.82,height*0.75,height*0.65]
        self.rect.centery = self.height[random.randrange(0,3)]
        self.rect.left = width + self.rect.width
        self.movement = [-1*speed,0]
        self.mask = pygame.mask.from_surface(self.image)
        self.act=0

        verb_future_sound = pygame.mixer.Sound('verb_future/sound/%d.wav' % x)
        verb_future_sounds.append(verb_future_sound)

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:   
            self.kill()
    def overlap(self):
        self.kill()

verb_past_sounds=[]
class Verb_past(pygame.sprite.Sprite):
    def __init__(self,speed=3.5,sizex=-1,sizey=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        x=random.randrange(1,26)
        self.images,self.rect = load_sprite_sheet('%d.png' % x,1,1,sizex,sizey,-1,folder="verb_past")
        self.image=self.images[0]
        self.rect.bottom = int(0.98*height)
        self.height = [height*0.82,height*0.73,height*0.65]
        self.rect.centery = self.height[random.randrange(0,3)]
        self.rect.left = width + self.rect.width
        self.movement = [-1*speed,0]
        self.mask = pygame.mask.from_surface(self.image)
        self.act=0

        verb_past_sound = pygame.mixer.Sound('verb_past/sound/%d.wav' % x)
        verb_past_sounds.append(verb_past_sound)

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:   
            self.kill()
    
    def overlap(self):
        self.kill()

class Ground():
    def __init__(self,speed=-3.5):
        self.image,self.rect = load_image('ground.png',-1,-1,-1)
        self.image1,self.rect1 = load_image('ground.png',-1,-1,-1)
        self.rect.bottom = height
        self.rect1.bottom = height
        self.rect1.left = self.rect.right
        self.speed = speed

    def draw(self):
        screen.blit(self.image,self.rect)
        screen.blit(self.image1,self.rect1)

    def update(self):
        self.rect.left += self.speed
        self.rect1.left += self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect1.right

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right

class Cloud(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image,self.rect = load_image('cloud.png',int(90*35/42),35,-1)
        self.speed = 1
        self.rect.left = x
        self.rect.top = y
        self.movement = [-1*self.speed,0]

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:      
            self.kill()

class Scoreboard():
    def __init__(self,x=-1,y=-1):
        self.score = 0
        self.tempimages,self.temprect = load_sprite_sheet('numbers.png',12,1,15,int(15*6/5),-1)
        self.image = pygame.Surface((100,int(15*6/5)))
        self.rect = self.image.get_rect()
        if x == -1:
            self.rect.left = width*0.89
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = height*0.1
        else:
            self.rect.top = y

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self,score,background_col):
        score_digits = extractDigits(score)
        self.image.fill(background_col)##
        for s in score_digits:
            self.image.blit(self.tempimages[s],self.temprect)
            self.temprect.left += self.temprect.width
        self.temprect.left = 0


def introscreen():
    intro1_image,intro1_rect = load_image('1.jpg',850,250,-1,folder='question')
    intro2_image,intro2_rect = load_image('2.jpg',850,250,-1,folder='question')
    intro3_image,intro2_rect = load_image('4.png',815,290,-1,folder='question')
    temp_dino = Dino(88,94)
    temp_dino.isBlinking = True
    gameStart = False

    callout,callout_rect = load_image('call_out.png',200,105,-1)
    callout_rect.left = width*0.03
    callout_rect.top = height*0.3

    temp_ground,temp_ground_rect = load_sprite_sheet('ground.png',15,1,-1,-1,-1)
    temp_ground_rect.left = width/20
    temp_ground_rect.bottom = height

    logo,logo_rect = load_image('logo.png',730,160,-1)
    logo_rect.centerx = width*0.6
    logo_rect.centery = height*0.45

    pygame.display.update()

    s=-1
    while s==-1:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        s=0

        temp_dino.update()

        if pygame.display.get_surface() != None:
            screen.fill(background_col)  ##
            screen.blit(temp_ground[0],temp_ground_rect)
            if temp_dino.isBlinking:
                screen.blit(logo,logo_rect)
                screen.blit(callout,callout_rect)
            temp_dino.draw()

            pygame.display.update()
            
    screen.fill(background_col)
    while s==0:
        disp_intro_msg(intro1_image)
        #print("into1")
        pygame.display.update()
        
        temp_dino = Dino(88,94)
        temp_dino.isBlinking = True        
        temp_dino.update()

        if pygame.display.get_surface() != None:
            screen.blit(temp_ground[0],temp_ground_rect)
        temp_dino.draw()
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    s=1
    screen.fill(background_col)
    while s==1:
        disp_intro_msg(intro2_image)
        #print("into2")
        pygame.display.update()

        temp_dino = Dino(88,94)
        temp_dino.isBlinking = True        
        temp_dino.update()

        if pygame.display.get_surface() != None:
            screen.blit(temp_ground[0],temp_ground_rect)
        temp_dino.draw()
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    s=2
                    
    screen.fill(background_col)
    while s==2 and not gameStart:
        disp_intro_msg(intro3_image,n=0)
        pygame.display.update()

        temp_dino = Dino(88,94)
        temp_dino.isBlinking = True        
        temp_dino.update()

        if pygame.display.get_surface() != None:
            screen.blit(temp_ground[0],temp_ground_rect)
        temp_dino.draw()
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    s=3
                    temp_dino.isJumping = True
                    temp_dino.isBlinking = False
                    temp_dino.movement[1] = -1*temp_dino.jumpSpeed

        temp_dino.update()
        
        clock.tick(FPS)
        #print(temp_dino.isJumping)
        if temp_dino.isJumping == False and temp_dino.isBlinking == False:
            gameStart = True

def gameplay():
    global high_score
    global verb_now_sounds
    global verb_past_sounds
    global verb_future_sounds
    gamespeed = 3
    startMenu = False
    gameOver = False
    gameQuit = False
    gamePause = False
    playerDino = Dino(88,94)
    new_ground = Ground(-1*gamespeed)
    scb = Scoreboard()
    highsc = Scoreboard(width*0.78)
    counter = 0
    colornum=1
    background_col = (235,235,235)

    verb_past = pygame.sprite.Group()
    verb_now = pygame.sprite.Group()
    verb_future = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()

    Verb_past.containers = verb_past
    Verb_now.containers = verb_now
    Verb_future.containers = verb_future
    Cloud.containers = clouds

    retbutton_image,retbutton_rect = load_image('replay_button.png',50,45,-1)
    gameover_image,gameover_rect = load_image('game_over.png',360,22,-1)
    question_image,question_rect = load_image('3.png',400,100,-1,folder="question")
    

    temp_images,temp_rect = load_sprite_sheet('numbers.png',12,1,15,int(15*6/5),-1)
    HI_image = pygame.Surface((30,int(15*6/5)))
    HI_rect = HI_image.get_rect()
    HI_image.fill(background_col)  ##
    HI_image.blit(temp_images[10],temp_rect)
    temp_rect.left += temp_rect.width
    HI_image.blit(temp_images[11],temp_rect)
    HI_rect.top = height*0.1
    HI_rect.left = width*0.73

    type_images=[]
    type_images_rect=[]
    for k in range(1,4):
        temp2_images,temp2_rect = load_sprite_sheet('%d.png' %k,1,1,210,int(30*6/5),-1,folder="type")
        type_images.append(temp2_images[0])
        type_images_rect.append(temp2_rect)
    type_image = pygame.Surface((220,int(30*6/5)))
    type_rect = type_image.get_rect()
    type_image.fill(background_col)  ##
    type_image.blit(type_images[0],type_images_rect[0])
    type_images_rect[0].left -= type_images_rect[0].width
    type_rect.top = height*0.1
    type_rect.left = width*0.05
    
    while not gameQuit:
        while startMenu:
            pass
        while not gameOver and not gamePause:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if playerDino.rect.bottom == int(0.98*height):
                                playerDino.isJumping = True
                                if pygame.mixer.get_init() != None:
                                    jump_sound.play()
                                playerDino.movement[1] = -1*playerDino.jumpSpeed

                        if event.key == pygame.K_DOWN:
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            playerDino.isDucking = False

            x=random.randrange(0,2)
            a=pygame.sprite.groupcollide(verb_past, verb_now, x==0 , x==1, collided = None)
            if a:
                if x==1:
                    for aa in a.values():
                        l=len(aa)
                        verb_now_sounds=verb_now_sounds[:-l]
                else:
                    l=len(a.keys())
                    verb_past_sounds=verb_past_sounds[:-l]
            b=pygame.sprite.groupcollide(verb_past, verb_future, x==0 , x==1, collided = None)
            if b:
                if x==1:
                    for bb in b.values():
                        l=len(bb)
                        verb_future_sounds=verb_future_sounds[:-l]
                else:
                    l=len(b.keys())
                    verb_past_sounds=verb_past_sounds[:-l]
            c=pygame.sprite.groupcollide(verb_future, verb_now, x==0 , x==1, collided = None)
            if c:
                if x==1:
                    for cc in c.values():
                        l=len(cc)
                        verb_now_sounds=verb_now_sounds[:-l]
                else:
                    l=len(c.keys())
                    verb_future_sounds=verb_future_sounds[:-l]
                
            for p in verb_past:
                p.movement[0] = -1*gamespeed
                if pygame.sprite.collide_mask(playerDino,p):
                    if colornum%3 == 0:
                        playerDino.isDead = False   #####
                    elif colornum%3 == 1:
                        playerDino.isDead = False   #####
                    elif colornum%3 == 2:
                        playerDino.isDead = True   #####
                        if pygame.mixer.get_init() != None:
                            die_sound.play()
                if pygame.sprite.collide_rect_ratio(1.5)(playerDino,p) and p.act==0:
                    try:
                        if pygame.mixer.get_busy()<1:
                            verb_past_sounds[0].play()
                            verb_past_sounds=verb_past_sounds[1:]
                            p.act=1
                    except:
                        pass                     
                
            for n in verb_now:
                n.movement[0] = -1*gamespeed
                if pygame.sprite.collide_mask(playerDino,n):
                    if colornum%3 == 0:
                        playerDino.isDead = False    #####
                    elif colornum%3 == 1:
                        playerDino.isDead = True  #####
                        if pygame.mixer.get_init() != None:
                            die_sound.play()
                    elif colornum%3 == 2:
                        playerDino.isDead = False   #####
                if pygame.sprite.collide_rect_ratio(1.5)(playerDino,n) and n.act==0:
                    try:
                        if pygame.mixer.get_busy()<1:
                            verb_now_sounds[0].play()
                            verb_now_sounds=verb_now_sounds[1:]
                            n.act=1
                    except:
                        pass
                        
            for f in verb_future:
                f.movement[0] = -1*gamespeed
                if pygame.sprite.collide_mask(playerDino,f):
                    if colornum%3 == 0:
                        playerDino.isDead = True  #####
                        if pygame.mixer.get_init() != None:
                            die_sound.play()
                    elif colornum%3 == 1:
                        playerDino.isDead = False   #####
                    elif colornum%3 == 2:
                        playerDino.isDead = False   #####
                if pygame.sprite.collide_rect_ratio(1.5)(playerDino,f) and f.act==0:
                    try:
                        if pygame.mixer.get_busy()<1:
                            verb_future_sounds[0].play()
                            verb_future_sounds=verb_future_sounds[1:]
                            f.act=1
                    except:
                        pass                            
            
            if len(verb_past)+len(verb_past)+len(verb_past) < 20:
                if len(verb_past)+len(verb_past)+len(verb_past) == 0:
                    last_obstacle.empty()
                    x=random.randrange(0,5)
                    if x==0:
                        last_obstacle.add(Verb_past(gamespeed,80,80))
                    elif x==1:
                        last_obstacle.add(Verb_now(gamespeed,80,80))
                    elif x==2:
                        last_obstacle.add(Verb_future(gamespeed,80,80))
                    elif x==3 or x==4:
                        if colornum%3==1:
                            last_obstacle.add(Verb_now(gamespeed,80,80))
                        elif colornum%3==2:
                            last_obstacle.add(Verb_past(gamespeed,80,80))
                        elif colornum%3==0:
                            last_obstacle.add(Verb_future(gamespeed,80,80))
                else:
                    for l in last_obstacle:
                        if l.rect.right < width*0.7 and random.randrange(0,30) == 10:
                            last_obstacle.empty()
                            x=random.randrange(0,5)
                            if x==0:
                                last_obstacle.add(Verb_past(gamespeed,80,80))
                                break
                            elif x==1:
                                last_obstacle.add(Verb_now(gamespeed,80,80))
                                break
                            elif x==2:
                                last_obstacle.add(Verb_future(gamespeed,80,80))
                                break
                            elif x==3 or x==4:
                                if colornum%3==1:
                                    last_obstacle.add(Verb_now(gamespeed,80,80))
                                elif colornum%3==2:
                                    last_obstacle.add(Verb_past(gamespeed,80,80))
                                elif colornum%3==0:
                                    last_obstacle.add(Verb_future(gamespeed,80,80))

            if len(clouds) < 5 and random.randrange(0,300) == 10:
                Cloud(width,random.randrange(height/5,height/2))            
                    
            if playerDino.score >= 200*colornum:
                if colornum%3 == 0:
                    background_col=background_col1
                elif colornum%3 == 1:
                    background_col=background_col2
                elif colornum%3 == 2:
                    background_col=background_col3
                colornum+=1
                HI_image.fill(background_col)
                type_image.fill(background_col)
                
            if playerDino.score >= 100*colornum:
                x=random.randrange(1,1000)
                if x==1:
                    gamePause=True
                    #print("pause")
                              
            playerDino.update()
            verb_past.update()
            verb_now.update()
            verb_future.update()
            clouds.update()
            new_ground.update()
            scb.update(playerDino.score,background_col)
            highsc.update(high_score,background_col)

            if pygame.display.get_surface() != None:
                screen.fill(background_col)##
                new_ground.draw()
                clouds.draw(screen)
                scb.draw()
                if high_score != 0:
                    highsc.draw()
                    screen.blit(HI_image,HI_rect)
                screen.blit(type_images[colornum%3-1],type_rect)#####
                verb_past.draw(screen)
                verb_now.draw(screen)
                verb_future.draw(screen)
                playerDino.draw()

                pygame.display.update()
                
            clock.tick(FPS)

            if playerDino.isDead:
                gameOver = True
                if playerDino.score > high_score:
                    high_score = playerDino.score
                    
            if counter%700 == 699:
                new_ground.speed -= 0.2
                gamespeed += 0.2

            counter = (counter + 1)

        if gameQuit:
            break
        
        while gamePause:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = False
            else:
                ans=disp_question(question_image)
                playerDino.draw()
                pygame.display.update()
                while gamePause:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            gameQuit = True
                            gameOver = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_a and ans==0:
                                gameQuit = False
                                gameOver = False
                                gamePause = False
                            elif event.key == pygame.K_b and ans==1:
                                gameQuit = False
                                gameOver = False
                                gamePause = False
                            elif event.key == pygame.K_c and ans==2:
                                gameQuit = False
                                gameOver = False
                                gamePause = False
                            else:
                                gameQuit = False
                                gameOver = True
                                die_sound.play()
                                gamePause = False
            
        while gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameQuit = True
                            gameOver = False

                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            gameOver = False
                            verb_now_sounds=[]
                            verb_past_sounds=[]
                            verb_future_sounds=[]
                            gameplay()
            highsc.update(high_score,background_col)
            if pygame.display.get_surface() != None:
                disp_gameOver_msg(retbutton_image,gameover_image)
                if high_score != 0:
                    highsc.draw()
                    screen.blit(HI_image,HI_rect)
                pygame.display.update()
            clock.tick(FPS)

    pygame.quit()
    quit()

def main():
    isGameQuit = introscreen()
    if not isGameQuit:
        gameplay()

main()
