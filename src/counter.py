import numpy as np
from cellpose import models
from src.utils import pre_process_crystal_violet, crea_maschera_pozzetto

def conta_colonie(immagine_rgb, diametro=21, area_minima=272):
    """
    Logica calibrata: 50 cellule = ~272 pixel, diametro medio = 21 pixel.
    """
    # 1. Pre-processing per Crystal Violet
    img_gray = pre_process_crystal_violet(immagine_rgb)
    
    # 2. Mascheramento bordi pozzetto
    img_final = crea_maschera_pozzetto(img_gray)
    
    # 3. Modello Cellpose (gpu=False per compatibilità locale, lo cambieremo in Colab)
    model = models.Cellpose(model_type='cyto', gpu=False)
    
    # Segmentazione
    masks, flows, styles, diams = model.eval(
        img_final, 
        diameter=diametro, 
        channels=[0, 0],
        flow_threshold=0.4,
        cellprob_threshold=0.0
    )
    
    # 4. Filtro Area (Criterio 50 cellule)
    labels_valide = [l for l in range(1, masks.max() + 1) if np.sum(masks == l) >= area_minima]
    
    # Creazione maschera filtrata per visualizzazione
    mask_filtrata = np.isin(masks, labels_valide) * masks
    
    return len(labels_valide), mask_filtrata