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

def gambar_bintang():
    if is_wireframe:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    points = 5  # Jumlah titik bintang
    outer_radius = 0.5  # Radius luar
    inner_radius = 0.2  # Radius dalam
    thickness = 0.2  # Ketebalan bintang

    # Buat titik-titik bintang
    vertices = []
    for i in range(points * 2):
        angle = i * math.pi / points  # Ubah perhitungan sudut
        radius = outer_radius if i % 2 == 0 else inner_radius
        x = radius * math.cos(angle)
        z = radius * math.sin(angle)
        vertices.append([x, thickness/2, z])
        vertices.append([x, -thickness/2, z])

    # Gambar sisi atas
    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, thickness/2, 0.0)  # Titik pusat
    for i in range(points * 2 + 1):
        idx = i % (points * 2)
        angle = idx * math.pi / points
        radius = outer_radius if idx % 2 == 0 else inner_radius
        x = radius * math.cos(angle)
        z = radius * math.sin(angle)
        glVertex3f(x, thickness/2, z)
    glEnd()

    # Gambar sisi bawah
    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(0.0, -thickness/2, 0.0)  # Titik pusat
    for i in range(points * 2 + 1):
        idx = i % (points * 2)
        angle = idx * math.pi / points
        radius = outer_radius if idx % 2 == 0 else inner_radius
        x = radius * math.cos(angle)
        z = radius * math.sin(angle)
        glVertex3f(x, -thickness/2, z)
    glEnd()

    # Gambar sisi-sisi bintang
    glBegin(GL_QUADS)
    for i in range(points * 2):
        angle1 = i * math.pi / points
        angle2 = ((i + 1) % (points * 2)) * math.pi / points
        
        radius1 = outer_radius if i % 2 == 0 else inner_radius
        radius2 = outer_radius if (i + 1) % 2 == 0 else inner_radius
        
        x1 = radius1 * math.cos(angle1)
        z1 = radius1 * math.sin(angle1)
        x2 = radius2 * math.cos(angle2)
        z2 = radius2 * math.sin(angle2)

        # Hitung normal
        v1 = [x2 - x1, 0.0, z2 - z1]
        length = math.sqrt(v1[0] * v1[0] + v1[2] * v1[2])
        if length < 0.0001:
            normal = [0.0, 0.0, 1.0]
        else:
            normal = [v1[0]/length, 0.0, v1[2]/length]

        glNormal3f(normal[2], 0.0, -normal[0])
        glVertex3f(x1, thickness/2, z1)
        glVertex3f(x2, thickness/2, z2)
        glVertex3f(x2, -thickness/2, z2)
        glVertex3f(x1, -thickness/2, z1)
    glEnd()

def main():
    # Inisialisasi GLFW
    if not glfw.init():
        return

    # Membuat window
    window = glfw.create_window(800, 600, "Bintang 3D", None, None)
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

    # Mengatur posisi cahaya
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
        glTranslatef(0.0, 0.0, -2.0)
        
        # Rotasi objek
        glRotatef(putaran_x, 1.0, 0.0, 0.0)
        glRotatef(putaran_y, 0.0, 1.0, 0.0)

        # Mengatur warna material
        glColor3f(1.0, 1.0, 0.0)  # Warna kuning
        
        # Menggambar bintang
        gambar_bintang()

        # Menukar buffer depan dan belakang
        glfw.swap_buffers(window)
        glfw.poll_events()

    # Membersihkan
    glfw.terminate()

if __name__ == '__main__':
    main() 