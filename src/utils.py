import cv2
import numpy as np

def crea_maschera_pozzetto(immagine, margine=0.85):
    """
    Crea un cerchio nero fuori dal pozzetto per evitare falsi positivi sui bordi.
    margine: 0.88 è il valore ideale per tagliare i riflessi della plastica 
    senza sacrificare le colonie periferiche.
    """
    h, w = immagine.shape[:2]
    
    # Calcoliamo il centro e il raggio
    centro = (w // 2, h // 2)
    # Usiamo un margine leggermente più stretto per escludere la curvatura della plastica
    raggio = int(min(h, w) * margine // 2)
    
    # Creiamo una maschera nera
    mask = np.zeros((h, w), dtype=np.uint8)
    
    # Disegniamo il cerchio bianco (zona da tenere)
    cv2.circle(mask, centro, raggio, 255, -1)
    
    # Applica la maschera all'immagine
    # Tutto ciò che è fuori dal cerchio diventa nero
    immagine_mascherata = cv2.bitwise_and(immagine, immagine, mask=mask)
    
    return immagine_mascherata

def pre_process_crystal_violet(immagine_rgb):
    """
    Ottimizza l'immagine per il Crystal Violet.
    L'estrazione del canale verde è perfetta perché il viola (complementare)
    appare quasi nero, creando il massimo contrasto possibile.
    """
    if len(immagine_rgb.shape) == 3:
        # Il canale verde (indice 1) è il migliore per il Crystal Violet
        canale_verde = immagine_rgb[:, :, 1]
    else:
        canale_verde = immagine_rgb

    # Invertiamo l'immagine se necessario (Cellpose preferisce oggetti chiari su fondo scuro 
    # o viceversa a seconda del modello, ma con 'cyto' e Crystal Violet, il contrasto 
    # creato dal CLAHE è solitamente sufficiente).
    
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8)) # Aumentato leggermente clipLimit
    img_contrast = clahe.apply(canale_verde)
    
    return img_contrast