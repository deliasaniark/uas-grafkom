import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Variabel untuk rotasi dan animasi
putaran_x = 0.0
putaran_y = 0.0
kecepatan_putar = 5
is_wireframe = False
sudut_buka = 0.0  # Sudut untuk membuka/menutup buku
kecepatan_buka = 2.0  # Kecepatan membuka/menutup
is_opening = False  # Status animasi membuka
is_closing = False  # Status animasi menutup

def kontrol_keyboard(window, key, scancode, action, mods):
    global putaran_x, putaran_y, is_wireframe, is_opening, is_closing
    
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
        if key == glfw.KEY_O:  # Tombol O untuk membuka
            is_opening = True
            is_closing = False
        if key == glfw.KEY_C:  # Tombol C untuk menutup
            is_closing = True
            is_opening = False

def update_animasi():
    global sudut_buka, is_opening, is_closing
    
    if is_opening and sudut_buka < 180:
        sudut_buka += kecepatan_buka
        if sudut_buka >= 180:
            is_opening = False
    elif is_closing and sudut_buka > 0:
        sudut_buka -= kecepatan_buka
        if sudut_buka <= 0:
            is_closing = False

def gambar_kubus(x, y, z):
    if is_wireframe:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glBegin(GL_QUADS)
    
    # Atas
    glVertex3f(-x, y, -z)
    glVertex3f(x, y, -z)
    glVertex3f(x, y, z)
    glVertex3f(-x, y, z)
    
    # Bawah
    glVertex3f(-x, -y, -z)
    glVertex3f(x, -y, -z)
    glVertex3f(x, -y, z)
    glVertex3f(-x, -y, z)
    
    # Depan
    glVertex3f(-x, -y, z)
    glVertex3f(x, -y, z)
    glVertex3f(x, y, z)
    glVertex3f(-x, y, z)
    
    # Belakang
    glVertex3f(-x, -y, -z)
    glVertex3f(x, -y, -z)
    glVertex3f(x, y, -z)
    glVertex3f(-x, y, -z)
    
    # Kiri
    glVertex3f(-x, -y, -z)
    glVertex3f(-x, -y, z)
    glVertex3f(-x, y, z)
    glVertex3f(-x, y, -z)
    
    # Kanan
    glVertex3f(x, -y, -z)
    glVertex3f(x, -y, z)
    glVertex3f(x, y, z)
    glVertex3f(x, y, -z)
    
    glEnd()

def gambar_buku():
    # Cover belakang
    glColor3f(0.8, 0.1, 0.1)  # Merah tua
    glPushMatrix()
    glTranslatef(0.0, 0.0, -0.12)
    glScalef(1.0, 1.5, 0.1)
    gambar_kubus(0.5, 0.5, 0.5)
    glPopMatrix()
    
    # Halaman-halaman
    glPushMatrix()
    glTranslatef(0.5, 0.0, 0.0)  # Pindahkan ke sisi kanan untuk rotasi
    glRotatef(sudut_buka, 0.0, 1.0, 0.0)  # Rotasi untuk membuka/menutup
    glTranslatef(-0.5, 0.0, 0.0)  # Kembalikan ke posisi semula
    
    # Cover depan
    glColor3f(0.8, 0.1, 0.1)
    glPushMatrix()
    glScalef(1.0, 1.5, 0.1)
    gambar_kubus(0.5, 0.5, 0.5)
    glPopMatrix()
    
    # Halaman-halaman buku
    glColor3f(1.0, 1.0, 1.0)
    for i in range(5):
        glPushMatrix()
        glTranslatef(0.0, 0.0, -(i * 0.02))
        glScalef(0.95, 1.45, 0.01)
        gambar_kubus(0.5, 0.5, 0.5)
        glPopMatrix()
    
    glPopMatrix()
    
    # Punggung buku
    glColor3f(0.6, 0.1, 0.1)
    glPushMatrix()
    glTranslatef(-0.52, 0.0, -0.06)
    glScalef(0.05, 1.5, 0.12)
    gambar_kubus(0.5, 0.5, 0.5)
    glPopMatrix()

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(800, 800, "Buku 3D Animasi", None, None)
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
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    
    # Atur perspektif
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        update_animasi()  # Update animasi buka/tutup
        
        glTranslatef(0.0, 0.0, -5.0)
        glRotatef(putaran_x, 1.0, 0.0, 0.0)
        glRotatef(putaran_y, 0.0, 1.0, 0.0)
        
        gambar_buku()
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main() 