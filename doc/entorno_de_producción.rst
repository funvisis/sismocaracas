===================================================================
Un entorno de producción estándar para un proyecto Django (FUVISIS)
===================================================================

:Autor:
	"Jesús Gómez" <jgomez@funfisis.gob.ve>

:Versión: 1.3 18/08/2011

:Revisor:
	"Daniel Ampuero" <danielmaxx@gmail.com>

Este documento servirá de guía para la instalación y configuración de
un ambiente de producción en FUNVISIS para instalar cualquier proyecto
*Django* [#]_.  A modo de ejemplo, se usará como nombre de proyecto
*djangoproject* [#]_, el cual deberá ser modificado cada vez que se
cree un nuevo proyecto con el nombre apropiado.

.. [#] Para saber más de *Django* visite http://www.djangoproject.com/

.. [#] Asumiremos que *djangoproject* cumple con los lineamientos
   descritos en el documento `Estándar para distribución de proyectos
   Django en FUNVISIS <distro_django_funvisis.html>`_

Empezaremos con instalar todo el software de terceros que necesita
nuestro proyecto en este servidor.

Preparación
===========

Software
--------

- Fedora 14
- Python 2.7
- Django 1.3
- Apache 2
- mod-wsgi

El entorno de producción considerado en este documento será un
servidor dedicado con el sistema operativo *Fedora 14*. *Python 2.7*
ya viene instalado por omisión en *Fedora 14*.

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

.. _mod-wsgi: *mod-wsgi* le da soporte a Apache del estándar WSGI_ de
   *Python*

.. _WSGI: http://www.python.org/dev/peps/pep-0333/

Para instalar *Django*, es preferible usar el sistema de paquetes de
Python que el del sistema operativo. El gestor de paquetes de Python
de preferencia es *pip*, y para usarlo debemos instalar a través de
*yum* el paquete *python-setuptols* que otorga el comando
*easy_intall* con el que instalaremos *pip*. Entonces, procedemos
desde una consola como usuario *root*::

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

*Django* no hace nada especial cuando le hacen una petición que
termine en alguna extensión; es indiferente para él si termina en
*.html*, en *.php* o en *.jpeg*. Para *Django* una petición es solo
eso y la delega a la vista [#]_ adecuada. Por lo tanto, el contenido
estático de un proyecto (páginas *html* estáticas, imágenes, videos,
*css*, *javascrip*, etc) no es servido a través de *Django* sino de un
servidor web separado dedicado a esta tarea.

.. [#] En *Django*, cada petición es analizada por un *enrutador*
   quien delega la acción a tomar a una *vista* en función de la
   *url*. La palabra *vista* puede confundir por eso, ya que no es más
   que un *manejador*.

Una configuración típica del entorno de producción es contar con al
menos dos servidores web separados en máquinas distintas; por
ejemplo, una máquina especializada en *I/O* (entrada y salida) para
servir el contenido estático, y otro especializado en *cómputo* para
ejecutar el código Django. Otra alternativa es la que se explica en
este documento, donde se instala y configura un solo servidor web
*Apache* para responder tanto a las peticiones de contenido estático
como a las peticiones de contenido dinámico. Se decidió explicar esta
alternativa ya que con esta información el lector será capaz de
instalar un ambiente con dos servidores por ser más sencillo que
instalarlo en un solo servidor.

Para que *Apache* responda a ambos tipos de peticiones, configuraremos
dos host virtuales [#]_, uno que llamaremos *static*, que contendrá los
recursos estáticos de todos los proyectos o sitios web, y otro que
llamaremos *djangoproject* [#]_. 


.. [#] *Host Virtual* es una técnica utilizada por *Apache* para
   responder a peticiones web de manera diferente dependiendo del
   nombre o la *IP* del *host* que hace la petición.

.. [#] Por supuesto, habría que configurar los *DNS* o los archivos
   ``hosts`` de los clientes para que traduzcan estos *nombres* a
   direcciones *IP*.

Para lograr todo lo mencionado anteriormente, primero, en el archivo
``/etc/httpd/conf/httpd.conf`` se activa la drectiva
``NameVirtualHost`` y se incluye la directiva ``Include
vhost_d/*.conf`` (si es que ya no está) con la cuál establecemos el
convenio de crear un archivo .conf por cada host virtual. Las líneas
pertinentes en el archivo ``http.conf`` serían las siguientes::

	NameVirtualHost *:80
	Include vhost_d/*.conf

Luego se creará un archivo ``.conf`` por cada host virtual en el
directorio ``/etc/httpd/vhost.d/``:

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
    	LogLevel crit
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
    
    	ErrorLog ${APACHE_LOG_DIR}/djangoproject.error.log
    	LogLevel crit
    	CustomLog ${APACHE_LOG_DIR}/djangoproject.access.log combined
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

El punto de entrada de los proyectos *Django* cuando los sirve
*Apache* con *WSGI* es un pequeño script ``.wsgi``. Así como es
sugerido tener un lugar diferente para los scripts *CGI* en el sistema
de archivos totalmente aparte de la raíz del contenido estático (por
ejemplo, ``/usr/lib/cgi-bin/`` en sistemas tipo *Debian*) se
recomienda tener almacenados los scripts *WSGI* en un lugar similar;
en nuestro caso, elegimos ``/usr/lib/wsgi-scripts/``. Por lo tanto,
debemos crear este directorio::

    # mkdir /usr/lib/wsgi-scripts

El directorio dedicado a los proyectos *Django* será
``/usr/lib/django-projects``. Como detalle, colocaremos en ese
directorio un directorio llamado ``base-templates`` donde irán las
plantillas que puedan ser reutilizadas por otras aplicaciones. Así que
creamos estos directorios::

    # mkdir -p /usr/lib/django-projects/base-templates

Y hacemos que este directorio esté en la ruta de búsqueda de *Python*
colocando un archivo ``.pth`` en ``/usr/lib/python2.7/site-packages/``
con el siguiente contenido: ``/usr/lib/django-projects``::

    # echo "/usr/lib/django-projects" >> /usr/lib/python2.7/funvisis.pth

Hecho todo esto, reiniciamos el servidor ``Apache``::

    # service httpd restart

Instalación
===========

Ya que los proyectos *Django* que instalaremos en este entorno
entienden el estándar descrito en este documento y el descrito en el
documento [2]_, en teoría debería bastar con ejecutar el script
``setup.py`` del proyecto adecuadamente.

Primero, debemos obtener el paquete del proyecto. Una manera
hipotética es que encontrándose en un servidor de archivos de la
fundación llamado ``code.funvisis.gob.ve`` [#]_, lo obtendríamos, por
ejemplo, de la siguiente manera::

    # wget -cb http://code.funvisis.gob.ve/djangoproject/lastest

Y por último, descomprimimos el paquete y lo instalamos con::

    # tar -xzf djangoproject-0.1.tar.gz
    # cd djangoproject
    # python setup.py install

.. [#] Con esto queda abierta la sugerencia de establecer un servidor
   de código donde se mantendría un repositorio de software
   oficialmente producido y mantenido por la fundación.

Completar
---------

Explicar:

- ¿Qué hace el ``setup.py``?¿dónde coloca qué?
- las opciones de instalación para cambiar la conducta por omisión de
  ``setup.py``

Configuración final [Base de datos]
-----------------------------------

Por último, configuramos el acceso a la base de datos (en caso de que
sea pertinente) editando el archivo ``settings.py`` que luego de la
instalación por omisión se encuentra en el directorio
``/usr/lib/django-projects/djangoproject/``. El siguiente ejemplo
supone una base de datos llamada ``djangoproject`` en un servidor de
base de datos *PostgreSQL* en el host ``bd.funvisis.gob.ve`` accesible
a través del puerto ``5432``, con un usuario llamado ``djangoproject``
con suficientes privilegios para utilizar todo el proyecto y su
contraseña es ``jojoto``. Traducido a *Python* en el ``settings.py``::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'djangoproject',
            'USER': 'djangoproject',
            'PASSWORD': 'jojoto',
            'HOST': 'bd.funvisis.gob.ve',
            'PORT': '5432',
        }
    }

Si la base de datos está recien creada, se inicializa con el siguiente
comando (si se hizo una instalación personalizada, entonces hay que
ajustar la ruta del comando ``manage.py``)::

    #python /usr/lib/django-projects/sismocaracas/manage.py syncdb

FIN
===

Ya está instalado el proyecto en el entorno de producción. Para
ponerlo a prueba, solo basta con visitar el proyecto en:
``http://djangoproject.funvisis.gob.ve/``
