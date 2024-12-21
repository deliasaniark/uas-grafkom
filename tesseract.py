import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

# Variabel untuk rotasi
putaran_x = 0.0
putaran_y = 0.0
putaran_w = 0.0  # Rotasi dalam dimensi keempat
kecepatan_putar = 5
is_wireframe = False  # Ubah ke False untuk mode solid

def kontrol_keyboard(window, key, scancode, action, mods):
    global putaran_x, putaran_y, putaran_w, is_wireframe
    
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_UP:
            putaran_x += kecepatan_putar
        if key == glfw.KEY_DOWN:
            putaran_x -= kecepatan_putar
        if key == glfw.KEY_LEFT:
            putaran_y -= kecepatan_putar
        if key == glfw.KEY_RIGHT:
            putaran_y += kecepatan_putar
        if key == glfw.KEY_Q:
            putaran_w += kecepatan_putar
        if key == glfw.KEY_E:
            putaran_w -= kecepatan_putar
        if key == glfw.KEY_SPACE:
            is_wireframe = not is_wireframe

def rotasi_4d(titik, sudut_w):
    rad = math.radians(sudut_w)
    cos_w = math.cos(rad)
    sin_w = math.sin(rad)
    
    x = titik[0] * cos_w - titik[3] * sin_w
    y = titik[1]
    z = titik[2]
    w = titik[0] * sin_w + titik[3] * cos_w
    
    return [x, y, z, w]

def proyeksi_4d_ke_3d(titik_4d):
    w = titik_4d[3]
    faktor = 2.0 / (3.0 - w)
    
    x = titik_4d[0] * faktor
    y = titik_4d[1] * faktor
    z = titik_4d[2] * faktor
    
    return [x, y, z]

def gambar_tesseract():
    # Definisikan vertices dengan ukuran yang lebih besar
    vertices_4d = [
        [-1.0, -1.0, -1.0, -1.0], [1.0, -1.0, -1.0, -1.0],
        [-1.0,  1.0, -1.0, -1.0], [1.0,  1.0, -1.0, -1.0],
        [-1.0, -1.0,  1.0, -1.0], [1.0, -1.0,  1.0, -1.0],
        [-1.0,  1.0,  1.0, -1.0], [1.0,  1.0,  1.0, -1.0],
        [-1.0, -1.0, -1.0,  1.0], [1.0, -1.0, -1.0,  1.0],
        [-1.0,  1.0, -1.0,  1.0], [1.0,  1.0, -1.0,  1.0],
        [-1.0, -1.0,  1.0,  1.0], [1.0, -1.0,  1.0,  1.0],
        [-1.0,  1.0,  1.0,  1.0], [1.0,  1.0,  1.0,  1.0]
    ]

    # Lakukan rotasi dan proyeksi untuk semua mode
    vertices_rotated = [rotasi_4d(v, putaran_w) for v in vertices_4d]
    vertices_3d = [proyeksi_4d_ke_3d(v) for v in vertices_rotated]

    if is_wireframe:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        
        # Gambar garis-garis kubus dalam dan luar
        edges = [
            # Kubus dalam
            (0,1), (1,3), (3,2), (2,0),  # sisi depan
            (4,5), (5,7), (7,6), (6,4),  # sisi belakang
            (0,4), (1,5), (2,6), (3,7),  # penghubung depan-belakang
            
            # Kubus luar
            (8,9), (9,11), (11,10), (10,8),  # sisi depan
            (12,13), (13,15), (15,14), (14,12),  # sisi belakang
            (8,12), (9,13), (10,14), (11,15),  # penghubung depan-belakang
            
            # Garis penghubung antara kubus dalam dan luar
            (0,8), (1,9), (2,10), (3,11),  # depan ke depan
            (4,12), (5,13), (6,14), (7,15)  # belakang ke belakang
        ]

        glColor3f(1.0, 1.0, 1.0)  # Warna putih untuk wireframe
        glBegin(GL_LINES)
        for edge in edges:
            for vertex_id in edge:
                glVertex3fv(vertices_3d[vertex_id])
        glEnd()
        
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        # Aktifkan transparansi
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Definisikan sisi-sisi kubus dengan normal
        faces_dalam = [
            ((0,1,3,2), (0.0, 0.0, 1.0)),
            ((4,5,7,6), (0.0, 0.0, -1.0)),
            ((2,3,7,6), (0.0, 1.0, 0.0)),
            ((0,1,5,4), (0.0, -1.0, 0.0)),
            ((0,2,6,4), (-1.0, 0.0, 0.0)),
            ((1,3,7,5), (1.0, 0.0, 0.0))
        ]
        
        faces_luar = [
            ((8,9,11,10), (0.0, 0.0, 1.0)),
            ((12,13,15,14), (0.0, 0.0, -1.0)),
            ((10,11,15,14), (0.0, 1.0, 0.0)),
            ((8,9,13,12), (0.0, -1.0, 0.0)),
            ((8,10,14,12), (-1.0, 0.0, 0.0)),
            ((9,11,15,13), (1.0, 0.0, 0.0))
        ]

        # Gambar kubus dalam (tidak transparan)
        glColor4f(0.5, 0.5, 1.0, 1.0)  # Biru solid
        glBegin(GL_QUADS)
        for face, normal in faces_dalam:
            glNormal3fv(normal)
            for vertex_id in face:
                glVertex3fv(vertices_3d[vertex_id])
        glEnd()

        # Gambar kubus luar (transparan)
        glColor4f(0.5, 0.5, 1.0, 0.3)  # Biru transparan
        glBegin(GL_QUADS)
        for face, normal in faces_luar:
            glNormal3fv(normal)
            for vertex_id in face:
                glVertex3fv(vertices_3d[vertex_id])
        glEnd()

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(800, 800, "Tesseract 4D Transparan", None, None)
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    glfw.set_key_callback(window, kontrol_keyboard)
    
    # Pengaturan pencahayaan
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    
    # Atur posisi dan warna lampu
    glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    
    glClearColor(0.0, 0.0, 0.0, 1.0)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800.0/800.0, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        glTranslatef(0.0, 0.0, -8.0)
        glRotatef(putaran_x, 1.0, 0.0, 0.0)
        glRotatef(putaran_y, 0.0, 1.0, 0.0)
        
        gambar_tesseract()
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main() 