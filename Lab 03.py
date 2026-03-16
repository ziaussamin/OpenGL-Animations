from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math,random


def draw_points(x, y, s):
    glPointSize(s)
    glBegin(GL_POINTS)
    glVertex2f(x,y)
    glEnd()

def MidPointLine(x1, y1, x2, y2):
    store=[]
    dx=x2-x1
    dy=y2-y1
    d=2*dy-dx
    pE=2*dy
    pNE=2*dy-2*dx
    x=x1
    y=y1
    for i in range(x,x2+1):
        store+=[[i,y]]
        if d>0:
            d+=pNE
            y+=1
        else:
            d+=pE
    return store

def findZone(x1, y1, x2, y2):
    dx=x2-x1
    dy=y2-y1
    if dx>0 and dy>=0:
        if abs(dx)>abs(dy):
            return 0
        else:
            return 1
    elif dx<=0 and dy>=0:
        if abs(dx)>abs(dy):
            return 3
        else:
            return 2
    elif dx<0 and dy<0:
        if abs(dx)>abs(dy):
            return 4
        else:
            return 5
    elif dx>=0 and dy<0:
        if abs(dx)>abs(dy):
            return 7
        else:
            return 6
        
def convertToZone0(zone, x1, y1, x2, y2):
    if zone == 0:
        x1,y1=x1,y1
        x2,y2=x2,y2       
    elif zone==1:
        x1,y1=y1,x1
        x2,y2=y2,x2
    elif zone==2:
        x1,y1=y1,-x1
        x2,y2=y2,-x2
    elif zone==3:
        x1,y1=-x1,y1
        x2,y2=-x2,y2
    elif zone==4:
        x1,y1=-x1,-y1
        x2,y2=-x2,-y2
    elif zone==5:
        x1,y1=-y1,-x1
        x2,y2=-y2,-x2
    elif zone==6:
        x1,y1=-y1,x1
        x2,y2=-y2,x2
    elif zone==7:
        x1,y1=x1,-y1
        x2,y2=x2,-y2
    return x1,y1,x2,y2

def convertToZoneM(color, zone, points):
    s=2
    glColor3f(color[0], color[1], color[2])
    if zone==0:
        for x,y in points:
            draw_points(x,y,s)
    elif zone==1:
        for x,y in points:
            draw_points(y,x,s)
    elif zone==2:
        for x,y in points:
            draw_points(-y,x,s)
    elif zone==3:
        for x,y in points:
            draw_points(-x,y,s)
    elif zone==4:
        for x,y in points:
            draw_points(-x,-y,s)
    elif zone==5:
        for x,y in points:
            draw_points(-y,-x,s)
    elif zone==6:
        for x,y in points:
            draw_points(y,-x,s)
    elif zone==7:
        for x,y in points:
            draw_points(x,-y,s)

def drawLines(color, x1, y1, x2, y2):
    zone=findZone(x1,y1,x2,y2)
    x1,y1,x2,y2=convertToZone0(zone,x1,y1,x2,y2)
    points=MidPointLine(x1,y1,x2,y2)
    convertToZoneM(color,zone,points)

def keyboardListener(key,x,y):
    global shooterX, finish
    if key==b' ':
        if finish==False:
            bullets.append([shooterX,shooterY])
    if key==b'a' and shooterX > sR+25:
        shooterX-= movement
        #print(sX)
    if key==b'd' and shooterX < width-25:
        shooterX+= movement
        #print(sX)

def mouseListener(button, state, x, y):
    global pause
    if button==GLUT_LEFT_BUTTON:
        if(state==GLUT_DOWN):

            if x>=460 and x<=480 and y>=5 and y<=30:          #Exit
                glutLeaveMainLoop()

            elif x>=240 and x<=260 and y>=10 and y<=35:       #Pause/Play
                if pause==False:
                    pause=True
                    print("Game paused")
                else:
                    pause=False
                    print("Game Continued")

            elif x>=10 and x<=40 and y>=10 and y<=30:         #Restart
                print('Starting Over!')
                restart_game()
    glutPostRedisplay()

def draw_circle(X,Y,r):
    x,y=0,r
    d=1-r
    numZone=8
    while x<y:
        for i in range(numZone):
            x0,y0= zoneConversion(x, y, i)
            draw_points(x0+X, y0+Y, 1)
        if d>0:
            d+=2*x-2*y+5
            x+=1
            y-=1
        else:
            d+=2*x+3
            x+=1

def zoneConversion(x1,y1,zone):
    if zone==1:
        x1,y1=y1,x1

    elif zone==2:
        x1,y1=y1,-x1

    elif zone==3:
        x1,y1=-x1,y1

    elif zone==4:
        x1,y1=-x1,-y1

    elif zone==5:
        x1,y1=-y1,-x1

    elif zone==6:
        x1,y1=-y1,x1

    elif zone==7:
        x1,y1=x1,-y1

    return x1,y1

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_bullets()
    draw_shooter()
    draw_circle_objects()

    if pause==False:
        glLoadIdentity()
        glOrtho(0,width,0,height,-1,1)
    
    if finish:
        print("Game Over!")

        print("Final Score:",score)

    color=[1,0,0]   #Exit button creation
    drawLines(color,460,490,480,470)
    drawLines(color,480,490,460,470)

    color=[1,1,0]  #Pause button creation
    if pause==False:
        drawLines(color,240,490,240,465)
        drawLines(color,260,490,260,465)
    else:
        drawLines(color,240,490,240,465)
        drawLines(color,240,490,260,478)
        drawLines(color,240,465,260,478)

    color=[0,0,1]   #Restart mechanism
    drawLines(color,10,480,40,480)
    drawLines(color,10,480,20,490)
    drawLines(color,10,480,20,470)

    glutSwapBuffers()

def update(value):
    global bullets,score,failure,finish
    if not pause:
        for circle in circles:
            circle[1]-= fall_length
            if circle[1]<=0:
                circles.remove(circle)
                failure+=1
                print(f"Missed points: {failure}")
                if failure>=3:
                    finish=True
            else:
                for bullet in bullets:
                    if check_collision(circle, bullet):
                        circles.remove(circle)
                        bullets.remove(bullet)
                        score+=1
                        print(f"Score: {score}")
                        break

        new_bullets=[]
        for bullet in bullets:
            bullet[1]+=bS
            if bullet[1]<height:
                new_bullets.append(bullet)
        bullets=new_bullets

        if random.randint(1,1000)<=cT:
            circles.append([random.randint(cR,width-cR),height-cR])
    glutTimerFunc(10,update,0)
    glutPostRedisplay()

def draw_bullet(x,y):
    glColor3f(0.5,1.5,0.5)
    draw_circle(x,y,bR)

def draw_shooter():
    glColor3f(0.0,1.0,1.0)
    draw_circle(shooterX,shooterY,sR)

def draw_circle_objects():
    glColor3f(1.0,0.0,1.0)
    for circle in circles:
        draw_circle(circle[0],circle[1],cR)

def draw_bullets():
    for bullet in bullets:
        draw_bullet(bullet[0],bullet[1])

def check_collision(circle,bullet):
    distance=((bullet[0]-circle[0])**2+(bullet[1]-circle[1])**2)**0.5
    return distance<=bR+cR

def restart_game():
    global score, failure, circles, bullets, finish
    score,failure=0,0
    finish=False
    circles=[]
    bullets=[]


width,height=500,500

sR=10
bR=5
bS=3
cR=15
cT=10

fall_length= 0.5

shooterX= 250
shooterY= 15
movement= 10


score,failure=0, 0
finish=False
pause=False
circles=[]
bullets=[]

glutInit()
glutInitWindowSize(width,height)
glutInitWindowPosition(0,0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Circle Shooter Game")
glutDisplayFunc(display)
glutTimerFunc(10,update,0)
glutKeyboardFunc(keyboardListener)
#glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()