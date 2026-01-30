import numpy as np
from cellpose import models
from src.utils import pre_process_crystal_violet, crea_maschera_pozzetto

def conta_colonie(immagine_rgb, diametro=21, area_minima=272):
    # 1. Pre-processing
    img_gray = pre_process_crystal_violet(immagine_rgb)
    img_final = crea_maschera_pozzetto(img_gray)
    
    # 2. Caricamento modello (Uso di CellposeModel per maggiore stabilità)
    model = models.CellposeModel(model_type='cyto', gpu=False)
    
    # 3. Segmentazione
    # CellposeModel.eval restituisce: masks, flows, styles
    masks, flows, styles = model.eval(
        img_final, 
        diameter=diametro, 
        channels=[0, 0],
        flow_threshold=0.4,
        cellprob_threshold=0.0
    )
    
    # 4. Filtro Area
    labels_valide = [l for l in range(1, masks.max() + 1) if np.sum(masks == l) >= area_minima]
    mask_filtrata = np.isin(masks, labels_valide) * masks
    
    return len(labels_valide), mask_filtrata