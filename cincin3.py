import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np

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

def gambar_cincin():
    radius_luar = 1.0
    radius_dalam = 0.9
    ketebalan = 0.1
    tinggi = 0.3
    segmen = 60
    
    if is_wireframe:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    # Warna emas untuk cincin
    glColor3f(1.0, 0.84, 0.0)
    
    # Gambar permukaan luar cincin
    glBegin(GL_QUAD_STRIP)
    for i in range(segmen + 1):
        sudut = 2.0 * math.pi * i / segmen
        cos_sudut = math.cos(sudut)
        sin_sudut = math.sin(sudut)
        
        # Titik pada lingkaran luar
        glNormal3f(cos_sudut, sin_sudut, 0.0)
        glVertex3f(radius_luar * cos_sudut, radius_luar * sin_sudut, tinggi/2)
        glVertex3f(radius_luar * cos_sudut, radius_luar * sin_sudut, -tinggi/2)
    glEnd()
    
    # Gambar permukaan dalam cincin
    glBegin(GL_QUAD_STRIP)
    for i in range(segmen + 1):
        sudut = 2.0 * math.pi * i / segmen
        cos_sudut = math.cos(sudut)
        sin_sudut = math.sin(sudut)
        
        # Titik pada lingkaran dalam
        glNormal3f(-cos_sudut, -sin_sudut, 0.0)
        glVertex3f(radius_dalam * cos_sudut, radius_dalam * sin_sudut, tinggi/2)
        glVertex3f(radius_dalam * cos_sudut, radius_dalam * sin_sudut, -tinggi/2)
    glEnd()
    
    # Gambar permukaan atas dan bawah
    for z in [tinggi/2, -tinggi/2]:
        glBegin(GL_QUAD_STRIP)
        for i in range(segmen + 1):
            sudut = 2.0 * math.pi * i / segmen
            cos_sudut = math.cos(sudut)
            sin_sudut = math.sin(sudut)
            
            if z > 0:
                glNormal3f(0.0, 0.0, 1.0)
            else:
                glNormal3f(0.0, 0.0, -1.0)
                
            glVertex3f(radius_dalam * cos_sudut, radius_dalam * sin_sudut, z)
            glVertex3f(radius_luar * cos_sudut, radius_luar * sin_sudut, z)
        glEnd()

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(800, 800, "Cincin 3D", None, None)
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    glfw.set_key_callback(window, kontrol_keyboard)
    
    # Pengaturan 3D dan pencahayaan
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    # Atur posisi dan warna lampu
    glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    
    # Atur material untuk efek mengkilap
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 128.0)
    
    # Atur perspektif
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        glTranslatef(0.0, 0.0, -5.0)
        glRotatef(putaran_x, 1.0, 0.0, 0.0)
        glRotatef(putaran_y, 0.0, 1.0, 0.0)
        
        gambar_cincin()
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main()