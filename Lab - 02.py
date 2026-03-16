from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

Width= 500
Height= 500


def findzone(x1, y1, x2, y2):
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
        



def convertToZone0(zone, x1, y1):
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




def originalZone(zone, x, y):

    if zone == 0:
        return x, y

    if zone == 1:
        return y, x

    if zone == 2:
        return -y, x
    
    if zone == 3:
        return -x, y
    
    if zone == 4:
        return -x, -y
    
    if zone == 5:
        return -y, -x
    
    if zone == 6:
        return y, -x
    
    if zone == 7:
        return x, -y
    



def draw_line_raw(color, zone, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    d =   2 * dy - dx
    dNE = 2 * (dy - dx)
    dE =  2 * dy

    x, y = x1, y1

    while x <= x2:
        cx, cy = originalZone(zone, x, y)
        glColor3f(color[0], color[1], color[2])
        glVertex2f(cx, cy)
        x += 1
        if d > 0:
            y += 1
            d = d + dNE
        else:
            d = d + dE




def draw_line_8way(color, x1, y1, x2, y2):
    zone = findzone(x1, y1, x2, y2)
    x1, y1 = convertToZone0(zone, x1, y1)
    x2, y2 = convertToZone0(zone, x2, y2)
    draw_line_raw(color, zone, x1, y1, x2, y2)


def specialKeyListener(key, x, y):
    global gb1,gb2,gb3,gb4
    speedCount=20
    if key== GLUT_KEY_RIGHT:
        if gb1[2]>=500:
            pass
        else:
            if pause==False:
                gb1[0]+=speedCount
                gb1[2]+=speedCount
                gb2[0]+=speedCount
                gb2[2]+=speedCount
                gb3[0]+=speedCount
                gb3[2]+=speedCount
                gb4[0]+=speedCount
                gb4[2]+=speedCount
    if key==GLUT_KEY_LEFT:
        if gb1[0]<=0:
            pass
        else:
            if pause==False:
                gb1[0]-=speedCount
                gb1[2]-=speedCount
                gb2[0]-=speedCount
                gb2[2]-=speedCount
                gb3[0]-=speedCount
                gb3[2]-=speedCount
                gb4[0]-=speedCount
                gb4[2]-=speedCount
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global yUpperPoint,gameInfo,pause,bColor
    if button==GLUT_LEFT_BUTTON:
        if(state==GLUT_DOWN):
            #exit
            if x>=450 and x<=500 and y>=450 and y<=500:
                glutLeaveMainLoop()
            #pause
            elif x>=220 and x<=275 and y>=450 and y<=500:
                if pause==False:
                    pause=True
                else:
                    pause=False
            #restart
            elif x>=0 and x<=50 and y>=450 and y<=500:
                yUpperPoint=450
                print('Starting Over!')
                gameInfo=0
                pause=False
                bColor=[1,1,1]
    glutPostRedisplay()


speed=1
gameInfo=0
def iterate():

    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


    global xLeftPoint,yUpperPoint,gb1,gameInfo,pause,barColor,ranColor
    if yUpperPoint==30:
        if gb1[0]<xLeftPoint+70 and gb1[2]>xLeftPoint:
            initY=210
            xLeftPoint=random.randint(0,450)
            gameInfo+=1
            ranColor=[random.random(),random.random(),random.random()]
            print(f'Score: {gameInfo}')   
        else:
            barColor=[1,0,0]
            print(f'Game Over! Score: {gameInfo}')
    if pause==True:
        yUpperPoint=yUpperPoint
    else:
        yUpperPoint=(yUpperPoint-speed)
    
    print(yUpperPoint)

    glutPostRedisplay()





xLeftPoint=250
yUpperPoint=450
gb1=[210,20,280,20]
gb2=[225,1,265,1]
gb3=[225,1,210,20]
gb4=[265,1,280,20]
pause=False
barColor=[1,1,1]
R3color=random.random()
ranColor=[R3color,R3color,R3color]

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    glBegin(GL_POINTS)



    global gb1,gb2,gb3,gb4,barColor,ranColor
    draw_line_8way(barColor,gb1[0],gb1[1],gb1[2],gb1[3])  #Bar
    draw_line_8way(barColor,gb2[0],gb2[1],gb2[2],gb2[3])
    draw_line_8way(barColor,gb3[0],gb3[1],gb3[2],gb3[3])
    draw_line_8way(barColor,gb4[0],gb4[1],gb4[2],gb4[3])

    draw_line_8way([1, 1, 0], 10, 10, 200, 400)
    

    color=[1,0,0]   #Exit button creation
    draw_line_8way(color,450,450,500,500)
    draw_line_8way(color,450,500,500,450)


    color=[1,1,0]   #Pause button creation
    if pause==False:
        draw_line_8way(color, 240,450,240,500)
        draw_line_8way(color, 260,450,260,500)
    else:
        draw_line_8way(color,220,450,220,500)
        draw_line_8way(color,220,450,275,475)
        draw_line_8way(color,220,500,275,475)


    color=[0,0,1]   #Restart mechanism
    draw_line_8way(color,0,475,50,475)
    draw_line_8way(color,0,475,25,450)
    draw_line_8way(color,0,475,25,500)


    color=[0,0,0]  #Diamond structure drawing
    diamondWidth=20
    diamondHeight=30
    global xLeftPoint,yUpperPoint

    p1=[int((xLeftPoint+(diamondWidth/2))),yUpperPoint]       
    p2=[xLeftPoint+diamondWidth,int((yUpperPoint-(diamondHeight)/2))]
    p3=[p1[0],yUpperPoint-diamondHeight]
    p4=[xLeftPoint,p2[1]]

    draw_line_8way(ranColor,p1[0],p1[1],p2[0],p2[1])
    draw_line_8way(ranColor,p2[0],p2[1],p3[0],p3[1])
    draw_line_8way(ranColor,p3[0],p3[1],p4[0],p4[1])
    draw_line_8way(ranColor,p4[0],p4[1],p1[0],p1[1])


    
    
    glEnd()
    #iterate()
    glutSwapBuffers()


def initialize():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, Width, 0.0, Height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
glutDisplayFunc(showScreen)
glutIdleFunc(iterate)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
initialize()
glutMainLoop()