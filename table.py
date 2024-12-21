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

def gambar_meja():
    # Bagian atas meja
    glColor3f(0.6, 0.3, 0.0)  # Warna coklat untuk meja
    glPushMatrix()
    glTranslatef(0.0, 0.5, 0.0)
    gambar_kubus(1.5, 0.1, 1.0)
    glPopMatrix()
    
    # Kaki-kaki meja
    kaki_posisi = [
        (1.3, 0.0, 0.8),
        (-1.3, 0.0, 0.8),
        (1.3, 0.0, -0.8),
        (-1.3, 0.0, -0.8)
    ]
    
    for pos in kaki_posisi:
        glPushMatrix()
        glTranslatef(*pos)
        gambar_kubus(0.1, 0.5, 0.1)
        glPopMatrix()

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(800, 800, "Meja 3D dengan Kaki Terhubung", None, None)
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
        
        # Posisikan meja
        glTranslatef(0.0, 0.0, -5.0)  # Pindahkan meja ke posisi yang sesuai
        glRotatef(putaran_x, 1.0, 0.0, 0.0)
        glRotatef(putaran_y, 0.0, 1.0, 0.0)
        
        gambar_meja()
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main() 