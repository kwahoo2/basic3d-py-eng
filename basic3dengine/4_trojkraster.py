#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame, math, sys

def main():

    xw = 800
    yw = 600
    screen = pygame.display.set_mode((xw, yw))
    background_colour = (255,255,255)
    screen.fill(background_colour)

    running = True
    
    while running:
        xps0 = 600 #od lewej do prawej
        yps0 = 100 #z góry na dół
        zf0 = -10.0 #głębość Z w float

        xps1 = 200 #współrzedne wierzchołków trojkąta od najmwyzsze (najmniejsze y) do najniższego
        yps1 = 300
        zf1 = -7.0
#        xps1 = 600
#        yps1 = 300

        xps2 = 500
        yps2 = 500
        zf2 = -4.0

        dx10 = xps1 - xps0
        dx21 = xps2 - xps1
        dx20 = xps2 - xps0
        dy10 = yps1 - yps0
        dy21 = yps2 - yps1
        dy20 = yps2 - yps0
        dzf10 = zf1 - zf0
        dzf21 = zf2 - zf1
        dzf20 = zf2 - zf0

        dwyp10 = math.sqrt(float(math.pow(dx10,2)+math.pow((dy10),2))) #początkowa odległosć między punktami na XY dla 10
        dwyp21 = math.sqrt(float(math.pow(dx21,2)+math.pow((dy21),2)))
        dwyp20 = math.sqrt(float(math.pow(dx20,2)+math.pow((dy20),2)))

        zprop10 = dzf10 / dwyp10 #proporcja przesunięcia XY dla 10 do przesunięcia Z do użycia na krawędziach trójkąta
        zprop21 = dzf21 / dwyp21
        zprop20 = dzf20 / dwyp20

#rasterizer buduje trójkąty z linii poziomych        
        if ((float(dx10) / float(dy10)) < (float(dx20) // float(dy20))):#przypadek gdy 1 jest po lewej 0-2
            for y in range(yps0, yps2): 
                if y < yps1: #gdy jest się między 0 a 1 
                    x0 = xps0 + (y-yps0) * dx10 // dy10
                    x1 = xps0 + (y-yps0) * dx20 // dy20
                    dwyp = math.sqrt(float(math.pow(xps1 - x0,2)+math.pow((yps1 - y),2))) #x0 i y podąza między punktami 1 i 0
                    z0 = zf1 - dwyp * zprop10 #z każdym krokiem mniejsza odległośc, to coraz mniej odejmowane od punktu końcowego zf1
                    dwyp = math.sqrt(float(math.pow(xps2 - x1,2)+math.pow((yps2 - y),2))) #x1 i y podąza między 2 i 0
                    z1 = zf2 - dwyp * zprop20

                else: #gdy jest się między 1 a 2
                    x0 = xps1 + (y-yps1) * dx21 // dy21
                    x1 = xps0 + (y-yps0) * dx20 // dy20
                    dwyp = math.sqrt(float(math.pow(xps2 - x0,2)+math.pow((yps2 - y),2))) #x0 i y podąza między 2 i 1
                    z0 = zf2 - dwyp * zprop21
                    dwyp = math.sqrt(float(math.pow(xps2 - x1,2)+math.pow((yps2 - y),2))) #x1 i y podąza między 2 i 0
                    z1 = zf2 - dwyp * zprop20

                for x in range(x0, x1):
                    if x >=0 and x < xw and y >=0 and y < yw: #ograniczenie tylko do obszaru ekranu
                        #screen.set_at((x, y), (0, 0, 0))
                        z = z1 - ((z1 - z0) / float(x1 - x0)) * float(x1 - x) 


                        screen.set_at((x, y), (int(abs(z * 20)), 255 - int(abs(z * 20)), 0))  #test kolorem zaleznym od z
        else:
            for y in range(yps0, yps2): 
                if y < yps1: #gdy jest się między 0 a 1 
                    x1 = xps0 + (y-yps0) * dx10 // dy10 #zamiana początku z koncem w tym przypadku
                    x0 = xps0 + (y-yps0) * dx20 // dy20
                    dwyp = math.sqrt(float(math.pow(xps1 - x1,2)+math.pow((yps1 - y),2))) #x1 i y podąza między punktami 1 i 0
                    z1 = zf1 - dwyp * zprop10 #z każdym krokiem mniejsza odległośc, to coraz mniej odejmowane od punktu końcowego zf1
                    dwyp = math.sqrt(float(math.pow(xps2 - x0,2)+math.pow((yps2 - y),2))) #x0 i y podąza między 2 i 0
                    z0 = zf2 - dwyp * zprop20

                else: #gdy jest się między 1 a 2
                    x1 = xps1 + (y-yps1) * dx21 // dy21
                    x0 = xps0 + (y-yps0) * dx20 // dy20
                    dwyp = math.sqrt(float(math.pow(xps2 - x1,2)+math.pow((yps2 - y),2))) #x1 i y podąza między 2 i 1
                    z1 = zf2 - dwyp * zprop21
                    dwyp = math.sqrt(float(math.pow(xps2 - x0,2)+math.pow((yps2 - y),2))) #x0 i y podąza między 2 i 0
                    z0 = zf2 - dwyp * zprop20
                for x in range(x0, x1):
                    if x >=0 and x < xw and y >=0 and y < yw: #ograniczenie tylko do obszaru ekranu
                        #screen.set_at((x, y), (0, 0, 0))
                        z = z1 - ((z1 - z0) / float(x1 - x0)) * float(x1 - x) 

                        screen.set_at((x, y), (int(abs(z * 20)), 255 - int(abs(z * 20)), 0))  #test kolorem zaleznym od z            


        for event in pygame.event.get(): #przerwanie pętli
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

main()
