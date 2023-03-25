import tkinter
import time
from PIL import Image, ImageTk
from math import floor,ceil
import pygame

# Création du labyrinthe
def setup(lvl,blockSize,dim):
    global goal
    for x in range(dim[0]):
        for y in range(dim[1]):
            if lvl[y][x]!='0':
                Imgs.append(canvas.create_image(x*blockSize,y*blockSize,image=Tiles[lvl[y][x]],anchor='nw'))
            else:
                Orbs.append(orb(x*blockSize+blockSize/2,y*blockSize+blockSize/2))
                goal += 1
    tk.update()

# Pac Man
class player:
    def __init__(self,pos,size):
        self.x = pos[0]
        self.y = pos[1]
        self.cost = 1 # costume actuel
        self.speed = 5 # doit être un mulitple de blockSize
        self.size = size
        self.anim = False
        dir = ('d','l','r','u') # down, left, right, up
        self.imgs = []
        for d in dir:
            self.imgs.append([])
            for i in range (1,9):
                self.imgs[-1].append(ImageTk.PhotoImage(Image.open('assets/sprite/pacman-'+d+' '+str(i)+'.gif').resize((size,size))))
        self.dir = -2
        self.next_dir = -1
        self.im = canvas.create_image(self.x,self.y,image=self.imgs[2][0])
    def collide(self,dir):
        if dir==0:
            x1 = floor((self.x-self.size/2)/blockSize)
            x2 = ceil((self.x-self.size/2)/blockSize)
            y = ceil(self.y/blockSize)
            if (self.y+self.size/2)%blockSize==0 and ((lvl[y][x1]!='0' or lvl[y][x2]!='0') and (lvl[y][x1]!='X' or lvl[y][x2]!='X')):
                return True
            else:
                return False
        if dir==1:
            x = floor(self.x/blockSize)-1
            y1 = floor((self.y-self.size/2)/blockSize)
            y2 = ceil((self.y-self.size/2)/blockSize)
            if (self.x-self.size/2)%blockSize==0 and ((lvl[y1][x]!='0' or lvl[y2][x]!='0') and (lvl[y1][x]!='X' or lvl[y2][x]!='X')):
                return True
            else:
                return False
        if dir==2:
            x = ceil(self.x/blockSize)
            y1 = floor((self.y-self.size/2)/blockSize)
            y2 = ceil((self.y-self.size/2)/blockSize)
            if (self.x+self.size/2)%blockSize==0 and ((lvl[y1][x]!='0' or lvl[y2][x]!='0') and (lvl[y1][x]!='X' or lvl[y2][x]!='X')):
                return True
            else:
                return False
        if dir==3:
            x1 = floor((self.x-self.size/2)/blockSize)
            x2 = ceil((self.x-self.size/2)/blockSize)
            y = floor(self.y/blockSize)-1
            if (self.y-self.size/2)%blockSize==0 and ((lvl[y][x1]!='0' or lvl[y][x2]!='0') and (lvl[y][x1]!='X' or lvl[y][x2]!='X')):
                return True
            else:
                return False
    def frame(self):
        self.cost = (self.cost+1)%8
        if not(self.collide(self.next_dir)) and 0<=self.next_dir<=3:
            self.dir = self.next_dir
            self.next_dir = -1
        canvas.itemconfig(self.im,image=self.imgs[self.dir][self.cost])
        if not(self.collide(self.dir)):
            if self.dir==0:
                canvas.move(self.im,0,self.speed)
                self.y += self.speed
            if self.dir==1:
                canvas.move(self.im,self.speed*-1,0)
                self.x -= self.speed
            if self.dir==2:
                canvas.move(self.im,self.speed,0)
                self.x += self.speed
            if self.dir==3:
                canvas.move(self.im,0,self.speed*-1)
                self.y -= self.speed
        else:
            if self.collide(self.next_dir):
                self.next_dir = -1
        if self.x/blockSize==dim[0]-1 and self.dir==2:
            self.anim = True
            for i in range(2):
                for j in range (int(blockSize/self.speed)):
                    canvas.move(self.im,self.speed,0)
                    canvas.itemconfig(self.im,image=self.imgs[self.dir][self.cost])
                    tk.update()
                    if self.cost==7:
                        self.cost = 0
                    else:
                        self.cost += 1
                    time.sleep(delay)
                canvas.move(self.im,-dim[0]*blockSize,0)
                self.x = blockSize/2
            canvas.move(self.im,dim[0]*blockSize,0)
            self.x = blockSize
            self.anim = False
        if self.x==blockSize and self.dir==1:
            self.anim = True
            for i in range(2):
                for j in range (int(blockSize/self.speed)):
                    canvas.move(self.im,-self.speed,0)
                    canvas.itemconfig(self.im,image=self.imgs[self.dir][self.cost])
                    tk.update()
                    if self.cost==7:
                        self.cost = 0
                    else:
                        self.cost += 1
                    time.sleep(delay)
                canvas.move(self.im,dim[0]*blockSize,0)
                self.x = dim[0]*blockSize
            canvas.move(self.im,-dim[0]*blockSize,0)
            self.x = dim[0]*blockSize-blockSize
            self.anim = False
        tk.update()
    def set_dir(self,d):
        if not(self.anim):
            if self.collide(d):
                self.next_dir = d
            else:
                self.dir = d

# Fantômes
class ghost:
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.color = color
        self.dir = 1
        self.size = blockSize-5
        self.speed = 5
        self.cost = 0
        self.free = False
        self.imgs = []
        for i in range (1,7):
            self.imgs.append(ImageTk.PhotoImage(Image.open('assets/ghosts/ghost_'+str(self.color)+'_'+str(i)+'.gif').resize((self.size,self.size))))
        self.im = canvas.create_image(self.x,self.y,image=self.imgs[0])
    def wait(self):
        self.cost = (self.cost+1)%6
        canvas.itemconfig(self.im,image=self.imgs[self.cost])
    def frame(self):
        self.cost = (self.cost+1)%6
        canvas.itemconfig(self.im,image=self.imgs[self.cost])
        if not self.free:
            if self.x!=9.5*blockSize:
                if self.x<9.5*blockSize:
                    canvas.move(self.im,self.speed,0)
                    self.x += self.speed
                else:
                    canvas.move(self.im,self.speed*-1,0)
                    self.x -= self.speed
            else:
                canvas.move(self.im,0,self.speed*-1)
                self.y -= self.speed
                if self.y<=8.5*blockSize:
                    self.free = True
                    self.x,self.y = 9.5*blockSize,8.5*blockSize
        else:
            if not self.collide(self.dir):
                if self.dir==0:
                    canvas.move(self.im,0,self.speed)
                    self.y += self.speed
                if self.dir==1:
                    canvas.move(self.im,self.speed*-1,0)
                    self.x -= self.speed
                if self.dir==2:
                    canvas.move(self.im,self.speed,0)
                    self.x += self.speed
                if self.dir==3:
                    canvas.move(self.im,0,self.speed*-1)
                    self.y -= self.speed
            dx = self.x-pacman.x
            dy = self.y-pacman.y
            if abs(dx)<20 and abs(dy)<20:
                gameOver()
            if self.collide(self.dir):
                if abs(dx)>abs(dy):
                    if dx>0:
                        if not self.collide(1):
                            self.dir = 1
                        else:
                            if dy>0 and not self.collide(3):
                                self.dir = 3
                            elif not self.collide(0):
                                self.dir = 0
                            elif not self.collide(2):
                                self.dir = 2
                    else:
                        if not self.collide(2):
                            self.dir = 2
                        else:
                            if dy>0 and  not self.collide(3):
                                self.dir = 3
                            elif not self.collide(0):
                                self.dir = 0
                            elif not self.collide(1):
                                self.dir = 1
                else:
                    if dy>0:
                        if not self.collide(3):
                            self.dir = 3
                        else:
                            if dx>0 and not self.collide(1):
                                self.dir = 1
                            elif not self.collide(2):
                                self.dir = 2
                            elif not self.collide(0):
                                self.dir = 0
                    else:
                        if not self.collide(0):
                            self.dir = 0
                        else:
                            if dx>0 and not self.collide(1):
                                self.dir = 1
                            elif not self.collide(2):
                                self.dir = 2
                            elif not self.collide(3):
                                self.dir = 3
    def collide(self,dir):
        if dir==0:
            x1 = floor((self.x-blockSize/2)/blockSize)
            x2 = ceil((self.x-blockSize/2)/blockSize)
            y = ceil(self.y/blockSize)
            if (self.y+blockSize/2)%blockSize==0 and ((lvl[y][x1]!='0' or lvl[y][x2]!='0') and (lvl[y][x1]!='X' or lvl[y][x2]!='X')):
                return True
            else:
                return False
        if dir==1:
            x = floor(self.x/blockSize)-1
            y1 = floor((self.y-blockSize/2)/blockSize)
            y2 = ceil((self.y-blockSize/2)/blockSize)
            if (self.x-blockSize/2)%blockSize==0 and ((lvl[y1][x]!='0' or lvl[y2][x]!='0') and (lvl[y1][x]!='X' or lvl[y2][x]!='X')):
                return True
            else:
                return False
        if dir==2:
            x = ceil(self.x/blockSize)
            y1 = floor((self.y-blockSize/2)/blockSize)
            y2 = ceil((self.y-blockSize/2)/blockSize)
            if (self.x+blockSize/2)%blockSize==0 and ((lvl[y1][x]!='0' or lvl[y2][x]!='0') and (lvl[y1][x]!='X' or lvl[y2][x]!='X')):
                return True
            else:
                return False
        if dir==3:
            x1 = floor((self.x-blockSize/2)/blockSize)
            x2 = ceil((self.x-blockSize/2)/blockSize)
            y = floor(self.y/blockSize)-1
            if (self.y-blockSize/2)%blockSize==0 and ((lvl[y][x1]!='0' or lvl[y][x2]!='0') and (lvl[y][x1]!='X' or lvl[y][x2]!='X')):
                return True
            else:
                return False

# Collectables
class orb:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.size = 3
        self.active = True
        self.im = canvas.create_oval(x-self.size,y-self.size,x+self.size,y+self.size,fill='yellow',outlines=None)
    def frame(self):
        if abs(pacman.x-self.x)<15 and abs(pacman.y-self.y)<15 and self.active:
            global Score
            Score += 1
            canvas.delete(self.im)
            self.active = False

# Défaite
def gameOver():
    global game
    print('Perdu !\nScore :',Score)
    game = False
    pygame.mixer.music.stop()
    pygame.mixer.music.load('assets/sounds/gameOver.wav')
    pygame.mixer.music.play()

# Victoire
def win():
    global game
    print('Bravo!')
    game = False

# Déplacements
def right(event):
    pacman.set_dir(2)

def left(event):
    pacman.set_dir(1)

def up(event):
    pacman.set_dir(3)

def down(event):
    pacman.set_dir(0)

# Paramètres
blockSize = 30
dim = (19,22)
delay = 0.03

# Fenêtre graphique
tk = tkinter.Tk()
tk.title('Pac Man')
try:
    tk.iconbitmap('assets/logo/ghost.ico')
except:
    pass
canvas = tkinter.Canvas(tk,width=blockSize*dim[0],height=blockSize*dim[1],bg='black')
canvas.pack()

# Importation des images
Tiles = {'X' : 'blank',
         '1' : 'wall-corner-bl',
         '2' : 'wall-corner-br',
         '3' : 'wall-corner-ul',
         '4' : 'wall-corner-ur',
         '5' : 'wall-end-b',
         '6' : 'wall-end-l',
         '7' : 'wall-end-r',
         '8' : 'wall-end-u',
         '9' : 'wall-straight-horiz',
         'A' : 'wall-straight-vert',
         'B' : 'wall-t-b',
         'C' : 'wall-t-l',
         'D' : 'wall-t-r',
         'E' : 'wall-t-u',
         'F' : 'wall-x',
         'G' : 'wall-o',
         'H' : 'ghost-door'}
for t in Tiles:
    Tiles[t] = ImageTk.PhotoImage(Image.open('assets/tiles/'+Tiles[t]+'.gif').resize((blockSize,blockSize)))

# Initialisation des variables
Score = 0
lvl = open('assets/levels/level1.txt').readlines()
Imgs = []
Orbs = []
goal = 0
setup(lvl,blockSize,dim)

# Création de pacman et des fantômes
pacman = player((9.5*blockSize,16.5*blockSize),blockSize)
blinky = ghost(9.5*blockSize,8.5*blockSize,1)
pinky = ghost(10.5*blockSize,10.5*blockSize,4)
clide = ghost(9.5*blockSize,10.5*blockSize,3)
inky = ghost(8.5*blockSize,10.5*blockSize,2)
tk.update()

# Association des touches
canvas.bind_all('<Right>',right)
canvas.bind_all('<Left>',left)
canvas.bind_all('<Up>',up)
canvas.bind_all('<Down>',down)

# Démarrage de la musique
pygame.mixer.init()
pygame.mixer.music.load('assets/sounds/theme.wav')
pygame.mixer.music.play()

# Boucle principale
game = True
t = time.time()
blinky.free = True
while game:
    time.sleep(delay)
    pacman.frame()
    for o in Orbs:
        o.frame()
    blinky.frame()
    dt = time.time()-t
    if dt>15:
        pinky.frame()
        inky.frame()
        clide.frame()
    elif dt>10:
        pinky.wait()
        inky.frame()
        clide.frame()
    elif dt>5:
        pinky.wait()
        inky.wait()
        clide.frame()
    else:
        pinky.wait()
        inky.wait()
        clide.wait()
    if Score==goal:
        win()

canvas.mainloop()
