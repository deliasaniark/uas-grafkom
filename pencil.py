import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

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

def gambar_silinder(radius, height, slices, stacks):
    if is_wireframe:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    quadric = gluNewQuadric()
    gluCylinder(quadric, radius, radius, height, slices, stacks)
    gluDisk(quadric, 0, radius, slices, stacks)  # Tutup bagian bawah
    glTranslatef(0, 0, height)
    gluDisk(quadric, 0, radius, slices, stacks)  # Tutup bagian atas
    gluDeleteQuadric(quadric)

def gambar_kerucut(radius, height, slices, stacks):
    if is_wireframe:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    quadric = gluNewQuadric()
    gluCylinder(quadric, radius, 0.0, height, slices, stacks)
    gluDisk(quadric, 0, radius, slices, stacks)  # Tutup bagian bawah
    gluDeleteQuadric(quadric)

def gambar_pensil():
    # Badan pensil
    glColor3f(1.0, 0.85, 0.0)  # Warna kuning untuk badan pensil
    glPushMatrix()
    glTranslatef(0.0, 0.0, -1.8)
    gambar_silinder(0.1, 2.0, 32, 32)
    glPopMatrix()
    
    # Ujung pensil
    glColor3f(0.5, 0.35, 0.05)  # Warna coklat untuk ujung pensil
    glPushMatrix()
    glTranslatef(0.0, 0.0, -1.8)
    glRotatef(180, 1.0, 0.0, 0.0)  # Rotasi untuk mengarahkan ujung ke depan
    gambar_kerucut(0.1, 0.2, 32, 32)
    glPopMatrix()
    
    # Penghapus
    glColor3f(1.0, 0.0, 0.0)  # Warna merah untuk penghapus
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.2)
    gambar_silinder(0.1, 0.2, 32, 32)
    glPopMatrix()

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(800, 800, "Pensil 3D", None, None)
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
        
        # Posisikan pensil
        glTranslatef(0.0, 0.0, -5.0)  # Pindahkan pensil ke posisi yang sesuai
        glRotatef(putaran_x, 1.0, 0.0, 0.0)
        glRotatef(putaran_y, 0.0, 1.0, 0.0)
        
        gambar_pensil()
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main() 