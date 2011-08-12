==================================================
 Un entorno de producción para un proyecto Django
==================================================

:Autrhors:
	"Jesús Gómez" <jgomez@funfisis.gob.ve>

:Version: 1.0 11/08/2011

- Intorducción El proyecto *Django* específico usado en este texto es
  sismocaracas_
  
  - Producción es solo una PC en la oficina.
  - Explicación de primero en una máquina virtual y luego en
    producción.
  - Un solo apache porque a futuro se migrará a Rails.

.. _sismocaracas: http://code.funvisis.gob.ve/sismocaracas/

Especificaciones técnicas
=========================

- Fedora 14
- Python 2.7...
- Django 1.3
- Apache 2...
- mod-wsgi...
- Postgres...

Preparación
===========

Software
--------

Empezaremos con instalar todo el software de terceros que necesita
nuestro proyecto.

*Python 2.7* ya viene instalado por omisión en *Fedora 14*.

Podemos instalar las versiones del gestor de paquetes de *Fedora 14* de
Apache, mod-wsgi y Postgres. Para ello, basta con::

    $ yum install apache postgres mod-wsgi

*mod-wsgi* le da soporte a Apache del estandar wsgi_ de *Python*

.. _wsgi: http://www.python.org/dev/peps/pep-0333/

Para instalar Django, prefiero usar el sistem de paquetes de Python
que el del sistema operativo. El gestor de paquetes de Python que
prefiero es *pip*, y para usarlo debemos instalar a través de *yum* el
paquete *dist-utils* que nos da el comando *easy_intall* con el que
instalaremos *pip*. Entonces, procedemos::

    $ yum install python-dist-utils
    $ easy_install pip
    $ pip install django

Configuración inicial - web
---------------------------

*Django* no hace nada al especial cuando le hacen una petición que
termine en algúna extención; es indiferente para él si termina en
*.html*, en *.php* o en *.jpeg*. Para *Django* una petición es solo
eso y la delega a la [vista]_ adecuada. Por lo tanto, el conenido
estático de un proyecto (páginas *html* estáticas, imágenes, videos,
*css*, *javascrip*, etc) no es servido a través de *Django* sino de un
servidor web separado dedicado a esta tarea.

.. [vista] En *Django*, cada petición es analizada por un *enrutador*
   quien delega la acción a tomar a una *vista* en función de la
   *url*. La palabra *vista* puede confundir por eso, ya que no es más
   que un *manejador*.

Aunque lo ideal sería tener al menos dos servidores web serparados en
máquinas distintas (por ejemplo, una máquina especializada en *I/O* o
entrada y salida para servir el contenido estático, y otro
especializado en *cómputo* para ejecutar el código Django) en este
ambiente usaremos el mismo servidor *Apache* para responder tanto a
las peticiones por contenido estático como a las peticiones por
contenido dinámico. Para lograr esto, le configuramos dos host
virtules, uno que llamaremos *static*, y otro que llamaremos
*dyn*. Esto se logra creando un archivo ``.conf`` por cada host
virtual en el directorio ``/etc/httpd/vhost.d/``. A continuación, la
configuración utilizada.

``static.conf``::

    <VirtualHost *:80>
    
    	ServerAdmin webmaster@funvisis.gob.ve
	ServerName staic.funvisis.gob.ve
	ServerAlias static

    	DocumentRoot /var/www
    
    	<Directory />
    		Options FollowSymLinks
    		AllowOverride None
    	</Directory>
    
    	<Directory /var/www/>
    		Options Indexes FollowSymLinks MultiViews
    		AllowOverride None
    		Order allow,deny
    		allow from all
    	</Directory>
    
    	ErrorLog ${APACHE_LOG_DIR}/static.error.log
    	LogLevel warn
    	CustomLog ${APACHE_LOG_DIR}/static.access.log combined
    
    </VirtualHost>

``dyn.conf``::

    <VirtualHost *:80>
    	ServerAdmin webmaster@funvisis.gob.ve
    	ServerName dyn.funvisis.gob.ve
    	ServerAlias dyn
    
    	WSGIDaemonProcess dyn.funvisis.gob.ve processes=2 threads=15 display-name=%{GROUP}
    	WSGIProcessGroup funvisis.gob.ve
    	WSGIScriptAlias /sismocaracas /usr/lib/wsgi-scripts/sismocaracas.wsgi
    
    	ErrorLog ${APACHE_LOG_DIR}/error_dyn.log
    	LogLevel warn
    	CustomLog ${APACHE_LOG_DIR}/access_dyn.log combined
    </VirtualHost>

Con esta configuración estamos declarando que:

- el contenido estático será servido cuando la url de la petición
  contenga a ``static.funvisis.gob.ve`` o a ``static`` como ``host``,
  y la raíz del directorio desde donde se obtendrá el contenido
  estático será ``/var/www/`` en el servidor.
- el contenido dinámico será servido cuando la url de la petición
  contenga a ``dyn.funvisis.gob.ve`` o ``dyn`` como host, y que por
  ahora solo hay una aplicación ubicada en el servidor en
  ``/usr/lib/wsgi-scripts/sismocaracas.wsgi`` y que se activará si la
  parte de la ruta del url empieza con ``/sismocaracas``

Ahora, dedicaremos un directorio dentro de ``/var/www/`` por cada proyecto para que coloquen en él el contenido estático específico a él. Entonces::

    $ mkdir /var/www/sismocaracas

