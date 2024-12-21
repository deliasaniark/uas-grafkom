import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Variabel untuk rotasi dan mode wireframe
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

def gambar_bola(radius, slices, stacks):
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, slices, stacks)
    gluDeleteQuadric(quadric)
    
def gambar_silinder(radius_base, radius_top, height, slices, stacks):
    quadric = gluNewQuadric()
    gluCylinder(quadric, radius_base, radius_top, height, slices, stacks)
    gluDeleteQuadric(quadric)

def gambar_manusia_salju():
    # Tentukan mode wireframe atau solid
    if is_wireframe:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Kepala
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(0.0, 0.95, 0.0)
    gambar_bola(0.25, 20, 20)
    glPopMatrix()
    
    # Tubuh tengah
    glPushMatrix()
    glTranslatef(0.0, 0.25, 0.0)
    gambar_bola(0.5, 20, 20)
    glPopMatrix()
    
    # Tubuh bawah
    glPushMatrix()
    glTranslatef(0.0, -0.75, 0.0)
    gambar_bola(0.75, 32, 32)
    glPopMatrix()
    
    # Mata kiri
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(-0.1, 1.05, 0.18)
    gambar_bola(0.05, 10, 10)
    glPopMatrix()
    
    # Mata kanan
    glPushMatrix()
    glTranslatef(0.1, 1.05, 0.18)
    gambar_bola(0.05, 10, 10)
    glPopMatrix()
    
    # Hidung
    glColor3f(1.0, 0.5, 0.0)
    glPushMatrix()
    glTranslatef(0.0, 0.95, 0.25)
    glRotatef(-360, 1.0, 0.0, 0.0)
    gambar_silinder(0.05, 0.0, 0.2, 10, 2)
    glPopMatrix()
    
    # mulut
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(-0.15, 0.85, 0.25)
    gambar_bola(0.02, 10, 10)
    glPopMatrix()
    
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(-0.05, 0.8, 0.25)
    gambar_bola(0.02, 10, 10)
    glPopMatrix()
    
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0.05, 0.8, 0.25)
    gambar_bola(0.02, 10, 10)
    glPopMatrix()

    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0.15, 0.85, 0.25)
    gambar_bola(0.02, 10, 10)
    glPopMatrix()
    
    # tangan
    # Tangan kiri
    glColor3f(0.6, 0.3, 0.1)
    glPushMatrix()
    glTranslatef(0.4, 0.3, 0.0)
    glRotatef(90, -0.80, 1.0, 0.0)
    gambar_silinder(0.05, 0.03, 0.8, 8, 2)
    glPopMatrix()

    # Tangan kanan  
    glPushMatrix()
    glTranslatef(-0.4, 0.3, 0.0)
    glRotatef(-90, 0.80, 1.0, 0.0)
    gambar_silinder(0.05, 0.03, 0.8, 8, 2)
    glPopMatrix()

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(800, 800, "Manusia Salju 3D dengan Hidung Benar", None, None)
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
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])  # Cahaya ambient
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])  # Cahaya diffuse
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])  # Cahaya specular
    
    # Atur perspektif
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0, 0.1, 100.0)  # Menggunakan aspek rasio 1.0 untuk menjaga proporsi
    glMatrixMode(GL_MODELVIEW)
    
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Posisikan manusia salju
        glTranslatef(0.0, 0.0, -5.0)  # Pindahkan manusia salju ke posisi yang sesuai
        glRotatef(putaran_x, 1.0, 0.0, 0.0)
        glRotatef(putaran_y, 0.0, 1.0, 0.0)
        
        gambar_manusia_salju()
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main() 