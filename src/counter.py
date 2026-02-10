import numpy as np
import torch
from cellpose import models
from src.utils import pre_process_crystal_violet, crea_maschera_pozzetto

# --- OTTIMIZZAZIONE VELOCITÀ ---
# Inizializziamo il modello fuori dalla funzione così viene caricato 
# in memoria una sola volta all'avvio del programma/notebook.
_usa_gpu = torch.cuda.is_available()
_model_cache = models.CellposeModel(model_type='cyto', gpu=_usa_gpu)

def conta_colonie(immagine_rgb, diametro=21, area_minima=50):
    """
    Esegue il conteggio delle colonie usando Cellpose.
    Parametri aggiornati per alta sensibilità:
    - area_minima: abbassata a 50 per includere colonie puntiformi.
    - cellprob_threshold: impostata a -2.0 per rilevare colonie sbiadite.
    """
    
    # 1. Pre-processing
    img_gray = pre_process_crystal_violet(immagine_rgb)
    img_final = crea_maschera_pozzetto(img_gray)
    
    # 2. Segmentazione (Alta Sensibilità)
    # Usiamo il modello pre-caricato invece di inizializzarne uno nuovo ogni volta
    masks, flows, styles = _model_cache.eval(
        img_final, 
        diameter=21, 
        channels=[0, 0],
        flow_threshold=0.8,      # Più tollerante sulle forme irregolari
        cellprob_threshold=-4.0  # Molto più sensibile al segnale debole
    )
    
    # 3. Filtro Area
    # Recuperiamo le label degli oggetti che superano la soglia minima
    unique_labels, counts = np.unique(masks, return_counts=True)
    
    # Escludiamo lo sfondo (label 0) e filtriamo per area
    labels_valide = unique_labels[(unique_labels > 0) & (counts >= area_minima)]
    
    # Creiamo la maschera finale contenente solo le colonie approvate
    mask_filtrata = np.isin(masks, labels_valide) * masks
    
    return len(labels_valide), mask_filtrata