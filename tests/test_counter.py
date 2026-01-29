import numpy as np
import pytest
from src.counter import conta_colonie

def test_immagine_vuota():
    # Crea un'immagine completamente nera 100x100
    img_nera = np.zeros((100, 100), dtype=np.uint8)
    # Dovrebbe contare zero colonie
    n, _ = conta_colonie(img_nera)
    assert n == 0

def test_formato_output():
    img_random = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
    n, masks = conta_colonie(img_random)
    # Verifica che n sia un numero e masks una matrice
    assert isinstance(n, int)
    assert masks.shape == (100, 100)

def test_rilevamento_colore_viola():
    # Crea un'immagine RGB con un cerchio viola (Crystal Violet sim)
    img = np.full((300, 300, 3), 255, dtype=np.uint8)
    # Viola: R=138, G=43, B=226
    cv2.circle(img, (150, 150), 20, (226, 43, 138), -1) 
    
    # Eseguiamo il conteggio con area minima piccola per il test
    n, _, _ = conta_colonie(img, diametro=40, area_minima=50)
    
    assert n == 1, f"Dovrebbe trovare 1 colonia, ne ha trovate {n}"