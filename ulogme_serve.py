import socketserver
import http.server
import sys
import cgi
import os
import subprocess
import signal

# Assuming these files exist in your project
from export_events import update_events
from rewind7am import rewind_time

# Port settings
IP = ""
if len(sys.argv) > 1:
    PORT = int(sys.argv[1])
else:
    PORT = 8124

rootdir = os.getcwd()
try:
    os.chdir('render')
except FileNotFoundError:
    print("Error: 'render' directory not found.")
    sys.exit(1)

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type']}
        )
        result = 'NOT_UNDERSTOOD'

        if self.path == '/refresh':
            refresh_time = form.getvalue('time')
            os.chdir(rootdir)
            update_events()
            os.chdir('render')
            result = 'OK'

        if self.path == '/addnote':
            note = form.getvalue('note')
            note_time = form.getvalue('time')
            os.chdir(rootdir) 
            try:
                subprocess.run(
                    ['./note.sh', str(note_time)],
                    input=note.encode('utf-8'),
                    check=True
                )
            except Exception as e:
                print(f"Error executing note.sh: {e}")
                result = 'ERROR'
            update_events()
            os.chdir('render')
            result = 'OK'

        if self.path == '/blog':
            post = form.getvalue('post')
            if post is None: post = ''
            post_time = int(form.getvalue('time'))
            os.chdir(rootdir)
            
            # Ensure logs dir exists before writing
            os.makedirs('logs', exist_ok=True)
            
            with open(f'logs/blog_{post_time}.txt', 'w', encoding='utf-8') as f:
                f.write(post)
            update_events()
            os.chdir('render')
            result = 'OK'

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(result.encode('utf-8'))

# allow server reuse
class ReusableTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True 

httpd = ReusableTCPServer((IP, PORT), CustomHandler)

print(f'Serving ulogme on http://localhost:{PORT}')

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nShutting down server...")
    httpd.shutdown()
    httpd.server_close()