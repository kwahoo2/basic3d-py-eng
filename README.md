basic3d-py-eng
==============
Kolejne stadia prostego silnika 3D w Pythonie. Do tego w pliku PDF i HTML znajduje się komentarz. Silnik wyświetlający kolorowy sześcian/łom/czajnik (ewentualnie z cieniowaniem płaskim) działa całkowicie software'owo, bez OpenGL czy innych pomocniczych bibliotek, bo chodzi o ugryzienie podstaw. Całość nie jest zaawansowana, a wręcz bardzo uproszczona, tak by była zrozumiała dla jak najszerszego grona osób. Wymagania programowo-sprzętowe są opisane w plikach HTML i PDF. Nie polecam jednak kopiować listingów z tamtych plików (mogą nie działać), lepiej od razu uruchomić pliki PY. Pliczki PY:

1_pygametest.py – puste okno

2_multiprojekcjapygame.py – projekcja 2D wierzchołków sześcianu

3_krawprojekcjapygame.py – projekcja z krawędziami

4_trojkraster.py – rasteryzer trójkąta

5_raster-trans.py – projekcja całego sześcianu z rasteryzacją, uwzględnieniem głębokości obiektów (uwaga: wyliczenie Z bez zgodności z perspektywą) i transformacjami (obrót, skalowanie, przesunięcie – nieopisane w PDF)

eksp-eng-obj-import.py – j.w. z importem bryły z pliku obj – nieopisany w PDF

eksp-eng-shaded.py – j.w. z cieniowaniem płaskim – nieopisany w PDF
