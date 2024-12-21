import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

# Variabel global untuk rotasi
rotasi_x = 0.0
rotasi_y = 0.0
mode_wireframe = False

def handle_keyboard(window, key, scancode, action, mods):
    """Fungsi untuk menangani input keyboard"""
    global rotasi_x, rotasi_y, mode_wireframe
    
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_UP:
            rotasi_x += 5
        elif key == glfw.KEY_DOWN:
            rotasi_x -= 5
        elif key == glfw.KEY_LEFT:
            rotasi_y -= 5
        elif key == glfw.KEY_RIGHT:
            rotasi_y += 5
        elif key == glfw.KEY_SPACE:
            mode_wireframe = not mode_wireframe

def gambar_balok(panjang, tinggi, lebar):
    """Fungsi untuk menggambar balok (badan rumah)"""
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if mode_wireframe else GL_FILL)
    
    p = panjang/2
    t = tinggi/2
    l = lebar/2

    glBegin(GL_QUADS)
    # Depan
    glVertex3f(-p, -t, l)
    glVertex3f(p, -t, l)
    glVertex3f(p, t, l)
    glVertex3f(-p, t, l)
    
    # Belakang
    glVertex3f(-p, -t, -l)
    glVertex3f(p, -t, -l)
    glVertex3f(p, t, -l)
    glVertex3f(-p, t, -l)
    
    # Kiri
    glVertex3f(-p, -t, -l)
    glVertex3f(-p, -t, l)
    glVertex3f(-p, t, l)
    glVertex3f(-p, t, -l)
    
    # Kanan
    glVertex3f(p, -t, -l)
    glVertex3f(p, -t, l)
    glVertex3f(p, t, l)
    glVertex3f(p, t, -l)
    
    # Atas
    glVertex3f(-p, t, -l)
    glVertex3f(p, t, -l)
    glVertex3f(p, t, l)
    glVertex3f(-p, t, l)
    
    # Bawah
    glVertex3f(-p, -t, -l)
    glVertex3f(p, -t, -l)
    glVertex3f(p, -t, l)
    glVertex3f(-p, -t, l)
    glEnd()

def gambar_atap_prisma():
    """Fungsi untuk menggambar atap prisma segitiga"""
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if mode_wireframe else GL_FILL)
    
    # Ukuran atap - sesuai gambar
    p = 1.0  # panjang
    t = 0.7  # tinggi atap
    l = 1.0  # lebar atap
    
    # Sisi segitiga depan dan belakang
    glBegin(GL_TRIANGLES)
    # Segitiga depan
    glVertex3f(-p, 0, l)     # kiri bawah
    glVertex3f(p, 0, l)      # kanan bawah
    glVertex3f(0, t, l)      # puncak
    
    # Segitiga belakang
    glVertex3f(-p, 0, -l)    # kiri bawah
    glVertex3f(p, 0, -l)     # kanan bawah
    glVertex3f(0, t, -l)     # puncak
    glEnd()
    
    # Sisi miring atap
    glBegin(GL_QUADS)
    # Sisi miring kiri
    glVertex3f(-p, 0, -l)
    glVertex3f(-p, 0, l)
    glVertex3f(0, t, l)
    glVertex3f(0, t, -l)
    
    # Sisi miring kanan
    glVertex3f(p, 0, -l)
    glVertex3f(p, 0, l)
    glVertex3f(0, t, l)
    glVertex3f(0, t, -l)
    glEnd()

def gambar_rumah():
    """Fungsi untuk menggambar rumah lengkap"""
    # Badan rumah
    glColor3f(0.8, 0.8, 0.8)  # Abu-abu
    glPushMatrix()
    gambar_balok(1.6, 1.0, 2.0)  # Lebih lebar dari panjang
    glPopMatrix()
    
    # Atap
    glColor3f(0.8, 0.2, 0.2)  # Merah
    glPushMatrix()
    glTranslatef(0.0, 0.5, 0.0)
    gambar_atap_prisma()
    glPopMatrix()
    
    # Pintu
    glColor3f(0.4, 0.2, 0.0)  # Coklat
    glPushMatrix()
    glTranslatef(0.0, -0.2, 1.01)
    gambar_balok(0.3, 0.6, 0.02)
    glPopMatrix()
    
    # Jendela kiri
    glColor3f(0.7, 0.9, 1.0)  # Biru muda
    glPushMatrix()
    glTranslatef(-0.5, 0.0, 1.01)
    gambar_balok(0.25, 0.25, 0.02)
    glPopMatrix()
    
    # Jendela kanan
    glPushMatrix()
    glTranslatef(0.5, 0.0, 1.01)
    gambar_balok(0.25, 0.25, 0.02)
    glPopMatrix()

def main():
    """Fungsi utama program"""
    if not glfw.init():
        return
    
    window = glfw.create_window(800, 600, "Rumah 3D Sederhana", None, None)
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    glfw.set_key_callback(window, handle_keyboard)
    
    # Setup tampilan 3D
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800.0/600.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Posisikan kamera
        glTranslatef(0.0, -0.3, -6.0)
        glRotatef(rotasi_x, 1.0, 0.0, 0.0)
        glRotatef(rotasi_y, 0.0, 1.0, 0.0)
        
        gambar_rumah()
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main() 