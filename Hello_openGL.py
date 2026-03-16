from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def draw_points(x, y):
    glPointSize(5)      #pixel size. by default 1 thake
                        #glColor3f(1.0, 1.0, 0)   if want to change color, color code needs to be put first
    glBegin(GL_POINTS)  #here, we specify whether a point, line or triangle
    glVertex2f(x,y)     #jekhane show korbe pixel
    glEnd()


def draw_anything():   
    glLineWidth(5)      #Determines line thickness  
    glBegin(GL_LINES)  
    glVertex2f(100,100)
    glVertex2f(400,200)     
    glEnd()


def draw_triangle():
    glBegin(GL_TRIANGLES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(100,100)

    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(300,100)

    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(250,250)
    glEnd()
 



def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 0.0) #konokichur color set (RGB)
    #call the draw methods here
    draw_points(250, 250)
    draw_anything()
    draw_triangle()
    glutSwapBuffers()



glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500) #window size       setting display size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
glutDisplayFunc(showScreen)

glutMainLoop()