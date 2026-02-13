counter-sspa
Questo repository contiene uno strumento automatizzato (Cellpose) per la segmentazione e il conteggio di colonie cellulari in immagini di saggi clonogenici.

Lo script run_analysis.py esegue le seguenti operazioni:
- Caricamento Modello IA: inizializza il modello pre-addestrato cyto di Cellpose ottimizzato per il riconoscimento cellulare.
- Pre-processing: converte le immagini in RGB e ottimizza il contrasto per migliorare la precisione della segmentazione.
- Segmentazione e conteggio: identifica ogni singola colonia presente nell'immagine e ne calcola il numero totale.
- Esportazione dati: genera un file .csv con i risultati numerici per ogni immagine analizzata.
- Visualizzazione: produce immagini di output con le maschere di segmentazione sovrapposte per validare visivamente il conteggio effettuato dall'IA.

Il test_counter.py (in tests/) verifica:
- test_model_loading: assicura che il modello Cellpose venga caricato correttamente in memoria.
- test_segmentation_logic: valida che la funzione di conteggio restituisca valori numerici coerenti.
- test_output_formats: verifica che lo script generi correttamente sia il file CSV che le immagini delle maschere.
- test_image_preprocessing: conferma che le utility di manipolazione dell'immagine non alterino i dati originali.

Come organizzare i dati:
Crea una cartella chiamata data nella root del progetto.
Inserisci le immagini da analizzare (formato .jpg, .png o .jpeg) direttamente nella cartella data.

Come eseguire l'analisi:
- Tramite Docker (Consigliato per riproducibilità):
docker build -t counter-sspa .
docker run --rm -v $(pwd)/data:/app/data -v $(pwd)/results:/app/results counter-sspa

- Tramite Google Colab (Per accelerazione GPU): è possibile utilizzare il file analysis.ipynb che permette di sfruttare la GPU gratuita di Google per velocizzare l'inferenza del modello.
    - Aprire il file analysis.ipynb in Colab.
    - Caricare le immagini in una cartella dedicata sul proprio Google Drive (es. SaggioClonogenico/input).
    - Il notebook clonerà il repository per importare la logica di conteggio da src/ e installerà le librerie necessarie.
    - I file generati verranno salvati direttamente su Drive nella cartella di output.
