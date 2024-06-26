#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame, math, sys

def main():
    
    xw = 800
    yw = 600
    screen = pygame.display.set_mode((xw, yw))
    fizxw = 2.0 #"fizyczna" (w jednostach przestrzeni 3D) szerokość okna widzenia
    fov = math.radians(75) #określenie szerokości pola widzenia
    zp = 6.0 #odległość od środka układu współrzędnych do "ekranu"
    zk = fizxw / (2 * math.tan(fov / 2)) #odległość od "ekranu" do obserwatora
    skala = int(xw / fizxw) #skala n pikseli na 1 jednostkę przestrzeni

    background_colour = (255,255,255)
    screen.fill(background_colour)

    p0 = (1.0, -3.0, 1.0) #punkt pierwszy - krotka, w odróżnieniu od listy niezmienna, 1.0, bo liczba zmiennoprzecinkowa
    p1 = (1.0, -1.0, 1.0)
    p2 = (-1.0, -3.0, 1.0)
    p3 = (-1.0, -1.0, 1.0)
    p4 = (1.0, -3.0, -1.0)
    p5 = (1.0, -1.0, -1.0)
    p6 = (-1.0, -3.0, -1.0)
    p7 = (-1.0, -1.0, -1.0)

    chmura = (p0, p1, p2, p3, p4, p5, p6, p7) #zebranie wszystkich krotek do jednej nadrzędnej

    running = True #start głównej pętli programu
    while running:
        screen.fill(background_colour) #czyszczenie klatki

        for i in range(0, len(chmura)): #pętla 8-elementowa, 0-7, bo ostatnia jest pomijana, len - dlugosc
            print (i)
            punkt = chmura[i] #wybranie kolejnej krotki z nadrzędnej
            print (punkt)
            x = punkt[0] #wybrana pierwsza współrzedna
            y = punkt[1]
            z = punkt[2]
            xp = zk * x /(zp + zk - z) #wyliczenie projekcji dla x-ów
            yp = zk * y /(zp + zk - z) #wyliczenie projekcji dla y-ów
            xps = int((xw / 2) + (xp * skala)) #wyśrodkowanie, skalowanie oraz konwersja do liczby całkowitej
            yps = int((yw / 2) - (yp * skala)) #wyśrodkowanie, skalowanie i odwrocenie y oraz konwersja do liczby całkowitej
            print ("x"+str(xps)) #wypisanie wartści w konsoli
            print ("y"+str(yps))
            screen.set_at((xps, yps), (0, 0, 0)) #narysowanie punktu w zadanym miejscu
            pygame.draw.circle(screen, (0, 0, 0), (xps, yps), 10, 1) #obrysowanie punktów okręgami dla lepszej widoczności

        pygame.display.flip()
        for event in pygame.event.get(): #przerwanie pętli
            if event.type == pygame.QUIT:
                running = False

main()
