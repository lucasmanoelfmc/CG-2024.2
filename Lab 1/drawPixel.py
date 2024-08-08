import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def wc_to_ndc(x, y, x_min, x_max, y_min, y_max):
    ndc_x = (x - x_min) / (x_max - x_min)
    ndc_y = (y - y_min) / (y_max - y_min)
    return ndc_x, ndc_y

def ndc_to_wc(ndc_x, ndc_y, x_min, x_max, y_min, y_max):
    wc_x = ndc_x * (x_max - x_min) - x_min
    wc_y = ndc_y * (y_max - y_min) - y_min
    return wc_x, wc_y

def ndc_to_dc(ndc_x, ndc_y, ndh, ndv):  
    dc_x = round(ndc_x * (ndh - 1))
    dc_y = round(ndc_y * (ndv - 1))
    return dc_x, dc_y

def draw_pixel(dc_x, dc_y):
    glBegin(GL_POINTS)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(dc_x, dc_y) 
    glEnd()


pg.init()
info = pg.display.Info()
height = info.current_h - 100
width = info.current_w - 100
display = (width, height)
screen = pg.display.set_mode(display, DOUBLEBUF | OPENGL)
font = pg.font.SysFont('arial', 15)

def draw_text(x, y, text):                                                
    textSurface = font.render(text, True, (255, 255, 255, 255), (0, 0, 0, 0))
    textData = pg.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def main():
    
    ndh = 50
    ndv = 50
    gluOrtho2D(0, ndh, 0, ndv) 

    # WC coordenadas
    wc_x_min = 0
    wc_x_max = 500
    wc_y_min = 0
    wc_y_max = 500
    wc_x = 250
    wc_y = 400

    ndc_coordinates = wc_to_ndc(wc_x, wc_y, wc_x_min, wc_x_max, wc_y_min, wc_y_max)
    dc_coordinates = ndc_to_dc(ndc_coordinates[0], ndc_coordinates[1], ndh, ndv)

    print(f"Height= {height}, Width = {width}")
    
    textWC = "Coordenadas WC: X = " + str(wc_x) + ", Y = " + str(wc_y)
    print(textWC)

    textNDC = "Coordenadas NDC: X = " + str(ndc_coordinates[0]) + ", Y = " + str(ndc_coordinates[1])
    print(textNDC)

    textDC = "Coordenadas DC: X = " + str(dc_coordinates[0]) + ", Y = " + str(dc_coordinates[1]) 
    print(textDC)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_pixel(dc_coordinates[0], dc_coordinates[1])
        draw_text(0, 30, textWC)
        draw_text(0, 15, textNDC)
        draw_text(0, 0, textDC)
        pg.display.flip()

if __name__ == "__main__":
    main()
