import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Variabel untuk rotasi
putaran_x = 0.0
putaran_y = 0.0
kecepatan_putar = 5
is_wireframe = True  # Mulai dengan mode wireframe

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

def gambar_kubus(x, y, z, panjang, lebar, tinggi):
    # Fungsi untuk menggambar kubus dengan posisi dan ukuran tertentu
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(panjang, lebar, tinggi)
    glBegin(GL_QUADS)
    
    # Definisikan setiap sisi kubus
    # Sisi depan
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    
    # Sisi belakang
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    
    # Sisi kiri
    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    
    # Sisi kanan
    glNormal3f(1.0, 0.0, 0.0)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, -0.5)
    
    # Sisi atas
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    
    # Sisi bawah
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    
    glEnd()
    glPopMatrix()

def gambar_kursi():
    # Gambar dudukan kursi
    gambar_kubus(0.0, 0.0, 0.0, 1.0, 0.1, 1.0)
    
    # Gambar kaki-kaki kursi
    gambar_kubus(-0.45, -0.55, -0.45, 0.1, 1.0, 0.1)
    gambar_kubus(0.45, -0.55, -0.45, 0.1, 1.0, 0.1)
    gambar_kubus(-0.45, -0.55, 0.45, 0.1, 1.0, 0.1)
    gambar_kubus(0.45, -0.55, 0.45, 0.1, 1.0, 0.1)
    
    # Gambar sandaran kursi
    gambar_kubus(0.0, 0.5, -0.45, 1.0, 1.0, 0.1)

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(800, 600, "Kursi 3D", None, None)
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    glfw.set_key_callback(window, kontrol_keyboard)
    
    # Pengaturan 3D
    glEnable(GL_DEPTH_TEST)
    
    # Atur perspektif
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800.0/600.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    
    # Atur pencahayaan
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    # Atur posisi dan warna lampu
    glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])  # Cahaya ambient
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])  # Cahaya diffuse
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])  # Cahaya specular
    
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Posisikan kursi
        glTranslatef(0.0, 0.0, -5.0)
        glRotatef(putaran_x, 1.0, 0.0, 0.0)
        glRotatef(putaran_y, 0.0, 1.0, 0.0)
        
        # Tentukan mode wireframe atau solid
        if is_wireframe:
            glDisable(GL_LIGHTING)  # Nonaktifkan pencahayaan untuk wireframe
            glColor3f(1.0, 1.0, 1.0)  # Warna putih untuk wireframe
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glEnable(GL_LIGHTING)  # Aktifkan pencahayaan untuk mode solid
            glColor3f(0.6, 0.3, 0.0)  # Warna coklat untuk mode solid
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        gambar_kursi()
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main() 