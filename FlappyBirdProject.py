import pygame
from random import randint
import os
# set correct path for windows
current_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_path)
#setting window
width,height=288,512
screen=pygame.display.set_mode((width,height))
#images used
background= pygame.image.load("./images/background.png")
bird=pygame.image.load("./images/bird.png")
base=pygame.image.load("./images/floor.png")
upperpipe=pygame.image.load("./images/upper-pipe.png")
lowerpipe=pygame.image.load("./images/lower-pipe.png")
over=pygame.image.load("./images/gameover.png")
zero=pygame.image.load("./images/numbers/0.png")
one=pygame.image.load("./images/numbers/1.png")
two=pygame.image.load("./images/numbers/2.png")
three=pygame.image.load("./images/numbers/3.png")
four=pygame.image.load("./images/numbers/4.png")
five=pygame.image.load("./images/numbers/5.png")
six=pygame.image.load("./images/numbers/6.png")
seven=pygame.image.load("./images/numbers/7.png")
eight=pygame.image.load("./images/numbers/8.png")
nine=pygame.image.load("./images/numbers/9.png")

#variables used:
BirdXaxis=144 #location of bird on x-axis
BirdYaxis=256 #location of bird on y-axis
Birdspeed=0 #the velocity of the bird
ground=425
xlocation=576 #location of pipes on x-axis
PipeHeight=randint(50,300) #This generates a random number within this range and uses it a the upper pipe's height
space=120 # gap between upper and lower pipes
PipeSpeed=2.5 # how much the pipes shift to the left
counter=0
beige=(255,240,180)	
black=(0,0,0)
salmon=(255,99,71)	
Gravity=True

#functions
def obstacle(xlocation,PipeHeight):
    #This function displays a set of upper and lower pipes with random heights each time 
    screen.blit(upperpipe,(xlocation,0),(0,(320-PipeHeight),55,PipeHeight))
    screen.blit(lowerpipe,(xlocation,int(PipeHeight+space)))

def ScoreImage(counter,locationX,locationY):
    #This function displays the score using images of the number
    #Example: if the score is 12, the function searches for the images of the numbers 1 and 2 and displays them next to one another
    for i in str(counter):
        if i=='0':
            screen.blit(zero,(locationX,locationY))
            numberwidth=zero.get_size()[0]
        elif i=='1':
            screen.blit(one,(locationX,locationY))
            numberwidth=one.get_size()[0]
        elif i=='2':
            screen.blit(two,(locationX,locationY))
            numberwidth=two.get_size()[0]
        elif i=='3':
            screen.blit(three,(locationX,locationY))
            numberwidth=three.get_size()[0]
        elif i=='4':
            screen.blit(four,(locationX,locationY))
            numberwidth=four.get_size()[0]
        elif i=='5':
            screen.blit(five,(locationX,locationY))
            numberwidth=five.get_size()[0]
        elif i=='6':
            screen.blit(six,(locationX,locationY))
            numberwidth=six.get_size()[0]
        elif i=='7':
            screen.blit(seven,(locationX,locationY))
            numberwidth=seven.get_size()[0]
        elif i=='8':
            screen.blit(eight,(locationX,locationY))
            numberwidth=eight.get_size()[0]
        else:
            screen.blit(nine,(locationX,locationY))
            numberwidth=nine.get_size()[0]
        locationX=locationX+numberwidth

def highscore(counter):
    #This function compares the score stored in the high score file with your current score, if it less,then your current score is saved as the highest score,otherwise,it stays the same
    f = open ("HighScore.txt",'r')
    line=f.readline()
    if line !="":
        line=int(line)
        if counter>line:
            f=open("HighScore.txt",'w')
            f.write(str(counter))
            f=open("HighScore.txt",'r')
            line=f.read()
    f.close()
    return line

def scoreboard(counter):
    #this function creates a score board; it draws a rectangle and displays your current score and your highest score
    pygame.draw.rect(screen,beige,(50,250,200,90))
    pygame.draw.rect(screen,black,(50,250,200,90),2)    
    myfont = pygame.font.SysFont('Comic Sans MS', 21)
    redtext = myfont.render('Score', False,salmon)
    redtext2 = myfont.render('Best', False,salmon)    
    screen.blit(redtext,(70,255))  
    screen.blit(redtext2,(180,255))
    ScoreImage(counter,90,285)
    ScoreImage(highscore(counter),190,285)

def gameover():
    #This function displays an image with the caption "Game Over" and displays the score board underneath it
    screen.blit(over,(50,200))
    scoreboard(counter)
    message_display("Press A to play again!")
def text_objects(text, font):
    TextSurface = font.render(text, True, black)
    return TextSurface, TextSurface.get_rect()

def message_display(text):
    LargeText = pygame.font.Font('freesansbold.ttf',15)
    TextSurf, TextRect = text_objects(text, LargeText)
    TextRect.center = (150,355)
    screen.blit(TextSurf, TextRect)
    pygame.display.update()
    
def main():
    pygame.init()
    #setting window
    width,height=288,512
    screen=pygame.display.set_mode((width,height))
    pygame.display.set_caption('Flappy Bird')
    clock=pygame.time.Clock()
    fps=80 #number of frames per second
    
    #sound effects
    fly=pygame.mixer.Sound('./sound-effects/fly.wav')
    die=pygame.mixer.Sound('./sound-effects/die.wav')
    point=pygame.mixer.Sound('./sound-effects/newPoint.wav')
    crash=pygame.mixer.Sound('./sound-effects/crash.wav')   
    
    #variables used:
    global counter
    global Gravity
    BirdXaxis=144 #location of bird on x-axis
    BirdYaxis=256 #location of bird on y-axis
    Birdspeed=0 #the velocity of the bird
    ground=425
    xlocation=576 #location of pipes on x-axis
    PipeHeight=randint(50,300) #This generates a random number within this range and uses it a the upper pipe's height
    space=120 # gap between upper and lower pipes
    PipeSpeed=2.5 # how much the pipes shift to the left
    beige=(255,240,180)	
    black=(0,0,0)
    salmon=(255,99,71)	
    #main loop
    crashed=False
    running=True 
    SoundPlayed=False
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN :
                if event.key==pygame.K_UP and BirdYaxis<425 and BirdYaxis>0 and crashed==False: 
                #if the up key is pressed, the bird will accelerate and the flap sound will play
                    fly.play()                
                    Birdspeed=-4  
                if event.key==pygame.K_a and crashed==True:
                    counter=0
                    Gravity=False
                    main()
                    running=False                    
            if event.type==pygame.KEYUP and BirdYaxis<425 and Gravity==True:
                #if no key is pressed, then gravity pulls you down
                Birdspeed=3       
        BirdYaxis+=Birdspeed #the location of the bird changes depending on the acceleration/deceleration 
        xlocation-=PipeSpeed #the location of the pipes is shifted to the left 
        screen.blit(background, (0, 0)) #the background image is displayed
        obstacle(xlocation,PipeHeight) #the pipes are generated
        screen.blit(base,(0,450)) #the base image is displayed
        screen.blit(bird,(BirdXaxis,BirdYaxis)) #the bird's image is displayed
        ScoreImage(counter,144,10)
    
        if xlocation<-55:
            #if the pipes go off the screen, then a new set of pipes is generated
            xlocation=288
            PipeHeight=randint(50,300)
        if BirdYaxis < 0:
            #this stops the bird from flying off the screen
            Birdspeed=0         
        if BirdXaxis+32> xlocation and (BirdYaxis <= PipeHeight or BirdYaxis+25 > PipeHeight+space) and BirdXaxis < 55+xlocation:
            #this condition determines collision, so if the bird collides with either pipes, then the game is over
            #sound effects imitating the collision are also played
            crashed=True
            if SoundPlayed==False:
                crash.play()
                die.play()
            SoundPlayed=True
            PipeSpeed=0
        
        if BirdXaxis > xlocation and BirdXaxis < xlocation+57 and BirdXaxis > xlocation+55:
            #if the bird passes through the gap successfully, then a point is added to the score
            counter=counter+1
            point.play()
        if BirdYaxis > ground:
            #if the bird hits the ground, the game then ends and sound effects imitating the collision are played as well
            gameover()
            crashed=True
            if SoundPlayed==False:
                crash.play() 
            SoundPlayed=True        
            Birdspeed=0
            PipeSpeed=0
        Gravity=True
        clock.tick(fps)
        pygame.display.update() 
main()
pygame.quit()
