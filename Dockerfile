FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema necessárias para pdfplumber
RUN apt-get update && apt-get install -y \
    gcc \
    libpoppler-cpp-dev \
    libpoppler-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copiar aplicação (backend + frontend + parser)
COPY main.py .
COPY index.html .
COPY pdf_parser.py .

# Criar diretórios
RUN mkdir -p uploads reports static

# Expor porta
EXPOSE 8000

# Comando padrão
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
