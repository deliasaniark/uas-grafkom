import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Variabel global untuk kontrol
is_wireframe = False
putaran_x = 0.0
putaran_y = 0.0

def gambar_silinder(radius, tinggi, segmen):
    if is_wireframe:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)  # Mode wireframe
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)  # Mode solid

    glBegin(GL_QUAD_STRIP)
    for i in range(segmen + 1):
        sudut = 2.0 * math.pi * i / segmen
        x = radius * math.cos(sudut)
        y = radius * math.sin(sudut)

        glVertex3f(x, y, tinggi / 2)  # Titik atas
        glVertex3f(x, y, -tinggi / 2)  # Titik bawah
    glEnd()

    # Gambar tutup atas
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0.0, 0.0, tinggi / 2)  # Titik pusat
    for i in range(segmen + 1):
        sudut = 2.0 * math.pi * i / segmen
        x = radius * math.cos(sudut)
        y = radius * math.sin(sudut)
        glVertex3f(x, y, tinggi / 2)
    glEnd()

    # Gambar tutup bawah
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0.0, 0.0, -tinggi / 2)  # Titik pusat
    for i in range(segmen + 1):
        sudut = 2.0 * math.pi * i / segmen
        x = radius * math.cos(sudut)
        y = radius * math.sin(sudut)
        glVertex3f(x, y, -tinggi / 2)
    glEnd()

def kontrol_keyboard(window, key, scancode, action, mods):
    global is_wireframe, putaran_x, putaran_y

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_W:  # Toggle wireframe mode
            is_wireframe = not is_wireframe
        elif key == glfw.KEY_UP:  # Rotate up
            putaran_x += 5.0
        elif key == glfw.KEY_DOWN:  # Rotate down
            putaran_x -= 5.0
        elif key == glfw.KEY_LEFT:  # Rotate left
            putaran_y -= 5.0
        elif key == glfw.KEY_RIGHT:  # Rotate right
            putaran_y += 5.0

def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 800, "Silinder 3D", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, kontrol_keyboard)  # Set callback untuk keyboard
    glEnable(GL_DEPTH_TEST)  # Aktifkan depth testing
    glClearColor(0.1, 0.1, 0.1, 1.0)  # Warna latar belakang gelap

    # Atur perspektif
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800/800, 0.1, 100.0)  # Atur perspektif
    glMatrixMode(GL_MODELVIEW)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glTranslatef(0.0, 0.0, -5.0)  # Pindahkan silinder ke depan
        glRotatef(putaran_x, 1.0, 0.0, 0.0)  # Rotasi silinder
        glRotatef(putaran_y, 0.0, 1.0, 0.0)  # Rotasi silinder

        glColor3f(1.0, 0.5, 0.0)  # Warna oranye untuk silinder
        gambar_silinder(1.0, 2.0, 32)  # Gambar silinder dengan radius 1.0 dan tinggi 2.0

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main() 