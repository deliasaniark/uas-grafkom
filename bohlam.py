import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Variabel untuk rotasi
putaran_x = 0.0
putaran_y = 0.0
kecepatan_putar = 5
is_wireframe = False

def kontrol_keyboard(window, key, scancode, action, mods):
    global putaran_x, putaran_y, is_wireframe
    
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_UP:
            putaran_x += kecepatan_putar
        if key == glfw.KEY_DOWN:
            putaran_x -= kecepatan_putar
        if key == glfw.KEY_LEFT:
            putaran_y -= kecepatan_putar
        if key == glfw.KEY_RIGHT:
            putaran_y += kecepatan_putar
        if key == glfw.KEY_SPACE:
            is_wireframe = not is_wireframe

def gambar_bohlam():
    if is_wireframe:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Bagian kaca bohlam (bentuk tetesan)
    glPushMatrix()
    glColor4f(0.95, 0.95, 0.95, 0.3)  # Warna putih transparan
    
    # Bagian bulat atas
    quadric = gluNewQuadric()
    gluSphere(quadric, 0.4, 32, 32)
    gluDeleteQuadric(quadric)
    
    # Bagian leher yang menyempit
    glPushMatrix()
    glTranslatef(0.0, -0.3, 0.0)
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.4, 0.2, 0.3, 32, 8)
    gluDeleteQuadric(quadric)
    glPopMatrix()
    glPopMatrix()

    # Bagian logam (fitting)
    glPushMatrix()
    glTranslatef(0.0, -0.6, 0.0)
    glColor3f(0.8, 0.8, 0.8)  # Warna abu-abu metalik
    
    # Bagian atas fitting
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.2, 0.25, 0.1, 32, 4)
    gluDeleteQuadric(quadric)
    
    # Bagian tengah fitting
    glTranslatef(0.0, 0.0, 0.1)
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.25, 0.25, 0.2, 32, 4)
    gluDeleteQuadric(quadric)
    
    # Bagian bawah fitting
    glTranslatef(0.0, 0.0, 0.2)
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.25, 0.22, 0.1, 32, 4)
    gluDeleteQuadric(quadric)
    glPopMatrix()

    # Bagian dalam bohlam (filamen)
    glPushMatrix()
    glTranslatef(0.0, -0.1, 0.0)
    glColor3f(0.7, 0.7, 0.7)  # Warna filamen
    glLineWidth(2.0)
    
    # Gambar filamen
    glBegin(GL_LINE_STRIP)
    for i in range(65):
        theta = i * 2.0 * math.pi / 16.0
        y = -0.1 + 0.05 * math.sin(theta * 2)
        r = 0.1
        x = r * math.cos(theta)
        z = r * math.sin(theta)
        glVertex3f(x, y, z)
    glEnd()
    glPopMatrix()

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(800, 800, "Bohlam 3D", None, None)
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    glfw.set_key_callback(window, kontrol_keyboard)
    
    # Pengaturan 3D dan pencahayaan
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    # Atur posisi dan warna lampu
    glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    
    # Material properties untuk efek kaca
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 100.0)
    
    # Atur perspektif
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        glTranslatef(0.0, 0.0, -3.0)
        glRotatef(putaran_x, 1.0, 0.0, 0.0)
        glRotatef(putaran_y, 0.0, 1.0, 0.0)
        
        gambar_bohlam()
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main()