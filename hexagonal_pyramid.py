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

def gambar_limas_segi_enam():
    if is_wireframe:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    radius = 0.5
    height = 1.0
    segments = 6

    # Titik puncak limas
    apex = [0.0, height, 0.0]

    # Buat titik-titik dasar segi enam
    base_points = []
    for i in range(segments):
        angle = 2.0 * math.pi * i / segments
        x = radius * math.cos(angle)
        z = radius * math.sin(angle)
        base_points.append([x, 0.0, z])

    # Gambar alas segi enam
    glBegin(GL_POLYGON)
    glNormal3f(0.0, -1.0, 0.0)
    for point in base_points:
        glVertex3fv(point)
    glEnd()

    # Gambar sisi-sisi limas
    glBegin(GL_TRIANGLES)
    for i in range(segments):
        p1 = base_points[i]
        p2 = base_points[(i + 1) % segments]
        
        # Hitung normal untuk setiap sisi
        v1 = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]
        v2 = [apex[0] - p1[0], apex[1] - p1[1], apex[2] - p1[2]]
        
        # Cross product untuk normal
        normal = [
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0]
        ]
        
        # Normalisasi
        length = math.sqrt(sum(x * x for x in normal))
        normal = [x / length for x in normal]
        
        glNormal3fv(normal)
        glVertex3fv(p1)
        glVertex3fv(p2)
        glVertex3fv(apex)
    glEnd() 

def main():
    # Inisialisasi GLFW
    if not glfw.init():
        return

    # Membuat window
    window = glfw.create_window(800, 600, "Limas Segi Enam", None, None)
    if not window:
        glfw.terminate()
        return

    # Membuat konteks OpenGL
    glfw.make_context_current(window)
    glfw.set_key_callback(window, kontrol_keyboard)

    # Pengaturan OpenGL
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    # Pengaturan cahaya
    glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])

    # Loop utama
    while not glfw.window_should_close(window):
        # Membersihkan buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Pengaturan viewport dan proyeksi
        width, height = glfw.get_framebuffer_size(window)
        glViewport(0, 0, width, height)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width/height, 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -3.0)
        
        # Rotasi objek
        glRotatef(putaran_x, 1.0, 0.0, 0.0)
        glRotatef(putaran_y, 0.0, 1.0, 0.0)
        
        # Warna objek
        glColor3f(0.7, 0.7, 1.0)
        
        # Gambar limas
        gambar_limas_segi_enam()

        # Swap buffer dan poll events
        glfw.swap_buffers(window)
        glfw.poll_events()

    # Bersihkan
    glfw.terminate()

if __name__ == '__main__':
    main() 