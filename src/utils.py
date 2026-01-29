import cv2
import numpy as np

def crea_maschera_pozzetto(immagine, margine=0.9):
    """
    Crea un cerchio nero fuori dal pozzetto per evitare falsi positivi sui bordi.
    margine: 0.9 significa che tiene il 90% del raggio centrale.
    """
    h, w = immagine.shape[:2]
    centro = (w // 2, h // 2)
    raggio = int(min(h, w) * margine // 2)
    
    # Crea una maschera bianca
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, centro, raggio, 255, -1)
    
    # Applica la maschera all'immagine
    # Tutto ciò che è fuori dal cerchio diventa nero (o bianco se preferisci)
    immagine_mascherata = cv2.bitwise_and(immagine, immagine, mask=mask)
    return immagine_mascherata

def pre_process_crystal_violet(immagine_rgb):
    """
    Ottimizza l'immagine per il Crystal Violet.
    Estrae il canale verde per massimizzare il contrasto delle colonie viola.
    """
    # Se l'immagine ha 3 dimensioni (H, W, Canali)
    if len(immagine_rgb.shape) == 3:
        # Estraiamo il canale verde
        canale_verde = immagine_rgb[:, :, 1]
    else:
        # È già in scala di grigi
        canale_verde = immagine_rgb

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img_contrast = clahe.apply(canale_verde)
    
    return img_contrast