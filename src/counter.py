import numpy as np
from src.utils import pre_process_crystal_violet, crea_maschera_pozzetto

def conta_colonie(immagine_rgb, model_to_use, diametro=21, area_minima=50):
    """
    Analisi rapida: usa il modello già caricato in memoria.
    """
    # 1. Pre-processing (Miglioramento contrasto e grigio)
    img_gray = pre_process_crystal_violet(immagine_rgb)
    
    # 2. Taglio del pozzetto (Fondamentale per i riflessi!)
    img_final = crea_maschera_pozzetto(img_gray)
    
    # 3. Segmentazione ad alta sensibilità
    masks, flows, styles = model_to_use.eval(
        img_final, 
        diameter=21, 
        channels=[0, 0],
        flow_threshold=0.4,       # Accetta anche forme irregolari
        cellprob_threshold=-1.5   # Massima sensibilità per colonie sbiadite
    )
    
    # 4. Filtro Area
    unique_labels, counts = np.unique(masks, return_counts=True)
    labels_valide = unique_labels[(unique_labels > 0) & (counts >= area_minima)]
    mask_filtrata = np.isin(masks, labels_valide) * masks
    
    return len(labels_valide), mask_filtrata