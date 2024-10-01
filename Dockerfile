# Verwende ein offizielles Python-Image als Basis
FROM python:3.9-slim

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die requirements.txt in den Container
COPY requirements.txt .

# Installiere die Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# # Pytest installieren (für Testzwecke)
RUN pip install pytest

# Kopiere den Rest der App in den Container
COPY app/ /app
COPY run.py /app

# Setze die Umgebungsvariablen für Flask
ENV FLASK_APP=run.py
ENV FLASK_ENV=development  

# Exponiere den Port 5000 für Flask
EXPOSE 5000

# Standardkommando für den Start der App
CMD ["flask", "run", "--host=0.0.0.0"]

# Optional: Für Testzwecke (uncomment if needed)
# COPY wait-for-it.sh /wait-for-it.sh
# ENTRYPOINT ["./wait-for-it.sh", "db:3306", "--", "pytest"]
