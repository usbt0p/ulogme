#!/bin/bash

# Define cleanup function
cleanup() {
    echo "Stopping ulogme..."
    
    # 1. Creamos la señal de parada
    touch logs/ulogme.stop
    
    # 2. Esperamos un poco a que el hijo (root) la vea y se cierre
    echo "Waiting for keyfreq to finish current cycle..."
    
    if [ ! -z "$WIN_PID" ]; then
        kill $WIN_PID 2>/dev/null
    fi
    if [ ! -z "$SERVER_PID" ]; then
        kill $SERVER_PID 2>/dev/null
    fi
    exit
}

# Trap SIGINT (Ctrl+C) and SIGTERM
trap cleanup SIGINT SIGTERM

if [ "$(uname)" == "Darwin" ]; then
  # Mac (Assuming existing script works) but not updated since legacy
  ./osx/run_ulogme_osx.sh
else
  # Linux
  # create this to ensure permission
  if [ ! -d "logs" ]; then
    mkdir logs
  fi

  # 1. Start Keyfreq (requires sudo)
  figlet -w 60 -f future "Welcome to Ulogme" | cowsay -n
  echo ""
  echo "Starting Key Frequency Logger (requires sudo)..."
  echo "Alternatively, you might want to add"
  echo "tu_usuario ALL=(ALL) NOPASSWD: /home/tu_usuario/Programs/ulogme/keyfreq.sh" 
  echo "to your sudoers file to change this behaviour and autostart the script without password prompt."
  echo ""
  
  sudo ./keyfreq.sh &
  KEYFREQ_PID=$!

  sleep 5

  # 2. Start Active Window Logger
  echo "Starting Active Window Logger..."
  ./logactivewin.sh &
  WIN_PID=$!

  # 3. Start python server
  echo "Starting Server ..."
  python3 ulogme_serve.py
  SERVER_PID=$!

  echo "ulogme is running. Press Ctrl+C to stop."
  
  # Wait for processes to finish (or until we kill them)
  wait $WIN_PID $KEYFREQ_PID $SERVER_PID
fi

# nohup ./ulogme.sh > /dev/null 2>&1 &
