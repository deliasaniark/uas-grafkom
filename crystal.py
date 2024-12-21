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

def gambar_kristal():
    if is_wireframe:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
    # Set material untuk efek kristal
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.3, 0.5])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.6, 0.6, 0.8, 0.5])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 0.5])
    glMaterialf(GL_FRONT, GL_SHININESS, 100.0)

    sides = 6
    height = 1.0
    radius_top = 0.2
    radius_bottom = 0.4
    radius_middle = 0.5

    # Titik-titik untuk bagian tengah kristal
    middle_points = []
    for i in range(sides):
        angle = 2.0 * math.pi * i / sides
        x = radius_middle * math.cos(angle)
        z = radius_middle * math.sin(angle)
        middle_points.append([x, 0.0, z])

    # Gambar bagian atas kristal
    glBegin(GL_TRIANGLES)
    for i in range(sides):
        p1 = middle_points[i]
        p2 = middle_points[(i + 1) % sides]
        apex = [0.0, height, 0.0]
        
        # Hitung normal
        v1 = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]
        v2 = [apex[0] - p1[0], apex[1] - p1[1], apex[2] - p1[2]]
        normal = [
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0]
        ]
        length = math.sqrt(sum(x * x for x in normal))
        normal = [x / length for x in normal]
        
        glNormal3fv(normal)
        glVertex3fv(p1)
        glVertex3fv(p2)
        glVertex3fv(apex)
    glEnd()

    # Gambar bagian bawah kristal
    glBegin(GL_TRIANGLES)
    for i in range(sides):
        p1 = middle_points[i]
        p2 = middle_points[(i + 1) % sides]
        bottom = [0.0, -height, 0.0]
        
        # Hitung normal
        v1 = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]
        v2 = [bottom[0] - p1[0], bottom[1] - p1[1], bottom[2] - p1[2]]
        normal = [
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0]
        ]
        length = math.sqrt(sum(x * x for x in normal))
        normal = [x / length for x in normal]
        
        glNormal3fv(normal)
        glVertex3fv(p1)
        glVertex3fv(p2)
        glVertex3fv(bottom)
    glEnd() 

def main():
    # Inisialisasi GLFW
    if not glfw.init():
        return

    # Membuat window
    window = glfw.create_window(800, 600, "Kristal 3D", None, None)
    if not window:
        glfw.terminate()
        return

    # Mengatur window sebagai konteks OpenGL saat ini
    glfw.make_context_current(window)
    glfw.set_key_callback(window, kontrol_keyboard)

    # Mengatur pencahayaan
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    
    # Posisi cahaya
    glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

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
        
        # Rotasi berdasarkan input keyboard
        glRotatef(putaran_x, 1.0, 0.0, 0.0)
        glRotatef(putaran_y, 0.0, 1.0, 0.0)

        # Menggambar kristal
        gambar_kristal()

        # Menukar buffer depan dan belakang
        glfw.swap_buffers(window)
        glfw.poll_events()

    # Membersihkan
    glfw.terminate()

if __name__ == "__main__":
    main() 