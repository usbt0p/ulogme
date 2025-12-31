#!/bin/bash

# Define cleanup function
cleanup() {
    echo "Stopping ulogme..."
    if [ ! -z "$KEYFREQ_PID" ]; then
        sudo kill $KEYFREQ_PID 2>/dev/null
    fi
    if [ ! -z "$WIN_PID" ]; then
        kill $WIN_PID 2>/dev/null
    fi
    exit
}

# Trap SIGINT (Ctrl+C) and SIGTERM
trap cleanup SIGINT SIGTERM

if [ "$(uname)" == "Darwin" ]; then
  # Mac (Assuming existing script works)
  ./osx/run_ulogme_osx.sh
else
  # Linux
  # create this to ensure permission
  if [ ! -d "logs" ]; then
    mkdir logs
  fi

  # 1. Start Keyfreq (requires sudo)
  echo "Starting Key Frequency Logger (requires sudo)..."
  sudo ./keyfreq.sh &
  KEYFREQ_PID=$!
  
  # 2. Start Active Window Logger
  echo "Starting Active Window Logger..."
  ./logactivewin.sh &
  WIN_PID=$!

  echo "ulogme is running. Press Ctrl+C to stop."
  
  # Wait for processes to finish (or until we kill them)
  wait $WIN_PID $KEYFREQ_PID
fi