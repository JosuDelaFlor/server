#!/bin/bash
set -e

echo "=== Despliegue de Servidor Minecraft + Ngrok ==="

# Verifica si Docker está en ejecución
if ! docker info > /dev/null 2>&1; then
  echo "Error: Docker no está en ejecución. Por favor arranca el demonio de Docker."
  exit 1
fi

# Crea el archivo .env si no existe para evitar errores
if [ ! -f .env ]; then
    echo "[!] Archivo .env no encontrado. Creando una plantilla..."
    echo "NGROK_AUTHTOKEN=" > .env
    echo "DISCORD_WEBHOOK_URL=" >> .env
    echo "CHECK_INTERVAL=10" >> .env
    echo "Por favor, edita el archivo .env con tus credenciales y vuelve a ejecutar este script."
    exit 0
fi

# Levantar infraestructura
echo "[*] Construyendo y levantando contenedores (Graceful re-creation)..."
docker-compose up -d --build --remove-orphans

echo "[*] ¡Despliegue finalizado!"
echo "Estado de los contenedores:"
docker-compose ps