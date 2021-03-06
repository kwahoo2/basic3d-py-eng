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

    troj0 = (0, 1, 3) #indeks wierzchołków wybranych z krotki "chmura, dal pierwszego trójkąta, + indeks kolor
    troj1 = (0, 3, 2)
    troj2 = (2, 3, 7)
    troj3 = (2, 7, 6)
    troj4 = (4, 1, 0)
    troj5 = (1, 4, 5)
    troj6 = (1, 7, 3)
    troj7 = (1, 5, 7)
    troj8 = (4, 0, 2)
    troj9 = (4, 2, 6)
    troj10 = (5, 4, 6) 
    troj11 = (5, 6, 7) #na szesciobok potrzeba 12 trójkątów

    zbiortroj = (troj0, troj1, troj2, troj3, troj4, troj5, troj5, troj7, troj8, troj9, troj10, troj11)
#alternatywnie zbiortroj = ((0, 1, 3), (0, 2, 3), itd)

    running = True #start głównej pętli programu
    while running:
        screen.fill(background_colour) #czyszczenie klatki

        for tr in range(0, len(zbiortroj)): #pętla 12-elemetowa, 0-11, bo ostania jest pomijana, len - długość
            trojkat = zbiortroj[tr]
            xps = [0, 0, 0] #tymczasowa lista punktów [] to listy, () to krotki 
            yps = [0, 0, 0]
            for i in range (0, 3):
                numerpunktu = trojkat[i] #pobranie indeksu punktu, "zbiortroj" ma wskazywac kolejne punkty z "chmura"
                punkt = chmura[numerpunktu] #wybranie kolejnej krotki z krotki "chmura"
                x = punkt[0] #wybrana pierwsza współrzedna
                y = punkt[1]
                z = punkt[2]
                xp = zk * x /(zp + zk - z) #wyliczenie projekcji dla x-ów
                yp = zk * y /(zp + zk - z) #wyliczenie projekcji dla y-ów
                xps[i] = int((xw / 2) + (xp * skala)) #wysrodkowanie, skalowanie oraz konwersja do liczby całkowitej
                yps[i] = int((yw / 2) - (yp * skala)) #wysrodkowanie, skalowanie i odwrócenie y oraz konwersja do liczby całkowitej
                screen.set_at((xps[i], yps[i]), (0, 0, 0)) #narysowanie punktu w zadanym miejscu
                pygame.draw.circle(screen, (0, 0, 0), (xps[i], yps[i]), 10, 1) #obrysowanie punktów okręgami dla lepszej widoczności
        
            pygame.draw.line(screen, (0, 0, 0), (xps[0], yps[0]), (xps[1], yps[1]), 1)#rysuj linię łączącą punkty
            pygame.draw.line(screen, (0, 0, 0), (xps[1], yps[1]), (xps[2], yps[2]), 1)#rysuj linię łączącą punkty
            pygame.draw.line(screen, (0, 0, 0), (xps[2], yps[2]), (xps[0], yps[0]), 1)#rysuj linię łączącą punkty

        pygame.display.flip()
        for event in pygame.event.get(): #przerwanie pętli
            if event.type == pygame.QUIT:
                running = False

main()
