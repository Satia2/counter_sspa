import pytest
import numpy as np
import cv2
from src.counter import conta_colonie

# Creiamo una classe "finta" per simulare il modello Cellpose senza caricarlo davvero
class MockModel:
    def eval(self, img, **kwargs):
        # Restituisce una maschera vuota (zeri), flussi e stili
        return np.zeros(img.shape[:2], dtype=int), None, None

@pytest.fixture
def mock_model():
    return MockModel()

def test_immagine_vuota(mock_model):
    img_nera = np.zeros((100, 100, 3), dtype=np.uint8)
    n, _ = conta_colonie(img_nera, model_to_use=mock_model)
    assert n == 0

def test_formato_output(mock_model):
    img_random = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    n, masks = conta_colonie(img_random, model_to_use=mock_model)
    assert isinstance(n, int)
    assert masks.shape == (100, 100)

def test_rilevamento_colore_viola(mock_model):
    img = np.full((300, 300, 3), 255, dtype=np.uint8)
    cv2.circle(img, (150, 150), 20, (226, 43, 138), -1)
    # Passiamo il modello obbligatorio
    n, _ = conta_colonie(img, model_to_use=mock_model, diametro=21, area_minima=10)
    assert isinstance(n, int)