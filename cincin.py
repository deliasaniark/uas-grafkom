import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Variabel untuk rotasi
putaran_x = 0.0
putaran_y = 0.0
kecepatan_putar = 5
is_solid = False

def kontrol_keyboard(window, key, scancode, action, mods):
    global putaran_x, putaran_y, is_solid
    
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
            is_solid = not is_solid

def gambar_cincin():
    radius_luar = 0.4    # Radius luar cincin
    radius_dalam = 0.35  # Radius dalam cincin
    ketebalan = 0.2      # Ketebalan cincin
    segmen = 64          # Jumlah segmen (semakin banyak semakin halus)
    
    if is_solid:
        # Gambar cincin padat
        glBegin(GL_QUAD_STRIP)
        glColor3f(1.0, 0.8, 0.0)  # Warna emas
        
        for i in range(segmen + 1):
            sudut = 2.0 * math.pi * i / segmen
            cos_sudut = math.cos(sudut)
            sin_sudut = math.sin(sudut)
            
            # Titik pada lingkaran dalam
            glNormal3f(cos_sudut, sin_sudut, 0.0)
            glVertex3f(radius_dalam * cos_sudut, radius_dalam * sin_sudut, ketebalan / 2)
            glVertex3f(radius_dalam * cos_sudut, radius_dalam * sin_sudut, -ketebalan / 2)
            
            # Titik pada lingkaran luar
            glVertex3f(radius_luar * cos_sudut, radius_luar * sin_sudut, ketebalan / 2)
            glVertex3f(radius_luar * cos_sudut, radius_luar * sin_sudut, -ketebalan / 2)
        glEnd()
        
        # Gambar sisi depan dan belakang cincin
        for z in [-ketebalan / 2, ketebalan / 2]:
            glBegin(GL_QUAD_STRIP)
            for i in range(segmen + 1):
                sudut = 2.0 * math.pi * i / segmen
                glVertex3f(radius_dalam * math.cos(sudut), radius_dalam * math.sin(sudut), z)
                glVertex3f(radius_luar * math.cos(sudut), radius_luar * math.sin(sudut), z)
            glEnd()
    else:
        # Mode wireframe
        glBegin(GL_LINES)
        glColor3f(1.0, 1.0, 1.0)  # Warna putih
        
        # Gambar garis-garis cincin
        for i in range(segmen):
            sudut1 = 2.0 * math.pi * i / segmen
            sudut2 = 2.0 * math.pi * (i + 1) / segmen
            
            # Lingkaran dalam
            glVertex3f(radius_dalam * math.cos(sudut1), radius_dalam * math.sin(sudut1), ketebalan / 2)
            glVertex3f(radius_dalam * math.cos(sudut2), radius_dalam * math.sin(sudut2), ketebalan / 2)
            glVertex3f(radius_dalam * math.cos(sudut1), radius_dalam * math.sin(sudut1), -ketebalan / 2)
            glVertex3f(radius_dalam * math.cos(sudut2), radius_dalam * math.sin(sudut2), -ketebalan / 2)
            
            # Lingkaran luar
            glVertex3f(radius_luar * math.cos(sudut1), radius_luar * math.sin(sudut1), ketebalan / 2)
            glVertex3f(radius_luar * math.cos(sudut2), radius_luar * math.sin(sudut2), ketebalan / 2)
            glVertex3f(radius_luar * math.cos(sudut1), radius_luar * math.sin(sudut1), -ketebalan / 2)
            glVertex3f(radius_luar * math.cos(sudut2), radius_luar * math.sin(sudut2), -ketebalan / 2)
            
            # Garis penghubung
            glVertex3f(radius_dalam * math.cos(sudut1), radius_dalam * math.sin(sudut1), ketebalan / 2)
            glVertex3f(radius_luar * math.cos(sudut1), radius_luar * math.sin(sudut1), ketebalan / 2)
            glVertex3f(radius_dalam * math.cos(sudut1), radius_dalam * math.sin(sudut1), -ketebalan / 2)
            glVertex3f(radius_luar * math.cos(sudut1), radius_luar * math.sin(sudut1), -ketebalan / 2)
        glEnd()

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(800, 600, "Cincin 3D", None, None)
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
    glLight(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    
    # Atur perspektif
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800.0/600.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Posisikan cincin
        glTranslatef(0.0, 0.0, -2.0)
        glRotatef(putaran_x, 1.0, 0.0, 0.0)
        glRotatef(putaran_y, 0.0, 1.0, 0.0)
        
        gambar_cincin()
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main() 