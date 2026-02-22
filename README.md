
# ulogme

Este es mi fork personal de [ulogme](https://github.com/karpathy/ulogme). Es un muy buen proyecto, pero al no estar mantenido desde 2016 era inutilizable en sistemas modernos (Ubuntu 24.04 con x11 + Python > 2 en mi caso). Más abajo tienes el [README original](#original-readme).

He modernizado la parte de Python para funcionar con Python 3.12 (quizas más) y también los scripts de shell para gestionar logging de teclas y de ventanas, y he mejorado (o a mi me lo parece al menos) la interfaz de usuario. Eso si, la parte de OSX no la he tocado y no tengo pensado así que no creo que funcione.

> [!NOTE]
> Esto es un proyecto personal que en gran parte he vibecodeado, así que no esperes gran documentación, ni que funcione en todos los sistemas (estoy bastante seguro de que ahora mismo solo funciona en el mío correctamente). Además, el código no es de mucha calidad, concretamente el de JS, html y css, ya que no se programar en ninguno y lo vibecodeé a muerte.
> Aún así, si quieres contribuir, no dudes en hacerlo y en escribirme o abrir un issue.

## Updates con respecto al original
> Para referencia futura, en el "backend":

    Muchas cosas porteadas de Python2 a Python3, librerias actualizadas, estilo de codigo adaptado.

    Objetivo de funcionamiento en entorno: Ubuntu con X11.

    Extensión GNOME: "Window Calls" (activada y funcionando en /org/gnome/Shell/Extensions/Windows) en vez de los comandos originales. 
    Menos flexible pero funciona en X11. esta es la dependencia grande del proyecto.

    ulogme.sh: Se ejecuta como usuario normal. Lanza keyfreq con sudo y logactivewin sin sudo para evitar problemas de loggeo de ventanas para root.

    logactivewin.sh: Llama a un script auxiliar de Python (get_window.py). Una especie de "capa de compatibilidad"

    get_window.py: Usa gdbus para consultar la extensión y ast.literal_eval para parsear la respuesta sin errores.

    ulogme.sh: sistema de cleanup para ctrl+c, autoinicio del servidor, centinel file para ctrl+c

    keyfreq.sh: sistema de cleanup para ctrl+c, centinel file para ctrl+c, cambios en la logica de espera y del bucle para que funcione el centinel file

> En el front:

    Añadir parametros de url para eliminar el cache y poder desarrollar bien.

    Evitar problemas con NaN's en las pie charts, y con desaparicion de keyfreqs en las overviews.

    cuando no hay keyfreqs (suspension) no se plottean

    revamped UI toda vibecodeada eso si

> Automatizaciones:

    Añadido el archivo .desktop junto con permisos en visudo para keyfreq.sh. Esto permite autostart del programa.

	[Desktop Entry]
	Type=Application
	Name=Ulogme
	Exec=/home/.../ulogme/ulogme.sh
	Path=/home/.../ulogme
	Terminal=false
	X-GNOME-Autostart-enabled=true

## TODOs

- [ ] trabajando en escritorio remoto hay bugs (no se logean las teclas, se duplican los eventos???)
- [ ] arreglar el blog, que no funciona
- [ ] hacer que al iniciar el server o recargar se calcule el dia de hoy (ahora no funciona) y te lleve a el directamente
- [x] mejorar el script de inicio: 
	- [x] que no te pida la contraseña o al menos no al cerrar
	- [x] que se pueda lanzar auto con el bashrc o cron, o un .desktop
	- [x] que se pueda lanzar en background 
- [ ] hacer que los ficherosn pasen a ser una base de datos rollo un sqlite. con ventanas mejores se podria hacer un filter y darselos a una llm
- [ ] mejor obtencion de las ventanas: sacar nombre de aplicacion y subnombres de pestañas, etc. Mirar en el repo de newlogme
- [ ] convertir los logs en una base de datos de series temporales simple, por un lado los textos y por otro los keyfreqs
- [ ] permitir dormir el programa, o suspender sin que siga trackeando
- [ ] permitir que pare de trackear si la pantalla se ha apagado (y vuelva a iniciar cuando se encienda)
- [ ] FIX: algunos de los nombres de ventana son poco informativos: un subreddit no dice que es reddit, el navegador der archivos solo pone el nombre de la carpeta... encontrar un mejor sistema para los nombres de las ventanas, o en su defecto usar python??? 
- [ ] Arreglar el problema de __LOCKSCREEN al usar alt+tab y super key (win key)
- [ ] Arreglar el problema de unknown cuando se entra en suspension
- [ ] Arreglar el problema de los NaN's en los pie charts
- [x] FIX : al hacer hover sobre las actividades de la vista de un día, el texto de detalle se sale de la pantalla en las actividades muy a la derecha
- [x] añadir un script para hacer que se inicie automáticamente ulogme y se sirva el servidor cada vez que se inicia el ordenador 
- [ ] añadir un script para pararlo correctamente (al iniciar en background con .desktop `kill` simple no funciona)
- [ ] hacer un sistema para añadir elementos sin categorizar (otros) a categorías (con gui??)
- [ ] usar una extensión rollo activity wathch para loggear firefox con detalle o visual studio con detalle

---

# Original README

### How productive were you today? How much code have you written? Where did your time go?

Keep track of your computer activity throughout the day: visualize your active window titles and the number of keystrokes in beautiful HTML timelines. Current features:

- Records your **active window** title throughout the day
- Records the **frequency of key presses** throughout the day
- Record custom **note annotations** for particular times of day, or for day in general
- Everything runs **completely locally**: none of your data is uploaded anywhere
- **Beautiful, customizable UI** in HTML/CSS/JS (d3js).

The project currently **only works on Ubuntu and OSX**, and uses new fancy **Promises** feature of ECMAScript 6. This might not be implemented in all browsers. My Chrome has it, but for example my Firefox doesn't.

## Demo

See a blog post (along with multiple screenshots) describing the project [here.](http://karpathy.github.io/2014/08/03/quantifying-productivity/)

## Getting Started

**To start recording**

1. Clone the repository to some folder: `$ git clone https://github.com/karpathy/ulogme.git`
2. If you're on Ubuntu, make sure you have the dependencies: `$ sudo apt-get install xdotool wmctrl`. On Fedora, you may also need `sudo yum install gnome-screensaver`.

TODO cambiar esto y avisar de la dependencia de python3 y de [la extension de Gnome window calls](https://github.com/ickyicky/window-calls) en ububntu.

3. `cd` inside and run `$ ./ulogme.sh` (note: this will ask you for sudo authentication which is required for `showkey` command). This will launch two scripts. One records the frequency of keystrokes and the other records active window titles. Both write their logs into log files in the `logs/` directory. Every log file is very simply just the unix time stamp followed by data, one per line.
4. For **OSX** only: there might be an additional step where you have to go to System Preferences > Security & Privacy > Accessibility, and make sure that Terminal (or iTerm2, or whatever you use to launch ulogme) is checked. If it wasn't checked previously and you just checked it, you may need to restart ulogme. If you don't do this step, you might find that window logging works but keypress logging doesn't.

**The user interface**

1. **Important**. As a one-time setup, copy over the example settings file to your own copy: `$ cp render/render_settings_example.js render/render_settings.js` to create your own `render_settings.js` settings file. In this file modify everything to your own preferences. Follow the provided example to specify title mappings: A raw window title comes in, and we match it against regular expressions to determine what type of activity it is. For example, the code would convert "Google Chrome - some cool website" into just "Google Chrome". Follow the provided example and read the comments for all settings in the file.
2. Once that's set up, start the web server viewer: `$ python ulogme_serve.py`, and go to to the provided address) for example `http://localhost:8123`) in your browser. Hit the refresh button on top right every time you'd like to refresh the results based on most recently recorded activity
3. If your data isn't loading, try to explicitly run `python export_events.py` and then hit refresh. This should only be an issue the very first time you run ulogme.

## User Interface

The user interface can switch between a single day view and an overview view by link on top. You have to hit the refresh button every time you'd like to pull in new data.

#### Single day page

- You can enter a reminder "blog" on top if you'd like to summarize the day for yourself or enter other memos.
- Click on any bar in the *barcode view* to enter a custom (short) note snippet for the time when the selected activity began. I use this to mark meetings, track my coffee/food intake, sleep time, or my total time spent running/swimming/gym or to leave notes for certain patterns of activity, etc. These could all later be correlated with various measures of productivity, in future.

#### Overview page

- You can click the window titles to toggle them on and off from the visualization 
- Clicking on the vertical bars takes you to the full statistics for that day.

## Known issues
- One Ubuntu user reported broken view with no data. On further inspection we found that the logs were corrupt. One of the lines in a file in `/logs` was, instead of looking as `{timestamp} {data}`  looked as `@@@@@@@{timestamp} {data}`, in other words an odd character was appended to the timestamp somehow. We manually erased these characters from the log file to fix the issue.
- Legacy code note: if you used ulogme from before 28 July, you will have to run `$ python legacy_split_events.py` to convert your events files, once.
- You may see *"address already in use"* if you try to run `python ulogme_serve.py`. Sometimes the system can get confused and takes a while to update what ports are being used. Use the optional argument to specify a different port, for example `python ulogme_serve.py 8124` and then go to `http://localhost:8124` instead, for example.
- Overview page is blank. Are you sure your browser supports ECMAScript 6? Chrome should be fine, Firefox might not be, yet. 

## Contributing

The Ubuntu and OSX code base are a little separate on the data collection side. However, they each just record very simple log files in `/logs`. Once the log files are written, `export_events.py` takes the log files, does some simple processing and writes the results into `.json` files in `/render`. The Javascript/HTML/CSS UI codebase is all common and all lives in `/render`.

### Ubuntu
ulogme has three main parts: 

1. Recording scripts `keyfreq.sh` and `logactivewin.sh`. You probably won't touch these.
2. Webserver: `ulogme_serve.py` which wraps Python's `SimpleHTTPServer` and does some basic communication with the UI. For example, the UI can ask the server to write a note to a log file, or for a refresh.
3. The UI. Majority of the codebase is here, reading the `.json` files in `/render` and creating the visualizations. There are several common `.js` files, and crucially the `index.html` and `overview.html` files. I expect that most people might be able to contribute here to add features/cleanup/bugfix.

### OSX code
Things get a little ugly in OSX if you want to change anything with recording the log files because you have to recompile these portions any time you make any changes. It's ugly and it had to be done. However, if you're only interested in hacking with the UI, just change Javascript in `render` and no recompile is necessary, naturally.

## Related projects

* [selfspy](https://github.com/gurgeh/selfspy), Log everything you do on the computer, for statistics, future reference and all-around fun.
* [arbtt](http://freecode.com/projects/arbtt), automatic rule-based time tracker.

For more projects, [this question on Personal Productivity Stack Exchange](https://productivity.stackexchange.com/questions/13913/automatic-time-tracking-software-for-computer-work-for-windows-linux-mac) might be also worth a look.

## License
MIT
