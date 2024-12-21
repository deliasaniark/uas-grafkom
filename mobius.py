import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
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

def gambar_mobius(segments, twists):
    if is_wireframe:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glColor3f(1.0, 1.0, 1.0)  # Warna putih untuk wireframe
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glBegin(GL_QUAD_STRIP)
    for i in range(segments + 1):
        theta = i * 2.0 * np.pi / segments
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        for j in range(2):
            phi = j * np.pi
            r = 1 + 0.5 * np.cos(twists * theta + phi)
            x = r * cos_theta
            y = r * sin_theta
            z = 0.5 * np.sin(twists * theta + phi)
            
            # Normal untuk pencahayaan
            nx = -0.5 * twists * sin_theta * np.sin(twists * theta + phi)
            ny = 0.5 * twists * cos_theta * np.sin(twists * theta + phi)
            nz = 0.5 * np.cos(twists * theta + phi)
            glNormal3f(nx, ny, nz)
            
            # Warna gradien
            glColor3f(0.5 * (1 + cos_theta), 0.5 * (1 + sin_theta), 0.5 * (1 + z))
            
            glVertex3f(x, y, z)
    glEnd()

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(800, 800, "Pita Möbius 3D Halus", None, None)
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
    
    # Aktifkan anti-aliasing
    glEnable(GL_MULTISAMPLE)
    
    # Atur perspektif
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0, 0.1, 100.0)  # Menggunakan aspek rasio 1.0 untuk menjaga proporsi
    glMatrixMode(GL_MODELVIEW)
    
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Posisikan pita Möbius
        glTranslatef(0.0, 0.0, -5.0)  # Pindahkan pita Möbius ke posisi yang sesuai
        glRotatef(putaran_x, 1.0, 0.0, 0.0)
        glRotatef(putaran_y, 0.0, 1.0, 0.0)
        
        gambar_mobius(segments=500, twists=1)
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main() 