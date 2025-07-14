#!/bin/bash

# Rango de ejecución (mañana o tarde)
PERIODO=$1  # "morning" o "afternoon"

if [ "$PERIODO" = "morning" ]; then
  # Rango 8:50 a 9:10 (en minutos desde medianoche: 530 a 550)
  MIN_START=530
  MIN_END=550
elif [ "$PERIODO" = "afternoon" ]; then
  # Rango 13:55 a 14:30 (en minutos desde medianoche: 835 a 870)
  MIN_START=835
  MIN_END=870
else
  echo "Uso: $0 [morning|afternoon]"
  exit 1
fi

# Tiempo aleatorio dentro del rango
RANDOM_MIN=$(shuf -i $MIN_START-$MIN_END -n 1)

# Convierte a formato HH:MM
HOUR=$((RANDOM_MIN / 60))
MINUTE=$((RANDOM_MIN % 60))
TIME_FORMATTED=$(printf "%02d:%02d" $HOUR $MINUTE)

echo "Esperando hasta $TIME_FORMATTED para ejecutar el script..."

# Espera hasta la hora aleatoria
NOW=$(date +%s)
TARGET=$(date -d "$TIME_FORMATTED" +%s)
SLEEP_TIME=$((TARGET - NOW))

if [ $SLEEP_TIME -gt 0 ]; then
  sleep $SLEEP_TIME
fi

# Activa entorno virtual y ejecuta script
cd ~/Projects/odoo-assistance
source venv/bin/activate
python main.py
