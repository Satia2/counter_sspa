# 1. Usiamo un'immagine Python ufficiale e leggera
FROM python:3.9-slim

# 2. Impostiamo variabili d'ambiente per evitare file .pyc e bufferizzazione log
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Installiamo le dipendenze di sistema necessarie per OpenCV
# libgl1 e libglib2.0 sono fondamentali per far girare cv2 in Docker
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# 4. Creiamo la directory di lavoro
WORKDIR /app

# 5. Copiamo e installiamo i requisiti prima del resto (ottimizza la cache di Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiamo tutto il resto del progetto
COPY . .

# 7. Definiamo il PYTHONPATH in modo che pytest e gli script trovino la cartella src
ENV PYTHONPATH=/app

# 8. Comando di default: esegue i test
# Se vorrai usare questo Docker per l'analisi, potrai sovrascrivere il comando
CMD ["pytest", "tests/"]