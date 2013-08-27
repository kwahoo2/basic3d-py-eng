#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame, math, sys, random

def main():
    
    xw = 800
    yw = 600
    screen = pygame.display.set_mode((xw, yw))
    lipx = xw * yw #całkowita liczba pikseli
    fizxw = 2.0 #"fizyczna" (w jednostach przestrzeni 3D) szerokość okna widzenia
    fov = math.radians(75) #określenie szerokosci pola widzenia
    zp = 1000.0 #odległość od środka układu współrzednych do "ekranu"
    zk = fizxw / (2 * math.tan(fov / 2)) #odległość od "ekranu" do obserwatora
    skala = int(xw / fizxw) #skala n pikseli na 1 jednostkę przestrzeni

    bufram = [] #z-bufor

    for i in range(0, lipx):
        bufram.append(-100000.0) #tworzenie nowej czystej listy dla koloru głębi z (float)

    background_colour = (255,255,255)
    screen.fill(background_colour)
    
    zbiorkolor = ((0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 0, 255)) 
    
    chmura, zbiortroj = importujdane() #pobranie sanych z pliku
    
    wektorswiatla = (1.0, 0.0, -1.0) #wektor oświetlenia wykorzystywany przy cieniowaniu

    running = True #start główeje pętli programu
    
    krok = 0

    while running:
        screen.fill(background_colour) #czyszczenie klatki
        for i in range(0, lipx):
            bufram[i] = -100000.0 # wypełnianie Z bufora bardzo małymi wartościami Z (daleko od obserwatora)


        for tr in range(0, len(zbiortroj)): #pętla 12-elementowa, 0-11, bo ostania jest pomijana, len - długość
            trojkat = zbiortroj[tr]
            #print trojkat
            xps = [0, 0, 0] #tymczasowa lista punktów [] to listy, () to krotki 
            yps = [0, 0, 0]
            zf = [0.0, 0.0, 0.0]
            trojktrans = [0.0, 0.0, 0.0] #wierzchołki trójkata po transformacji
            for i in range (0, 3):
                numerpunktu = trojkat[i] #pobranie indeksu punktu, "zbiortroj" ma wkazywac kolejne punkty z "chmura"
                punkt = chmura[numerpunktu] #wybranie kolejnej krotki z krotki "chmura"
                x = punkt[0] #wybrany pierwsza współrzedna
                y = punkt[1]
                z = punkt[2]
                x, y, z = transformacja(x, y, z, krok) #wywołanie funcji transformacji
                trojktrans[i] = [x, y, z] #trojkat po transformacji, wprowszane na potrzeby wektora normalnego

                xp = zk * x /(zp + zk - z) #wyliczenie projekcji dla x-ów
                yp = zk * y /(zp + zk - z) #wyliczenie projekcji dla y-ów
                #skala = 100 #skala 100 pikseli na 1 jednostkę przestrzeni
                xps[i] = int((xw / 2) + (xp * skala)) #wysrodkowanie, skalowanie oraz konwersja do liczby całkowitej
                yps[i] = int((yw / 2) - (yp * skala)) #wysrodkowanie, skalowanie i odwrócenie y oraz konwersja do liczby całkowitej
                zf[i] = z    
            kolortrojk = zbiorkolor[trojkat[3]] #czwarty zrgument trojkata to kolor
            #print [xps[0], yps[0], zf[0]], [xps[1], yps[1], zf[1]], [xps[2], yps[2], zf[2]], kolortrojk
            normalny = wnormal(trojktrans[0], trojktrans[1], trojktrans[2]) #wyliczenie wektora normalnego, potrzebne do oswietlenia
            #print normalny
            coswektorow = coswekt(normalny, wektorswiatla)
            #print coswektorow
            kolormod = [0, 0, 0] #dodatkowa lista z kolorami po modyfikacjach
            kolormod[0] = int((1 - coswektorow) * kolortrojk[0] * 0.5)
            kolormod[1] = int((1 - coswektorow) * kolortrojk[1] * 0.5)
            kolormod[2] = int((1 - coswektorow) * kolortrojk[2] * 0.5)
            bufram = rysujtrojk([xps[0], yps[0], zf[0]], [xps[1], yps[1], zf[1]], [xps[2], yps[2], zf[2]], kolormod, xw, yw, screen, bufram, zp) #wywołanie rasterizera trójkąta ze zwrotem z-bufora
        pygame.display.flip()
        krok = krok + 1
        for event in pygame.event.get(): #przerwanie pętli
            if event.type == pygame.QUIT:
                running = False

def rysujtrojk(wierz0, wierz1, wierz2, kolortrojk, xw, yw, screen, bufram, zp): #rasterizer trójkątów

    while 1: #prosty algorytm sortowania 3 elementów
        if wierz0[1] > wierz1[1]:
            wierztemp = wierz0
            wierz0 = wierz1
            wierz1 = wierztemp    

        if wierz1[1] > wierz2[1]:
            wierztemp = wierz1
            wierz1 = wierz2
            wierz2 = wierztemp 

        if wierz0[1] <= wierz1[1] and wierz1[1] <= wierz2[1]: #przerwanie gdy uporządkowane rosnąco wg 2 elementu
            break 

    #print wierz0, wierz1, wierz2

    xps0 = wierz0[0] #od lewej do prawej
    yps0 = wierz0[1] #z góry na dół
    zf0 = wierz0[2] #głębość Z w float
    xps1 = wierz1[0] #współrzedne wierzchołków trojkąta od najmwyzsze (najmniejsze y) do najniższego
    yps1 = wierz1[1]
    zf1 = wierz1[2]
    xps2 = wierz2[0]
    yps2 = wierz2[1]
    zf2 = wierz2[2]

    dx10 = xps1 - xps0
    dx21 = xps2 - xps1
    dx20 = xps2 - xps0
    dy10 = yps1 - yps0
    dy21 = yps2 - yps1
    dy20 = yps2 - yps0
    dzf10 = zf1 - zf0
    dzf21 = zf2 - zf1
    dzf20 = zf2 - zf0

    if dx10 != 0 or dy10 != 0:
        dwyp10 = math.sqrt(float(math.pow(dx10,2)+math.pow((dy10),2))) #początkowa odległosć między punktami na XY dla 10
        zprop10 = dzf10 / dwyp10 #proporcja przesunięcia XY dla 10 do przesunięcia Z do użycia na krawędziach trójkąta
    else:
        zprop10 = 0
    
    if dx21 != 0 or dy21 != 0:
        dwyp21 = math.sqrt(float(math.pow(dx21,2)+math.pow((dy21),2)))
        zprop21 = dzf21 / dwyp21
    else:
        zprop21 = 0

    if dx20 != 0 or dy20 != 0:
        dwyp20 = math.sqrt(float(math.pow(dx20,2)+math.pow((dy20),2)))
        zprop20 = dzf20 / dwyp20
    else:
        zprop20 = 0

#rasterizer buduje trójkąty z linii poziomych      

    lewy = False #pomocnicza zmienna, jeśli true, to 1 jest po lewej 0-2
    if dy10 != 0  and dy21 != 0 and dy20 != 0: #tylko gdy y są różne, bez dzielenia przez 0 
        if ((float(dx10) / float(dy10)) < (float(dx20) / float(dy20))):#przypadek gdy 1 jest po lewej 0-2, konwersja int do float dla wyzszej dokładności porównania
            lewy = True
        else:
            lewy = False 
    elif dy10 == 0 and dy21 != 0 and dy20 != 0: #gdy poziomo miedzy 0-1
        if dx10 < 0:
            lewy = True
        else:
            lewy = False
    elif dy10 != 0 and dy21 == 0 and dy20 != 0: #gdy poziomo miedzy 2-1
        if dx21 > 0:
            lewy = True
        else:
            lewy = False
    else: #zwykle gdy poziomo miedzy 2-0, to 1-0 i 2-1, linia prosta pozioma
        if dx20 > 0:
            lewy = True
        else:
            lewy = False

        

    if (lewy == True):#przypadek gdy 1 jest po lewej 0-2
        for y in range(yps0, yps2): 
            if y < yps1: #gdy jest się między 0 a 1 
                if dy10 != 0:
                    x0 = xps0 + (y-yps0) * dx10 / dy10 #x0 zawsze po lewej w stosunku do x1
                else:
                    x0 = xps1
                if dy20 != 0:
                    x1 = xps0 + (y-yps0) * dx20 / dy20
                else:
                    x1 = xps0
                dwyp = math.sqrt(float(math.pow(xps1 - x0,2)+math.pow((yps1 - y),2))) #x0 i y podąza między punktami 1 i 0
                z0 = zf1 - dwyp * zprop10 #z każdym krokiem mniejsza odległośc, to coraz mniej odejmowane od punktu końcowego zf1
                dwyp = math.sqrt(float(math.pow(xps2 - x1,2)+math.pow((yps2 - y),2))) #x1 i y podąza między 2 i 0
                z1 = zf2 - dwyp * zprop20
                #print x0, y, z0

            else: #gdy jest się między 1 a 2
                if dy21 != 0:
                    x0 = xps1 + (y-yps1) * dx21 / dy21
                else:
                    x0 = xps1
                if dy20 != 0:
                    x1 = xps0 + (y-yps0) * dx20 / dy20
                else:
                    x1 = xps2
                dwyp = math.sqrt(float(math.pow(xps2 - x0,2)+math.pow((yps2 - y),2))) #x0 i y podąza między 2 i 1
                z0 = zf2 - dwyp * zprop21
                dwyp = math.sqrt(float(math.pow(xps2 - x1,2)+math.pow((yps2 - y),2))) #x1 i y podąza między 2 i 0
                z1 = zf2 - dwyp * zprop20
                #print x0, y, z0
            for x in range(x0, x1):
                if x >=0 and x < xw and y >=0 and y < yw: #ograniczenie tylko do obszaru ekranu
                    #screen.set_at((x, y), (0, 0, 0))
                    z = z1 - ((z1 - z0) / float(x1 - x0)) * float(x1 - x) 
                    #print x, y, z
                    pozpix = x + y * xw
                    if (z > bufram[pozpix] and z < zp): #zapisuje piksel tylko gdy jest blizej obserwatora niz pozostałe
                        screen.set_at((x, y), (kolortrojk))
                        bufram[pozpix] = z
    else:
        for y in range(yps0, yps2): 
            if y < yps1: #gdy jest się między 0 a 1 
                if dy10 != 0:
                    x1 = xps0 + (y-yps0) * dx10 / dy10 #zamiana początku z koncem w tym przypadku
                else:
                    x1 = xps1
                if dy20 != 0:                
                    x0 = xps0 + (y-yps0) * dx20 / dy20
                else:
                    x0 = xps0
                dwyp = math.sqrt(float(math.pow(xps1 - x1,2)+math.pow((yps1 - y),2))) #x1 i y podąza między punktami 1 i 0
                z1 = zf1 - dwyp * zprop10 #z każdym krokiem mniejsza odległośc, to coraz mniej odejmowane od punktu końcowego zf1
                dwyp = math.sqrt(float(math.pow(xps2 - x0,2)+math.pow((yps2 - y),2))) #x0 i y podąza między 2 i 0
                z0 = zf2 - dwyp * zprop20

            else: #gdy jest się między 1 a 2
                if dy21 != 0:
                    x1 = xps1 + (y-yps1) * dx21 / dy21
                else:
                    x1 = xps1
                if dy20 != 0:
                    x0 = xps0 + (y-yps0) * dx20 / dy20
                else:
                    x0 = xps2
                dwyp = math.sqrt(float(math.pow(xps2 - x1,2)+math.pow((yps2 - y),2))) #x1 i y podąza między 2 i 1
                z1 = zf2 - dwyp * zprop21
                dwyp = math.sqrt(float(math.pow(xps2 - x0,2)+math.pow((yps2 - y),2))) #x0 i y podąza między 2 i 0
                z0 = zf2 - dwyp * zprop20
            for x in range(x0, x1):
                if x >=0 and x < xw and y >=0 and y < yw: #ograniczenie tylko do obszaru ekranu
                    #screen.set_at((x, y), (0, 0, 0))
                    z = z1 - ((z1 - z0) / float(x1 - x0)) * float(x1 - x) 
                    pozpix = x + y * xw
                    if (z > bufram[pozpix] and z < zp): #zapisuje piksel tylko gdy jest blizej obserwatora niz pozostałe
                        screen.set_at((x, y), (kolortrojk))
                        bufram[pozpix] = z

    #pygame.display.flip()
    return bufram


def transformacja(x, y, z, krok):
    y = y - 200.0
    #wzrostx = 0.03 * krok
    #wzrosty = 0.03 * krok
    #wzrostz = -0.02 * krok
    #x = x * (1 + wzrostx) #skalowanie w x
    #y = y * (1 + wzrosty) #skalowanie w y
    #z = z * (1 + wzrostz) #skalowanie w z

    katXY = 0.05 * krok #w radianach, obracanie wokół osi Z
    #x, y, z = obrotXY(x, y, z, katXY)

    katXZ = 0.05 * krok #w radianach, obracanie wokół osi Y
    x, y, z = obrotXZ(x, y, z, katXZ)

    katYZ = 0.05 * krok #w radianach, obracanie wokół osi X
    #x, y, z = obrotYZ(x, y, z, katYZ)

    #przesx = 0.05 * krok
    #przesy = 0.025 * krok
    #przesz = - 1.0 * krok
    #x = x + przesx  #przesuwanie w kierunku x
    #y = y + przesy  #przesuwanie w kierunku y
    #z = z + przesz #przesuwanie w kierunku z

    return x, y, z

def obrotXY(x, y, z, katXY):
    xt = x * math.cos(katXY) - y * math.sin(katXY) #konieczny import biblioteki math! pomocniczne zmienne, by nie uzywac nadpisanyc x, y, z
    yt = x * math.sin(katXY) + y * math.cos(katXY)
    zt = z
    return xt, yt, zt

def obrotXZ(x, y, z, katXZ):
    xt = x * math.cos(katXZ) + z * math.sin(katXZ)
    yt = y
    zt = -x * math.sin(katXZ) + z * math.cos(katXZ)
    return xt, yt, zt

def obrotYZ(x, y, z, katYZ):
    xt = x
    yt = y * math.cos(katYZ) - z * math.sin(katYZ)
    zt = y * math.sin(katYZ) + z * math.cos(katYZ)
    return xt, yt, zt 

def wnormal(wierz0, wierz1, wierz2): #kalkulacja wektora normalnego dla trójkąta
    normalny = [0.0, 0.0, 0.0]
    U = [wierz1[0] - wierz0[0], wierz1[1] - wierz0[1], wierz1[2] - wierz0[2]] #metoda http://www.opengl.org/wiki/Calculating_a_Surface_Normal
    V = [wierz2[0] - wierz0[0], wierz2[1] - wierz0[1], wierz2[2] - wierz0[2]]
    normalny[0] = U[1] * V[2] - U[2] * V[1]
    normalny[1] = U[2] * V[0] - U[0] * V[2]
    normalny[2] = U[0] * V[1] - U[1] * V[0]
    return normalny

def coswekt(wekt0, wekt1): #obliczenie cosinusa miedzy wektorami http://www.mathsisfun.com/algebra/vectors-dot-product.html
    wektdlug0 = math.sqrt((math.pow(wekt0[0], 2) + math.pow(wekt0[1], 2) + math.pow(wekt0[2], 2))) #obliczenie długości wektora 
    wektdlug1 = math.sqrt((math.pow(wekt1[0], 2) + math.pow(wekt1[1], 2) + math.pow(wekt1[2], 2)))
    iloczynskal = (wekt0[0] * wekt1[0]) + (wekt0[1] * wekt1[1]) + (wekt0[2] * wekt1[2])
    coswektor = iloczynskal / (wektdlug0 * wektdlug1)
    return coswektor
 
def importujdane():
    #nazwa = "szescian.obj"
    nazwa = "crowbar.obj"
    #nazwa = "teapot.obj"
    plikmodelu = open(nazwa, "r").readlines()
    wierz = []
    trojk = []
    for linia in plikmodelu:
        lista_slow = linia.split()
        for slowo in lista_slow:
            if slowo == "v":
                x = float(lista_slow[1])
                y = float(lista_slow[2])
                z = float(lista_slow[3])
                wierz.append((x, y, z))
            if slowo == "f":
                t0 = int(lista_slow[1]) - 1
                t1 = int(lista_slow[2]) - 1
                t2 = int(lista_slow[3]) - 1
                ind  = 2
                #ind = random.randint(0, 2) #losowe kolory z tablicy kolorów
                trojk.append((t0, t1, t2, ind))
    print wierz
    print trojk  
    return wierz, trojk 

main()
