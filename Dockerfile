FROM python:3.11-slim

# Instalar dependências de compilação
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar o arquivo de dependências
COPY requirements.txt .

# Atualizar pip
RUN pip install --upgrade pip

# Instalar as dependências do requirements.txt
RUN pip install -r requirements.txt

# Copiar o restante dos arquivos da aplicação
COPY . /app/

EXPOSE 5000

CMD ["python", "myindex.py"]