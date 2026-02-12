import os
import cv2
import pandas as pd
from cellpose import models
from src.counter import conta_colonie

def main():
    input_dir = "data"
    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)
    
    model = models.Cellpose(gpu=False, model_type='cyto')
    
    results = []
    
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    print(f"Trovate {len(image_files)} immagini. Inizio analisi...")
    
    for filename in image_files:
        path = os.path.join(input_dir, filename)
        img = cv2.imread(path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        count, mask = conta_colonie(img_rgb, model)
        
        results.append({"filename": filename, "count": count})
        print(f"Analizzata {filename}: {count} colonie trovate.")
        
        cv2.imwrite(os.path.join(output_dir, f"mask_{filename}"), (mask > 0).astype(int) * 255)

    df = pd.DataFrame(results)
    df.to_csv(os.path.join(output_dir, "counts.csv"), index=False)
    print(f"\nAnalisi completata! Risultati salvati in {output_dir}/counts.csv")

if __name__ == "__main__":
    main()