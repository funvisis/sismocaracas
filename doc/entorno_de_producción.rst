==================================================
 Un entorno de producción para un proyecto Django
==================================================

:Autor:
	"Jesús Gómez" <jgomez@funfisis.gob.ve>

:Versión: 1.1 15/08/2011

:Revisor:
	"Daniel Ampuero" <danielmaxx@gmail.com>

Este manuscrito servirá de guía para la instalación de cualquier
proyecto Django en un servidor Apache en el entorno de producción de
FUNVISIS.  A modo de ejemplo, se usará como nombre de proyecto
*djangoproject*, el cual deberá ser modificado cada vez que se cree un
nuevo proyecto con el nombre apropiado.

Todo proyecto Django debe seguir los liniemientos descritos en *BLAH*
y *BLAHBLAH*.

Empezaremos con instalar todo el software de terceros que necesita
nuestro proyecto en este servidor.

- Intorducción El proyecto *Django* específico usado en este texto es
  djangoproject_
  
  - Producción es solo una PC en la oficina.
  - Explicación de primero en una máquina virtual y luego en
    producción.
  - Se trata de una instalación desde un servidor con el SO recien
    instalado.
  - Un solo apache porque a futuro se migrará a Rails.

.. _djangoproject: http://code.funvisis.gob.ve/djangoproject/



Preparación
===========

Software
--------

- Fedora 14
- Python 2.7
- Django 1.3
- Apache 2
- mod-wsgi

*Python 2.7* ya viene instalado por omisión en *Fedora 14*.

Podemos instalar las versiones de *Apache* y mod-wsgi_ que ofrece el 
gestor de paquetes de *Fedora 14* [#]_. Para ello, como *root*, 
escribimos::

    # yum install httpd.i686 mod-wsgi

.. [#] Para que *yum* funcione sin problemas dentro de las
   instalaciones de *FUNVISIS*, es necesario configurarle el
   proxy. Para ello, se define la variable de entorno ``http_proxy``
   (en minúsculas) con el siguiente valor:
   ``http://linuxfire:3128``. Para que quede permanentemente esta
   configuración, se puede colocar en el ``.bash_profile`` del usuario
   ``root`` lo siguiente::

       http_proxy=http://linuxfire:3128
       export http_proxy

.. _mod-wsgi: *mod-wsgi* le da soporte a Apache del estandar WSGI_ de
   *Python*

.. _WSGI: http://www.python.org/dev/peps/pep-0333/

Para instalar *Django*, es preferible usar el sistem de paquetes de
Python que el del sistema operativo. El gestor de paquetes de Python
de preferencia es *pip*, y para usarlo debemos instalar a través de
*yum* el paquete *python-setuptols* que otorga el comando
*easy_intall* con el que instalaremos *pip*. Entonces, procedemos
desde una cónsola como usuario *root*::

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
eso y la delega a la vista[#]_ adecuada. Por lo tanto, el conenido
estático de un proyecto (páginas *html* estáticas, imágenes, videos,
*css*, *javascrip*, etc) no es servido a través de *Django* sino de un
servidor web separado dedicado a esta tarea.

.. [#] En *Django*, cada petición es analizada por un *enrutador*
   quien delega la acción a tomar a una *vista* en función de la
   *url*. La palabra *vista* puede confundir por eso, ya que no es más
   que un *manejador*.

Aunque lo ideal sería tener al menos dos servidores web serparados en
máquinas distintas; por ejemplo, una máquina especializada en *I/O* 
(entrada y salida) para servir el contenido estático, y otro
especializado en *cómputo* para ejecutar el código Django. En esta guía
se instalará y configurará un solo servidor web *Apache* para responder
tanto a las peticiones de contenido estático como a las peticiones de
contenido dinámico. Para lograr esto, le configuramos dos host
virtules, uno que llamaremos *static*, y otro que llamaremos
*djangoproject* [#]_.

.. [#] Por supuesto, habría que configurar los *DNS* o los archivos
   ``hosts`` de los clientes para que traduzcan estos *nombres* a
   direcciones *IP*.

Esto se logra creando un archivo ``.conf`` por cada host virtual en el
directorio ``/etc/httpd/vhost.d/``, los siguientes archivos:

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

- ``djangoproject.conf``::

    <VirtualHost *:80>
    	ServerAdmin webmaster@funvisis.gob.ve
    	ServerName djangoproject.funvisis.gob.ve
    	ServerAlias djangoproject
    
    	WSGIDaemonProcess djangoproject.funvisis.gob.ve processes=2 \
	threads=15 display-name=%{GROUP}

    	WSGIProcessGroup funvisis.gob.ve
    	WSGIScriptAlias \
	/ /usr/lib/wsgi-scripts/djangoproject.wsgi
    
    	ErrorLog ${APACHE_LOG_DIR}/error_dyn.log
    	LogLevel warn
    	CustomLog ${APACHE_LOG_DIR}/access_dyn.log combined
    </VirtualHost>

Con esta configuración estamos declarando que:

- El contenido estático será servido cuando la url de la petición
  contenga a ``static.funvisis.gob.ve`` o a ``static`` como
  *host*, y la raíz del directorio donde se obtendrá el
  contenido estático será ``/var/www/`` en el servidor.
- El contenido dinámico será servido cuando la url de la petición
  contenga a ``djangoproject.funvisis.gob.ve`` o ``djangoproject`` 
  como *host* y será manejada por el *script* de entrada 
  ``/usr/lib/wsgi-scripts/djangoproject.wsgi``.

Ahora, dedicaremos un directorio dentro de ``/var/www/`` por cada
proyecto para que coloquen en ese directorio el contenido estático
específico al proyecto, y otro directorio para la aplicación *admin*
de *Django* (esta carpeta es importante para que el administrador de
Django pueda verse adecuadamente) en donde copiaremos todo el
contenido estático que dedica *Django* a esta aplicación::

    # mkdir /var/www/djangoproject
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
la configuración del host virtual *djangoproject* (i.e
``djangoproject.wsgi``). El contenido de este script es el siguiente::

    import os
    import sys
    
    os.environ['DJANGO_SETTINGS_MODULE'] = 'djangoproject.settings'
    
    import django.core.handlers.wsgi
    application = django.core.handlers.wsgi.WSGIHandler()

Para que este script funcione, el directorio ``djangoproject``, el cual
se encuentra dentro del paquete de distribución del proyecto y contiene el
archivo``settings.py``, debe estar en la ruta de búsqueda
de Python. Entonces, primero hay que decidir en qué lugar se van a
colocar los proyectos de *Django* [#]_. El directorio
dedicado a los proyectos *Django* será
``/usr/lib/django_projects``. Como detalle, colocaremos en ese
directorio, además de los directorios de cada proyecto con sus
respectivos settings.py, un directorio llamado ``base_templates``
donde iran las plantillas que puedan ser reutilizadas por otras
aplicaciones. Así que creamos estos directorios::

    # mkdir -p /usr/lib/django_projects/base_templates

Y hacemos que este directorio esté en la ruta de búsqueda de
*Python*. Hay dos estrategias:

- Colocar un archivo ``.pth`` en ``/usr/lib/python2.7/site-packages/``
  con el siguiente contenido: ``/usr/lib/django_projects``::

    # echo "/usr/lib/django_projects" >> /usr/lib/python2.7/funvisis.pth

.. [#] Esta decisión, y las otras que tienen que ver con la
   distribución de los directorios de los proyectos, debería
   establecerse en un documento interno. También, es importante
   recordar que en próximas versiones de esta estandarización, se va a
   establecer que las aplicaciones reutilizables deben instalarse como
   paquetes del sistema y los proyectos junto con sus aplicaciones
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
    # tar -xvzf djangoproject.tar.gz -C /usr/lib/django_projects

Si la carpeta ``templates`` hubiera tenido un contenido, se copiaría
su contenido en ``/usr/lib/django_projects/base_templates``::

   # cp -R /usr/lib/django_projects/djangoproject/templates/* \
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

    MEDIA_ROOT = '/var/www/djangoproject'
    MEDIA_URL = 'http://static.funvisis.gob.ve/djangoproject/'
    STATICFILES_DIRS = (
        '/usr/lib/django_projects/djangoproject/templates',)
    STATIC_URL = 'http://static.funvisis.gob.ve/djangoproject/'
    ADMIN_MEDIA_PREFIX = 'http://static.funvisis.gob.ve/admin/'
    TEMPLATE_DIRS = (
        '/usr/lib/django_projects/djangoproject/templates',
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
*PostgreSQL* en el mismo servidor llamada ``djangoproject``, cuyo dueño
es el usuario ``djangoproject`` y su contraseña es
``jojoto``. Traducido a *Python* en el ``settings.py``::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'djangoproject',
            'USER': 'djangoproject',
            'PASSWORD': 'jojoto',
            'HOST': '',
            'PORT': '',
        }
    }

FIN
===

Ya está instalado el proyecto en el entorno de producción. Ahora solo
basta con visitar el proyecto en:
``http://djangoproject.funvisis.gob.ve/``

Finalmente, cambiamos en los archivos de configuración la línea::

    LogLevel warn

por la línea::

    LogLevel critical
