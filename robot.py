import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

def gambar_kubus():
    vertices = [
        # Depan
        -0.5, -0.5,  0.5,
         0.5, -0.5,  0.5,
         0.5,  0.5,  0.5,
        -0.5,  0.5,  0.5,
        # Belakang
        -0.5, -0.5, -0.5,
         0.5, -0.5, -0.5,
         0.5,  0.5, -0.5,
        -0.5,  0.5, -0.5,
    ]
    
    edges = [
        0, 1, 2, 3,  # Depan
        4, 5, 6, 7,  # Belakang
        0, 4, 7, 3,  # Kiri
        1, 5, 6, 2,  # Kanan
        3, 2, 6, 7,  # Atas
        0, 1, 5, 4   # Bawah
    ]
    
    glBegin(GL_QUADS)
    for i in range(0, len(edges), 4):
        for j in range(4):
            idx = edges[i + j]
            glVertex3f(vertices[idx*3], vertices[idx*3+1], vertices[idx*3+2])
    glEnd()

def gambar_silinder(radius_bawah, radius_atas, tinggi, slice, stack):
    q = gluNewQuadric()
    gluCylinder(q, radius_bawah, radius_atas, tinggi, slice, stack)

def gambar_bola(radius, slice, stack):
    q = gluNewQuadric()
    gluSphere(q, radius, slice, stack)

def gambar_robot():
    # Kepala (Kubus)
    glColor3f(0.7, 0.7, 0.7)
    glPushMatrix()
    glTranslatef(0.0, 1.0, 0.0)
    glScalef(0.8, 0.8, 0.8)
    gambar_kubus()
    
    # Mata kiri (Bola)
    glColor3f(0.0, 0.0, 1.0)
    glPushMatrix()
    glTranslatef(-0.25, 0.1, 0.5)
    gambar_bola(0.15, 10, 10)
    glPopMatrix()
    
    # Mata kanan (Bola)
    glPushMatrix()
    glTranslatef(0.25, 0.1, 0.5)
    gambar_bola(0.15, 10, 10)
    glPopMatrix()
    glPopMatrix()

    # Badan (Kubus)
    glColor3f(0.7, 0.7, 0.7)
    glPushMatrix()
    glTranslatef(0.0, -0.2, 0.0)
    glScalef(1.2, 1.6, 0.8)
    gambar_kubus()
    glPopMatrix()

    # Tangan kiri (Silinder)
    glColor3f(0.6, 0.6, 0.6)
    glPushMatrix()
    glTranslatef(-1.2, 0.2, 0.0)
    glRotatef(90, 0.0, 1.0, 0.0)
    gambar_silinder(0.1, 0.1, 0.8, 8, 2)
    glPopMatrix()

    # Tangan kanan (Silinder)
    glPushMatrix()
    glTranslatef(1.2, 0.2, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)
    gambar_silinder(0.1, 0.1, 0.8, 8, 2)
    glPopMatrix()

    # Kaki kiri (Silinder)
    glColor3f(0.6, 0.6, 0.6)
    glPushMatrix()
    glTranslatef(-0.4, -1.5, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gambar_silinder(0.12, 0.12, 0.8, 8, 2)
    glPopMatrix()

    # Kaki kanan (Silinder)
    glPushMatrix()
    glTranslatef(0.4, -1.5, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gambar_silinder(0.12, 0.12, 0.8, 8, 2)
    glPopMatrix()
    
    # Antena (Silinder dan Bola)
    glColor3f(0.5, 0.5, 0.5)  # Warna abu-abu untuk antena
    
    # Batang antena kiri
    glPushMatrix()
    glTranslatef(-0.3, 1.2, 0.0)  # Y diubah dari 1.0 ke 1.2
    glRotatef(-90, 1.0, 0.0, 0.0)
    gambar_silinder(0.03, 0.03, 0.4, 8, 2)
    glPopMatrix()

    # Ujung antena kiri
    glColor3f(1.0, 0.0, 0.0)  # Warna merah untuk ujung antena
    glPushMatrix() 
    glTranslatef(-0.3, 1.6, 0.0)  # Y diubah dari 1.4 ke 1.6
    gambar_bola(0.06, 10, 10)
    glPopMatrix()

    # Batang antena kanan
    glColor3f(0.5, 0.5, 0.5)
    glPushMatrix()
    glTranslatef(0.3, 1.2, 0.0)  # Y diubah dari 1.0 ke 1.2
    glRotatef(-90, 1.0, 0.0, 0.0)
    gambar_silinder(0.03, 0.03, 0.4, 8, 2)
    glPopMatrix()

    # Ujung antena kanan
    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0.3, 1.6, 0.0)  # Y diubah dari 1.4 ke 1.6
    gambar_bola(0.06, 10, 10)
    glPopMatrix()

def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Robot Sederhana", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    
    # Variabel untuk rotasi dan wireframe
    rotation_y = 0.0
    rotation_x = 0.0
    is_wireframe = False  # Status mode wireframe
    
    # Callback untuk keyboard
    def key_callback(window, key, scancode, action, mods):
        nonlocal rotation_y, rotation_x, is_wireframe
        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_LEFT:
                rotation_y -= 5
            elif key == glfw.KEY_RIGHT:
                rotation_y += 5
            elif key == glfw.KEY_UP:
                rotation_x -= 5
            elif key == glfw.KEY_DOWN:
                rotation_x += 5
            # Tambah toggle wireframe dengan tombol W
            elif key == glfw.KEY_W and action == glfw.PRESS:
                is_wireframe = not is_wireframe
                if is_wireframe:
                    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)  # Mode wireframe
                else:
                    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)  # Mode solid

    glfw.set_key_callback(window, key_callback)
    
    # Callback untuk resize window
    def window_resize(window, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width/height, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    glfw.set_window_size_callback(window, window_resize)
    
    # Inisialisasi
    init()
    
    # Set proyeksi awal
    window_resize(window, 800, 600)

    # Posisi dan arah cahaya
    glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
    
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Atur posisi kamera
        gluLookAt(0.0, 0.0, 5.0,  # Posisi kamera
                  0.0, 0.0, 0.0,  # Titik yang dilihat
                  0.0, 1.0, 0.0)  # Arah atas kamera
        
        # Terapkan rotasi
        glRotatef(rotation_x, 1.0, 0.0, 0.0)  # Rotasi pada sumbu X
        glRotatef(rotation_y, 0.0, 1.0, 0.0)  # Rotasi pada sumbu Y
        
        gambar_robot()
        
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main() 