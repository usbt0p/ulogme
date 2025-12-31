#!/bin/bash

# logs the active window titles over time. Logs are written 
# in logs/windowX.txt, where X is unix timestamp of 7am of the
# recording day. The logs are written if a window change event occurs
# (with 2 second frequency check time), or every 10 minutes if 
# no changes occur.

LANG=en_US.utf8

# Config
waittime="2" 
maxtime="600" 

mkdir -p logs
last_write="0"
lasttitle=""

# Function to check lock state via DBus (Modern Gnome/Ubuntu/Mint)
check_gnome_lock() {
    is_active=$(gdbus call --session --dest org.gnome.ScreenSaver --object-path /org/gnome/ScreenSaver --method org.gnome.ScreenSaver.GetActive 2>/dev/null)
    if [[ "$is_active" == *"(true,)"* ]]; then
        return 0 # Locked
    else
        return 1 # Unlocked
    fi
}

while true
do
    islocked=false

    # Try modern Gnome DBus check first
    if check_gnome_lock; then
        islocked=true
    else
        # Fallback for older systems or XScreensaver
        if command -v xscreensaver-command &> /dev/null; then
            if [[ $(xscreensaver-command -time) =~ "screen non-blanked" ]]; then 
                islocked=false
            else
                islocked=true
            fi
        fi
    fi

    if [ "$islocked" = true ]; then
        curtitle="__LOCKEDSCREEN"
    else 
        # Get Active Window Title
        # Warning: xdotool only works on X11, not Wayland
        id=$(xdotool getactivewindow 2>/dev/null)
        if [ -z "$id" ]; then
            curtitle="unknown"
        else
            curtitle=$(wmctrl -lpG | while read -a a; do w=${a[0]}; if (($((16#${w:2}))==id)) ; then echo "${a[@]:8}"; break; fi; done)
        fi
    fi

    perform_write=false

    # if window title changed, perform write
    if [[ "$lasttitle" != "$curtitle" ]]; then
        perform_write=true
    fi

    T="$(date +%s)"
    
    # Optional: Periodic write even if no change (uncomment to enable)
    # elapsed_seconds=$(expr $T - $last_write)
    # if [ $elapsed_seconds -ge $maxtime ]; then
    #    perform_write=true
    # fi

    if [ "$perform_write" = true ]; then 
        # Calculate file name based on 7AM logic using python script
        # Optimized: Only call python if we are actually writing
        logfile="logs/window_$(python3 rewind7am.py $T).txt"
        
        echo "$T $curtitle" >> $logfile
        echo "logged window: $(date) : $curtitle"
        last_write=$T
    fi

    lasttitle="$curtitle"
    sleep "$waittime"
done