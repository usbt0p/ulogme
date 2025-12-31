#!/usr/bin/python3
import subprocess
import json
import ast
import os
import sys

def get_dbus_env():
    """
    Intenta reconstruir el entorno DBus manualmente si falta.
    En Ubuntu/Systemd, el socket suele estar en /run/user/<UID>/bus
    """
    env = os.environ.copy()
    
    # Si la variable ya existe y parece válida, la usamos
    if env.get('DBUS_SESSION_BUS_ADDRESS'):
        return env

    # Si no, la forzamos usando el ID de usuario actual
    uid = os.getuid()
    socket_path = f"/run/user/{uid}/bus"
    
    if os.path.exists(socket_path):
        env['DBUS_SESSION_BUS_ADDRESS'] = f"unix:path={socket_path}"
    
    return env

def get_active_window():
    # Comando para pedir la lista de ventanas a la extensión
    cmd = [
        "gdbus", "call", "--session", 
        "--dest", "org.gnome.Shell", 
        "--object-path", "/org/gnome/Shell/Extensions/Windows", 
        "--method", "org.gnome.Shell.Extensions.Windows.List"
    ]

    try:
        # Obtenemos el entorno reparado
        my_env = get_dbus_env()

        # Ejecutamos el comando pasando explícitamente el entorno (env=my_env)
        output = subprocess.check_output(cmd, env=my_env).decode('utf-8').strip()
        
        if not output:
            # TODO this may be holding us back from knowing when we are in alt+tab
            return "__LOCKEDSCREEN"

        # Parseo seguro de la tupla de Python/GDBus
        # GDBus devuelve: ('[JSON]',)
        data_tuple = ast.literal_eval(output)
        json_str = data_tuple[0]
        windows = json.loads(json_str)
        
        # Buscar la ventana con foco
        for w in windows:
            if w.get('focus') is True:
                title = w.get('title')
                wm_class = w.get('wm_class')
                
                if title:
                    return title
                elif wm_class:
                    return wm_class
                else:
                    # TODO this should maybe be changed for lockscreen or whatever it is 
                    return "unknown"
        
        # TODO same as above todos
        return "__LOCKEDSCREEN"

    except Exception:
        # Si todo falla, devolvemos unknown silenciosamente
        return "unknown"

if __name__ == "__main__":
    # Imprimimos el resultado
    print(get_active_window())