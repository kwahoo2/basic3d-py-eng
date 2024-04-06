basic3d-py-eng
==============
Kolejne stadia prostego silnika 3D w Pythonie. Do tego w pliku PDF i HTML znajduje się komentarz. Silnik wyświetlający kolorowy sześcian/łom/czajnik (ewentualnie z cieniowaniem płaskim) działa całkowicie software'owo, bez OpenGL czy innych pomocniczych bibliotek, bo chodzi o ugryzienie podstaw. Całość nie jest zaawansowana, a wręcz bardzo uproszczona, tak by była zrozumiała dla jak najszerszego grona osób. Wymagania programowo-sprzętowe są opisane w plikach HTML i PDF. Nie polecam jednak kopiować listingów z tamtych plików (mogą nie działać), lepiej od razu uruchomić pliki PY. Pliczki PY:

1_pygametest.py – puste okno

2_multiprojekcjapygame.py – projekcja 2D wierzchołków sześcianu

3_krawprojekcjapygame.py – projekcja z krawędziami

4_trojkraster.py – rasteryzer trójkąta

5_raster-trans.py – projekcja całego sześcianu z rasteryzacją, uwzględnieniem głębokości obiektów (uwaga: wyliczenie Z bez zgodności z perspektywą) i transformacjami (obrót, skalowanie, przesunięcie)

eksp-eng-obj-import.py – j.w. z importem bryły z pliku obj

eksp-eng-shaded.py – j.w. z cieniowaniem płaskim 

Obrazek: ![Obrazek](https://github.com/kwahoo2/basic3d-py-eng/tree/master/basic3dengine/1_crowbar.png?raw=true)

Filmik: [![Filmik](https://img.youtube.com/vi/SpJZFgCjs_g/0.jpg)](https://www.youtube.com/watch?v=SpJZFgCjs_g)


##English

The creation stages of a simple 3D engine in Python. There is a commentary (unfortunately only in Polish at this moment) in the PDF and HTML file. The engine displaying a colored cube/crowbar/teapot (possibly with flat shading) runs entirely software, without OpenGL or other auxiliary libraries, as it's all about learning the basics. The whole thing is not advanced, in fact it's very simplified, so that it can be understood by the widest possible range of people. The software and hardware requirements are described in the HTML and PDF files. However, I do not recommend copying the listings from those files (they may not work), it is better to run the PY files right away. PY files:

1_pygametest.py - empty window

2_multiprojectionapygame.py - 2D projection of the vertices of the cube

3_krawprojekcjapygame.py - projection with edges

4_trojkraster.py - triangle rasterizer

5_raster-trans.py - projection of the entire cube with rasterization, consideration of object depth (note: Z calculation without perspective correctness) and transformations (rotation, scaling, translation)

eksp-eng-obj-import.py - as above, but with import of solid from obj file

eksp-eng-shaded.py - as above with flat shading
