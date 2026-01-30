import numpy as np
import pytest
import cv2  # <--- FONDAMENTALE

from src.counter import conta_colonie

def test_immagine_vuota():
    # Creiamo un'immagine 3D (100x100x3)
    img_nera = np.zeros((100, 100, 3), dtype=np.uint8)
    n, _ = conta_colonie(img_nera)
    assert n == 0

def test_formato_output():
    img_random = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    n, masks = conta_colonie(img_random)
    assert isinstance(n, int)
    assert masks.shape == (100, 100)

def test_rilevamento_colore_viola():
    img = np.full((300, 300, 3), 255, dtype=np.uint8)
    # Cerchio viola (Crystal Violet sim)
    cv2.circle(img, (150, 150), 20, (226, 43, 138), -1) 
    
    # Testiamo che il codice arrivi alla fine senza errori
    n, _ = conta_colonie(img, diametro=21, area_minima=10)
    assert isinstance(n, int)