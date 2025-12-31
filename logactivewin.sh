#!/bin/bash

# Configuración
waittime="1"
LANG=en_US.utf8

mkdir -p logs
lasttitle=""

while true
do
    # 1. Llamar al script de Python dedicado
    curtitle=$(python3 get_window.py)
    
    # 2. Guardar solo si ha cambiado
    if [[ "$lasttitle" != "$curtitle" ]]; then
        T="$(date +%s)"
        logfile="logs/window_$(python3 rewind7am.py $T).txt"
        
        echo "$T $curtitle" >> $logfile
        echo "logged window: $(date) : $curtitle"
        lasttitle="$curtitle"
    fi

    sleep "$waittime"
done