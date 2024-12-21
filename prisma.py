import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

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

def gambar_prisma():
    if is_wireframe:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Titik-titik segitiga alas
    points = [
        [-0.5, 0.0, -0.3],
        [0.5, 0.0, -0.3],
        [0.0, 0.0, 0.6]
    ]
    height = 1.0  # Tinggi prisma

    glBegin(GL_TRIANGLES)
    # Alas bawah
    glNormal3f(0.0, -1.0, 0.0)
    for p in points:
        glVertex3f(p[0], -height/2, p[2])

    # Alas atas
    glNormal3f(0.0, 1.0, 0.0)
    for p in points:
        glVertex3f(p[0], height/2, p[2])
    glEnd()

    # Sisi-sisi prisma
    glBegin(GL_QUADS)
    for i in range(3):
        p1 = points[i]
        p2 = points[(i+1)%3]
        
        # Hitung normal untuk sisi
        dx = p2[0] - p1[0]
        dz = p2[2] - p1[2]
        length = math.sqrt(dx*dx + dz*dz)
        nx = dz/length
        nz = -dx/length
        
        glNormal3f(nx, 0.0, nz)
        glVertex3f(p1[0], -height/2, p1[2])
        glVertex3f(p2[0], -height/2, p2[2])
        glVertex3f(p2[0], height/2, p2[2])
        glVertex3f(p1[0], height/2, p1[2])
    glEnd()

def main():
    # Inisialisasi GLFW
    if not glfw.init():
        return

    # Membuat window
    window = glfw.create_window(800, 600, "Prisma 3D", None, None)
    if not window:
        glfw.terminate()
        return

    # Mengatur window sebagai konteks OpenGL saat ini
    glfw.make_context_current(window)
    
    # Mengatur callback keyboard
    glfw.set_key_callback(window, kontrol_keyboard)

    # Mengatur pencahayaan
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)

    # Posisi cahaya
    glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])

    # Loop utama
    while not glfw.window_should_close(window):
        # Membersihkan buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Mengatur proyeksi perspektif
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800.0/600.0, 0.1, 100.0)

        # Mengatur posisi kamera
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5.0)
        
        # Rotasi objek
        glRotatef(putaran_x, 1.0, 0.0, 0.0)
        glRotatef(putaran_y, 0.0, 1.0, 0.0)

        # Menggambar prisma
        gambar_prisma()

        # Menukar buffer depan dan belakang
        glfw.swap_buffers(window)
        
        # Memproses events
        glfw.poll_events()

    # Membersihkan
    glfw.terminate()

if __name__ == '__main__':
    main()