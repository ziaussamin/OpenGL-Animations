from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

WINDOW_WIDTH  = 500
WINDOW_HEIGHT = 500

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




class AABB:
    x = 0
    y = 0
    w = 0
    h = 0

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
    
    def collides_with(self, other):
        return (self.x < other.x + other.w and # x_min_1 < x_max_2
                self.x + self.w > other.x  and # x_max_1 > m_min_2
                self.y < other.y + other.h and # y_min_1 < y_max_2
                self.y + self.h > other.y)     # y_max_1 > y_min_2

# Global variables
box1 = AABB(200, 25, 100, 20)
box2 = AABB(250, 500, 20, 20)
box_speed = 5
collision = False

def draw_box(box):
    global collision
    is_colliding = collision
    
    color = None
    if is_colliding:
        color = (1.0, 0.0, 0.0)
    else:
        color = (0.0, 1.0, 0.0)

    glBegin(GL_POINTS)
    # glVertex2f(box.x, box.y)
    # glVertex2f(box.x + box.w, box.y)

    draw_line_8way(color,box.x, box.y, box.x + box.w, box.y)

    # glVertex2f(box.x + box.w, box.y)
    # glVertex2f(box.x + box.w, box.y + box.h)

    draw_line_8way(color,box.x + box.w, box.y,box.x + box.w, box.y + box.h)    



    # glVertex2f(box.x + box.w, box.y + box.h)
    # glVertex2f(box.x, box.y + box.h)


    draw_line_8way(color,box.x + box.w, box.y + box.h,box.x, box.y + box.h)    

    # glVertex2f(box.x, box.y + box.h)
    # glVertex2f(box.x, box.y)

    draw_line_8way(color,box.x, box.y + box.h, box.x, box.y)    

    glEnd()

def initialize():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, WINDOW_WIDTH, 0.0, WINDOW_HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def check_collision():
    global box1, box2, collision

    if box1.collides_with(box2):
        collision = True
    else:
        collision = False

def show_screen():
    # this function should contain the logic for drawing objects
    # DO NOT do game logic here (e.g. object movement, collision detection, sink detection etc.)

    # clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # draw stuffs here
    draw_box(box1)
    draw_box(box2)

    # do not forget to call glutSwapBuffers() at the end of the function
    glutSwapBuffers()

def keyboard_ordinary_keys(key, _, __):
    # check against alphanumeric keys here (e.g. A..Z, 0..9, spacebar, punctuations)
    # must cast characters to binary when comparing (e.g. key == b'q')

    glutPostRedisplay()

def keyboard_special_keys(key, _, __):
    # check against special keys here (e.g. F1..F11, arrow keys, etc.)
    # use GLUT_KEY_* constants while comparing (e.g. GLUT_KEY_F1, GLUT_KEY_LEFT, etc.)
    global box1

    # if key == GLUT_KEY_UP:
    #     box1.y += box_speed
    # elif key == GLUT_KEY_DOWN:
    #     box1.y -= box_speed
    if key == GLUT_KEY_LEFT:
        box1.x -= box_speed
    elif key == GLUT_KEY_RIGHT:
        box1.x += box_speed

    glutPostRedisplay()

def mouse_click(button, state, x, y):
    # check for mouse clicks here (left, middle and right click)
    # use GLUT_LEFT_BUTTON, GLUT_MIDDLE_BUTTON, GLUT_RIGHT_BUTTON constants while comparing
    # use GLUT_DOWN and GLUT_UP constants while comparing for button state
    # You should either listen to GLUT_DOWN or GLUT_UP, so filter that out

    # convert coordinates, (flip the y-axis first)
    mx, my = x, WINDOW_HEIGHT - y

    # do your click detection here using button, state, mx, my


    glutPostRedisplay()

def animation():
    # write codes here that's going to run every frame
    # for example, updating coordinates of objects that move spotaneously
    # or collision detection, or sink detection, etc.
    # Note: DO NOT write drawing codes here

    check_collision()

    global box2
    box2.y -= 0.1


    # don't forget to call glutPostRedisplay()
    # otherwise your animation will be stuck
    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL AABB Collision")

glutDisplayFunc(show_screen)
glutIdleFunc(animation)

glutKeyboardFunc(keyboard_ordinary_keys)
glutSpecialFunc(keyboard_special_keys)
glutMouseFunc(mouse_click)

glEnable(GL_DEPTH_TEST)
initialize()
glutMainLoop()