import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

# Variabel untuk mengatur rotasi dan tampilan kubus
putaran_x = 0.0
putaran_y = 0.0
kecepatan_putar = 5
is_solid = False  # False = mode kerangka, True = mode padat

def kontrol_keyboard(window, key, scancode, action, mods):
    global putaran_x, putaran_y, is_solid
    
    # Ketika tombol ditekan
    if action == glfw.PRESS or action == glfw.REPEAT:
        # Kontrol rotasi dengan tombol panah
        if key == glfw.KEY_UP:    
            putaran_x += kecepatan_putar
        if key == glfw.KEY_DOWN:  
            putaran_x -= kecepatan_putar
        if key == glfw.KEY_LEFT:  
            putaran_y -= kecepatan_putar
        if key == glfw.KEY_RIGHT: 
            putaran_y += kecepatan_putar
        # Tombol spasi untuk mengubah mode tampilan
        if key == glfw.KEY_SPACE:
            is_solid = not is_solid

def gambar_kubus():
    if is_solid:  # Mode kubus padat
        glBegin(GL_QUADS)
        glColor3f(0.0, 0.5, 1.0)  # Warna biru muda
        
        # Sisi depan
        glNormal3f(0.0, 0.0, 1.0)  # Normal untuk pencahayaan
        glVertex3f(-0.5, -0.5,  0.5)
        glVertex3f( 0.5, -0.5,  0.5)
        glVertex3f( 0.5,  0.5,  0.5)
        glVertex3f(-0.5,  0.5,  0.5)
        
        # Sisi belakang
        glNormal3f(0.0, 0.0, -1.0)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5,  0.5, -0.5)
        glVertex3f( 0.5,  0.5, -0.5)
        glVertex3f( 0.5, -0.5, -0.5)
        
        # Sisi atas
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(-0.5,  0.5, -0.5)
        glVertex3f(-0.5,  0.5,  0.5)
        glVertex3f( 0.5,  0.5,  0.5)
        glVertex3f( 0.5,  0.5, -0.5)
        
        # Sisi bawah
        glNormal3f(0.0, -1.0, 0.0)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f( 0.5, -0.5, -0.5)
        glVertex3f( 0.5, -0.5,  0.5)
        glVertex3f(-0.5, -0.5,  0.5)
        
        # Sisi kanan
        glNormal3f(1.0, 0.0, 0.0)
        glVertex3f( 0.5, -0.5, -0.5)
        glVertex3f( 0.5,  0.5, -0.5)
        glVertex3f( 0.5,  0.5,  0.5)
        glVertex3f( 0.5, -0.5,  0.5)
        
        # Sisi kiri
        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, -0.5,  0.5)
        glVertex3f(-0.5,  0.5,  0.5)
        glVertex3f(-0.5,  0.5, -0.5)
        glEnd()
        
    else:  # Mode kerangka kubus
        glBegin(GL_LINES)  # Mulai menggambar garis
        glColor3f(1.0, 1.0, 1.0)  # Warna putih
        
        # Titik-titik sudut kubus
        titik = [
            [-0.5, -0.5, -0.5], [ 0.5, -0.5, -0.5],
            [ 0.5,  0.5, -0.5], [-0.5,  0.5, -0.5],
            [-0.5, -0.5,  0.5], [ 0.5, -0.5,  0.5],
            [ 0.5,  0.5,  0.5], [-0.5,  0.5,  0.5]
        ]
        
        # Garis-garis yang menghubungkan titik
        garis = [
            (0,1), (1,2), (2,3), (3,0),  # sisi belakang
            (4,5), (5,6), (6,7), (7,4),  # sisi depan
            (0,4), (1,5), (2,6), (3,7)   # penghubung depan-belakang
        ]
        
        # Menggambar garis
        for g in garis:
            for t in g:
                glVertex3fv(titik[t])
        glEnd()

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(800, 600, "Kubus 3D", None, None)
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    glfw.set_key_callback(window, kontrol_keyboard)
    
    # Pengaturan perspektif
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800.0/600.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    
    # Pengaturan 3D
    glEnable(GL_DEPTH_TEST)
    
    # Pencahayaan yang diperbaiki
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    # Atur posisi lampu (pindahkan ke depan dan atas)
    glLight(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])
    
    # Atur warna cahaya lebih terang
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    
    # Warna background
    glClearColor(0.2, 0.2, 0.2, 1.0)  # Background abu-abu gelap
    
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        glTranslatef(0.0, 0.0, -5.0)
        glRotatef(putaran_x, 1.0, 0.0, 0.0)
        glRotatef(putaran_y, 0.0, 1.0, 0.0)
        
        gambar_kubus()
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

# Jalankan program
if __name__ == "__main__":
    main()
