#!/bin/bash


# logs the key press frequency over 9 second window. Logs are written 
# in logs/keyfreqX.txt every 9 seconds, where X is unix timestamp of 7am of the
# recording day.

LANG=en_US.utf8
helperfile="logs/keyfreqraw.txt" # temporary helper file
stopfile="logs/ulogme.stop"  # Definimos el archivo señal
mkdir -p logs

# Aseguramos que no existe señal vieja al arrancar
rm -f $stopfile

while true
do

  # 1. Comprobar si me han pedido parar ANTES de empezar el trabajo
  if [ -f "$stopfile" ]; then
      echo "Stop signal detected. Exiting..."
      rm -f $stopfile  # Limpiamos
      exit 0
  fi

  showkey > $helperfile &
  PID=$!
  
  # 2. Esperar 9 segundos (o salir antes si aparece el archivo)
  # Usamos un bucle de espera para responder rápido al Ctrl+C
  for i in {1..9}; do
      sleep 1
      if [ -f "$stopfile" ]; then
          kill $PID 2>/dev/null
          rm -f $stopfile
          exit 0
      fi
  done

  kill $PID 2>/dev/null
  
  # count number of key release events
  num=$(cat $helperfile | grep release | wc -l)
  
  # append unix time stamp and the number into file
  logfile="logs/keyfreq_$(python3 rewind7am.py).txt"
  echo "$(date +%s) $num"  >> $logfile
  echo "logged key frequency: $(date) $num release events detected into $logfile"
  
done
