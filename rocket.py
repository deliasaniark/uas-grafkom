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

def gambar_silinder(radius_base, radius_top, height, slices, stacks):
    quadric = gluNewQuadric()
    gluCylinder(quadric, radius_base, radius_top, height, slices, stacks)
    gluDeleteQuadric(quadric)

def gambar_kerucut(radius, height, slices, stacks):
    quadric = gluNewQuadric()
    gluCylinder(quadric, radius, 0, height, slices, stacks)
    gluDeleteQuadric(quadric)

def gambar_roket():
    # Mode wireframe atau solid
    if is_wireframe:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Badan roket (silinder utama)
    glColor3f(0.8, 0.8, 0.8)  # Abu-abu
    glPushMatrix()
    glRotatef(90, -1.0, 0.0, 0.0)
    gambar_silinder(0.15, 0.15, 1.2, 32, 32)  # Badan sedikit lebih panjang
    glPopMatrix()

    # Kepala roket (kerucut)
    glColor3f(1.0, 0.0, 0.0)  # Merah
    glPushMatrix()
    glTranslatef(0.0, 1.2, 0.0)  # Posisi kepala dinaikkan
    glRotatef(90, -1.0, 0.0, 0.0)
    gambar_kerucut(0.15, 0.4, 32, 32)  # Kepala sedikit lebih tinggi
    glPopMatrix()

    # Mesin roket (silinder bawah)
    glColor3f(0.6, 0.6, 0.6)  # Abu-abu gelap
    glPushMatrix()
    glTranslatef(0.0, -0.1, 0.0)  # Sesuaikan posisi mesin
    glRotatef(90, -1.0, 0.0, 0.0)
    gambar_silinder(0.17, 0.15, 0.1, 20, 32)
    glPopMatrix()

    # Sirip roket (4 buah)
    glColor3f(0.0, 0.0, 1.0)  # Biru
    for i in range(4):
        glPushMatrix()
        glTranslatef(0.0, -0.55, 0.0)  # Sesuaikan posisi sirip
        glRotatef(90 * i, 0.0, 1.0, 0.0)
        glTranslatef(0.15, 0.45, 0.0)
        glRotatef(-15, 0.0, 0.0, 1.0)  # Kurangi sudut rotasi
        
        # Gambar sirip sebagai segitiga tipis
        glBegin(GL_TRIANGLES)
        glVertex3f(0.0, 0.0, 0.1)  # Perlebar sumbu z
        glVertex3f(0.0, 0.0, -0.1) # Perlebar sumbu z
        glVertex3f(0.3, -0.25, 0.0) # Perlebar dan pendekkan sirip
        glEnd()
        
        glPopMatrix()

    # Jendela roket (lingkaran kecil)
    glColor3f(0.2, 0.2, 0.8)  # Biru tua
    for i in range(3):
        glPushMatrix()
        glTranslatef(0.0, 0.7 - (i * 0.25), 0.152)  # Sesuaikan jarak antar jendela
        glScalef(1.0, 1.0, 0.1)
        quadric = gluNewQuadric()
        gluDisk(quadric, 0, 0.03, 32, 1)
        gluDeleteQuadric(quadric)
        glPopMatrix()

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(800, 800, "Roket 3D Sederhana", None, None)
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
        
        glTranslatef(0.0, 0.0, -5.0)
        glRotatef(putaran_x, 1.0, 0.0, 0.0)
        glRotatef(putaran_y, 0.0, 1.0, 0.0)
        
        gambar_roket()
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main() 