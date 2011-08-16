==================================================
 Un entorno de producción para un proyecto Django
==================================================

:Autrhors:
	"Jesús Gómez" <jgomez@funfisis.gob.ve>

:Version: 1.1 15/08/2011

- Intorducción El proyecto *Django* específico usado en este texto es
  sismocaracas_
  
  - Producción es solo una PC en la oficina.
  - Explicación de primero en una máquina virtual y luego en
    producción.
  - Se trata de una instalación desde un servidor con el SO recien
    instalado.
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
nuestro proyecto en este servidor.

*Python 2.7* ya viene instalado por omisión en *Fedora 14*.

Podemos instalar las versiones del gestor de paquetes de *Fedora 14*
[#]_ de *Apache* y mod-wsgi_. Para ello, basta con::

    # yum install httpd.i686 mod-wsgi

.. [#] Para que *yum* funcione sin problemas dentro de las
   instalaciones de *FUNVISIS*, es necesario configurarle el
   proxy. Para ello, se define la variable de entorno ``http_proxy``
   (en minúsculas) con el siguiente valor:
   ``http://linuxfire:3128``. En mi caso, coloqué las siguentes líneas
   en el ``.bash_profile`` del usuario ``root``::

       http_proxy=http://linuxfire:3128
       export http_proxy

.. _mod-wsgi: *mod-wsgi* le da soporte a Apache del estandar WSGI_ de *Python*

.. _WSGI: http://www.python.org/dev/peps/pep-0333/

Para instalar *Django*, prefiero usar el sistem de paquetes de Python
que el del sistema operativo. El gestor de paquetes de Python que
prefiero es *pip*, y para usarlo debemos instalar a través de *yum* el
paquete *python-setuptols* que nos da el comando *easy_intall* con el
que instalaremos *pip*. Entonces, procedemos desde una cónsola como
usuario *root*::

    # yum install python-setuptools
    # easy_install pip
    # pip install django

Y verificamos que *Django* se haya instalado bien observando que no
haya errores con el siguiente comando::

    # python -c "import django"

Con esto, ya tenemos el software necesario para instalar nuestro
proyecto, pero antes debemos configurar *Apache* y decidir el esquema
de los directorios del ambiente de producción.

Configuración inicial [web]
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
*dyn* [#]_.

.. [#] Por supuesto, habría que configurar los *DNS* o los archivos
   ``hosts`` de los clientes para que traduzcan estos *nombres* a
   direcciones *IP*.

Esto se logra creando un archivo ``.conf`` por cada host virtual en el
directorio ``/etc/httpd/vhost.d/``. A continuación, la configuración
utilizada.

- ``static.conf``::

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

- ``dyn.conf``::

    <VirtualHost *:80>
    	ServerAdmin webmaster@funvisis.gob.ve
    	ServerName dyn.funvisis.gob.ve
    	ServerAlias dyn
    
    	WSGIDaemonProcess dyn.funvisis.gob.ve processes=2 \
	threads=15 display-name=%{GROUP}

    	WSGIProcessGroup funvisis.gob.ve
    	WSGIScriptAlias \
	/sismocaracas /usr/lib/wsgi-scripts/sismocaracas.wsgi
    
    	ErrorLog ${APACHE_LOG_DIR}/error_dyn.log
    	LogLevel warn
    	CustomLog ${APACHE_LOG_DIR}/access_dyn.log combined
    </VirtualHost>

Con esta configuración estamos declarando que:

- el contenido estático será servido cuando la url de la petición
  contenga a ``static.funvisis.gob.ve`` o a ``static`` como
  *host*, y la raíz del directorio desde donde se obtendrá el
  contenido estático será ``/var/www/`` en el servidor.
- el contenido dinámico será servido cuando la url de la petición
  contenga a ``dyn.funvisis.gob.ve`` o ``dyn`` como *host*, y que
  por ahora solo hay una aplicación ubicada en el servidor en
  ``/usr/lib/wsgi-scripts/sismocaracas.wsgi`` y que se activará si la
  parte de la *ruta* del url empieza con ``/sismocaracas``

Ahora, dedicaremos un directorio dentro de ``/var/www/`` por cada
proyecto para que coloquen en ese directorio el contenido estático
específico al proyecto, y otro directorio para la aplicación *admin*
de *Django* (esta carpeta es importante para que el administrador de
Django pueda verse adecuadamente) en donde copiaremos todo el
contenido estático que dedica *Django* a esta aplicación::

    # mkdir /var/www/sismocaracas
    # mkdir /var/www/admin
    # cp -r \
    /usr/lib/python2.7/site-packages/django/contrib/admin/media/* \
    /var/www/admin

Así como es sugerido tener un lugar diferente para los scripts *CGI*
en el sistema de archivos totalmente aparte de la raíz del contenido
estático (por ejemplo, ``/usr/lib/cgi-bin/`` en sistemas tipo
*Debian*) se recomienda tener almacenados los scripts *WSGI* en un
lugar similar; en nuestro caso, elegimos
``/usr/lib/wsgi-scripts/``. Por lo tanto, debemos crear este
directorio::

    # mkdir /usr/lib/wsgi-scripts

En ese directorio colocaremos el script al que hacemos referencia en
la configuración del host virtual *dyn* (i.e
``sismocaracas.wsgi``). El contenido de este script es el siguiente::

    import os
    import sys
    
    os.environ['DJANGO_SETTINGS_MODULE'] = 'sismocaracas.settings'
    
    import django.core.handlers.wsgi
    application = django.core.handlers.wsgi.WSGIHandler()

Para que este script funcione, el directorio ``sismocaracas`` que
contiene el archivo ``settings.py`` debe estar en la ruta de búsqueda
de Python. Entonces, primero hay que decidir en qué lugar se van a
colocar los proyectos de *Django* [#]_. En nuestro caso, el directorio
dedicado a los proyectos *Django* será
``/usr/lib/django_projects``. Como detalle, colocaremos en ese
directorio, además de los direcotrios de cada proyecto con sus
respectivos settings.py, un directorio llamado ``base_templates``
donde iran las plantillas que puedan ser reutilizadas por otras
aplicaciones. Así que creamos estos directorios::

    # mkdir -p /usr/lib/django_projects/base_templates

Y hacemos que este directorio esté en la ruta de búsqueda de
*Python*. Hay dos estrategias:

- Colocar un archivo ``.pth`` en ``/usr/lib/python2.7/site-packages/``
  con el siguiente contenido: ``/usr/lib/django_projects``::

    # echo "/usr/lib/django_projects" >> /usr/lib/python2.7/funvisis.pth

- Definir la variable de entorno ``PYTHONPATH`` en el usuario que
  ejecuta el demonio *Apache*. Esta opción no la he probado y es
  posible que al ejecutarse *Apache* ignore las variables de
  entorno. De hecho, es posible que tenga alguna configuración para
  establecerle las variabales de entorno, en cuyo caso, se preferiría
  esta opción a la opción anterior del archivo ``.pth``

.. [#] Esta decisión, y las otras que tienen que ver con la
   distribución de los directorios de los proyectos, debería
   establecerse en un documento interno. También, es importante
   recordar que en próximas versiones de esta estandarización, se va a
   establecer que las aplicaciones reutilizables deben instalarce como
   paquetes del sistema y que los proyectos junto con sus aplicaciones
   específicas se instalen de la manera descrita en este documento, es
   decir, colocando el paquete en el directorio elegido para los
   proyectos *Django*.

Instalación
===========

Ya que los proyectos *Django* son simplemente paquetes estandar de
*Python*, bastaría con instalarlos como cualquier paquete *Python*,
tal vez creandoles un *setup.py*. Esto implicaría que al instalarlos
con ``python setup.py install`` quedarían en el ``dist-package`` o
``site-package`` como si fueran otro paquete de terceros que extiende
la funcionalidad de Python. Para evitar esto, se puede cambiar al
*setup.py* en su código [#]_ o al momento de su ejecución con unos
parámetros para que instale en un directorio específico.

.. [#] Cómo hacer esto se escapa del ámbito de este texto. Puede
    consultarse la `documentación de Python sobre distutils
    <http://docs.python.org/distutils/setupscript.html>`_ o en el
    artículo interno `setup.py para proyectos Django en FUNVISIS
    <setup_py_4_django_fvis.html>`_

Dicho esto, por ahora podemos aplicar una instalación más trivial;
simplemente copiamos la carpeta del proyecto en
``/usr/lib/django_projects/``. Haremos la instalación por ``setup.py``
cuando el proyecto incluya dicho script.

Suponiendo que bajamos el ``tar.gz`` en el home del ``root``, hacemos
lo siguiente::

    # cd
    # tar -xvzf sismocaracas.tar.gz -C /usr/lib/django_projects

Si la carpeta ``templates`` hubiera tenido un contenido, se copiaría
su contenido en ``/usr/lib/django_projects/base_templates``::

   # cp -R /usr/lib/django_projects/sismocaracas/templates/* \
   /usr/lib/django_projects/templates

Configuración final [``setup.py``]
----------------------------------

Por último, hay que configurar el proyecto. Todo proyecto *Django* se
configura dandole valor a ciertas variables que almacenaremos en un
archivo ``.py`` al cuál hacemos referencia desde el ``.wsgi``
configurado en *Apache*. En nuestro caso, es el archivo
``settings.py``. Éste ya tiene varios valores establecidos, pero
debemos configurar las variables [MEDIA_ROOT]_, [MEDIA_URL]_,
[STATICFILES_DIRS]_, [STATIC_URL]_, [ADMIN_MEDIA_PREFIX]_ y
[TEMPLATE_DIRS]_::

    MEDIA_ROOT = '/var/www/sismocaracas'
    MEDIA_URL = 'http://static.funvisis.gob.ve/sismocaracas/'
    STATICFILES_DIRS = (
        '/usr/lib/django_projects/sismocaracas/templates',)
    STATIC_URL = 'http://static.funvisis.gob.ve/sismocaracas/'
    ADMIN_MEDIA_PREFIX = 'http://static.funvisis.gob.ve/admin/'
    TEMPLATE_DIRS = (
        '/usr/lib/django_projects/sismocaracas/templates',
	'/usr/lib/django_projects/templates')

.. [MEDIA_ROOT] Directorio donde se va a guardar el contenido subido
   por los usuarios del proyecto.
.. [MEDIA_URL] La URL con el que se accesa al directorio
   ``MEDIA_ROOT``.
.. [STATICFILES_DIRS] Lista de directorio donde está almacenado el
   contenido estático que define la aplicación, no el que suben los
   usuarios. Hay unos ``.js`` en la aplicación ``inspection``, que
   pudiera pensarse en sacar de ahí y colocarlo en alguno de estos
   directorios.

.. [STATIC_URL] La URL con el que se accesa a los directorios
   ``STATICFILES_DIRS``.

.. [ADMIN_MEDIA_PREFIX] Prefijo *URL* utilizado para los archivos
   estáticos de la aplicación *admin* (*CSS*, *JavaScript* e
   imágenes).

.. [TEMPLATE_DIRS] Lista de directorios en los cuales *Django* busca
   una plantilla específica. Como busca en orden, colocamos de primero
   en la lista los directorios que contienen plantillas que
   substituyen a sus versiones en los otros directorios. Es decir, si
   dos plantillas con el mismo nombre están en directorios contenidos
   en esta lista, se usará la plantilla del directorio que esté
   primero en la lista.

Por último, configuramos el acceso a la base de datos (en caso de que
sea pertinente). En esta prueba, creamos una base de datos
*PostgreSQL* en el mismo servidor llamada ``sismocaracas``, cuyo dueño
es el usuario ``sismocaracas`` y su contraseña es
``jojoto``. Traducido a *Python* en el ``settings.py``::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'sismocaracas',
            'USER': 'sismocaracas',
            'PASSWORD': 'jojoto',
            'HOST': '',
            'PORT': '',
        }
    }

FIN
===

Ya está instalado el proyecto en el entorno de producción. Ahora solo
basta con visitar el proyecto en:
http://dyn.funvisis.gob.ve/sismocaracas/inspections/
