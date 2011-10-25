# -*- coding: utf-8 -*-
#from django.db import models
from django.conf import settings
from django.contrib.gis.db import models
#from django.contrib.auth.models import User
from funvisis.django.fvisusers.models import FVISUser
#from funvisis.django.fvisgallery.models import FVISGallery
from photologue.models import Gallery
#from photologue.models import GalleryUpload


from funvisis.utils.djangorelated \
    import get_path_to_app_repo_ as get_path_to_app_repo

import os
import datetime
import time

class Building(models.Model):

    # 1. General
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    init_time = models.DateTimeField(verbose_name=u'1.1 Hora inicio')
    end_time = models.DateTimeField(verbose_name=u'1.2 Hora culminación')
    code = models.CharField(
        verbose_name=u'1.3 Código', max_length=20, blank=True)

    # 2. Participants
    inspector = models.ForeignKey(
        FVISUser, related_name=u'building_inspector',
        verbose_name=u'2.1 Inspector')
    reviewer = models.ForeignKey(
        FVISUser,
        related_name=u'building_reviewer',
        verbose_name=u'2.2 Revisor',
        limit_choices_to={'user__groups__name': u'revisores'})
    supervisor = models.ForeignKey(
        FVISUser, related_name=u'building_supervisor',
        verbose_name=u'2.3 Supervisor',
                limit_choices_to={'user__groups__name': u'supervisores'})

    # 3. Interviewee
    interviewee_building_relationship = models.CharField(
        verbose_name=u'3.1 Relación con la Edif.', max_length=50)
    interviewee_name_last_name = models.CharField(
        verbose_name=u'3.2 Nombre y apellido', max_length=50)
    interviewee_phone_number = models.CharField(
        verbose_name=u'3.3 Teléfono', max_length=50, blank=True)
    interviewee_email = models.EmailField(
        verbose_name=u'3.4 Correo Electrónico', blank=True)

    # 4. Building identification and location
    name_or_number = models.CharField(
        max_length=50, verbose_name=u'4.1 Nombre o Nº')
    floors = models.IntegerField(verbose_name=u'4.2 Nº de pisos')
    semi_basements = models.IntegerField(verbose_name=u'4.3 Nº de semi-sótanos')
    basements = models.IntegerField(verbose_name=u'4.4 Nº de sótanos')
    state = models.CharField(max_length=50, verbose_name=u'4.5 Estado')
    city = models.CharField(max_length=100, verbose_name=u'4.6 Ciudad')
    municipality = models.CharField(
        max_length=100, verbose_name=u'4.7 Municipio')
    parish = models.CharField(max_length=100, verbose_name=u'4.8 Parroquia')
    urbanization = models.CharField(
        max_length=100, verbose_name=u'4.9 Urb, Sector, Barrio')
    street = models.CharField(
        max_length=100, verbose_name=u'4.10 Calle, Vereda, otro', blank=True)
    square = models.CharField(
        max_length=100, verbose_name=u'4.11 Manzana Nº', blank=True)
    plot = models.CharField(
        max_length=100, verbose_name=u'4.12 Nº Parcela', blank=True)
    #coord_x = models.FloatField(
    #    verbose_name=u'4.13 Coord. X', null=True, blank=True)
    #coord_y = models.FloatField(
    #    verbose_name=u'4.14 Coord. Y', null=True, blank=True)
    point = models.PointField(verbose_name='4.13 Ubicación geográfica', srid=4189)
    #time_zone = models.FloatField(
    #    verbose_name=u'4.15 Huso', null=True, blank=True)

    # 5. Building usage
    governmental = models.BooleanField(verbose_name=u'Gubernamental')
    firemen = models.BooleanField(verbose_name=u'Bomberos')
    civil_defense = models.BooleanField(verbose_name=u'Protección Civil')
    police = models.BooleanField(verbose_name=u'Policial')
    military = models.BooleanField(verbose_name=u'Military')
    popular_housing = models.BooleanField(verbose_name=u'Vivienda Popular')
    single_family = models.BooleanField(verbose_name=u'Vivienda Unifamiliar')
    multifamily = models.BooleanField(verbose_name=u'Vivienda Multifamiliar')

    medical_care = models.BooleanField(verbose_name=u'Médico-Asistencial')
    educational = models.BooleanField(verbose_name=u'Educativo')
    sports_recreational = models.BooleanField(
        verbose_name=u'Deportivo-Recreativo')
    cultural = models.BooleanField(verbose_name=u'Cultural')

    industrial = models.BooleanField(verbose_name=u'Industrial')
    commercial = models.BooleanField(verbose_name=u'Comercial')
    office = models.BooleanField(verbose_name=u'Oficina')
    religious = models.BooleanField(verbose_name=u'Religioso')

    other = models.CharField(
        verbose_name=u'Otro (Especifique)', max_length='50', blank=True)

    # 6. Carrying Capacity
    people = models.IntegerField(
        verbose_name=u'6.1 Número de personas que ocupan el inmueble')
    # occupation_during = models.CharField(
    #     max_length=10, verbose_name='6.2 Ocupación durante',
    #     choices=(
    #         (u'mañana', 'mañana'),
    #         ('tarde', 'tarde'),
    #         ('noche', 'noche'),),)
    occupation_during_morning = models.BooleanField(verbose_name=u'mañana')
    occupation_during_afternoon = models.BooleanField(verbose_name=u'tarde')
    occupation_during_evening = models.BooleanField(verbose_name=u'noche')

    # 7. Building age
    year = models.IntegerField(
        verbose_name=u'7.1 Año de construcción', null=True, blank=True)
    year_range = models.CharField(
        max_length=20, verbose_name = u'7.2 Rango del año de construcción',
        choices=(
            ('<1940', 'Antes de 1940'),
            ('[1940, 1947]', 'Entre 1940 y 1947'),
            ('[1948, 1955]', 'Entre 1948 y 1955'),
            ('[1956, 1967]', 'Entre 1956 y 1967'),
            ('[1968, 1982]', 'Entre 1968 y 1982'),
            ('[1983, 1998]', 'Entre 1983 y 1998'),
            ('[1999, 2001]', 'Entre 1999 y 2001'),
            ('>2001', 'Después de 2001'),))

    # 8. Ground conditions
    building_at = models.CharField(
        max_length='10', verbose_name=u'8.1 Edificación en',
        choices=(
            ('planicie', 'Planicie'),
            ('ladera', 'Ladera'),
            ('base', 'Base'),
            ('cima', 'Cima'),))

    # 32.5 means (20º - 45º)
    # 67.5 means > 45º
    ground_slope = models.CharField(
        max_length='10', verbose_name=u'8.2 Pendiente del terreno',
        choices=(
            ('[20, 45]', '20º - 45º'),
            ('>45', 'Mayor a 45º'),),
        blank=True)
    ground_over = models.BooleanField(
        verbose_name=u'8.3 Localizada sobre la mitad superior de la ladera',
        choices=(
            (True, u'Sí'),
            (False, u'No')))
    talus_slope = models.FloatField(
        verbose_name=u'8.4 Pendiente del talud',
        choices=(
            (32.5, '20º - 45º'),
            (67.5, 'Mayor a 45º'),), # Al limpiar la base de datos,
                                     # cambiar el promedio por los
                                     # rangos adecuados.
        null=True, blank=True)
    talus_separation_gt_H = models.BooleanField(
        verbose_name=u'8.5 Separación al talud',
        choices=(
            (False, 'Menor a H del Talud'),
            (True, 'Mayor a H del Talud')))
    drainage = models.BooleanField(
        verbose_name=u'8.6 Drenajes',
        choices=(
            (True, u'Sí'),
            (False, u'No')))

    # 9. Structural type
    gates_of_concrete = models.BooleanField(
        verbose_name=u'Pórticos de concreto armado')
    gates_of_concrete_block_walls_filled_with_clay_concrete = \
        models.BooleanField(
        verbose_name=u'Pórticos de concreto armado rellenos con paredes' \
            ' de bloques de arcilla de concreto')
    diagonalized_steel_frames = models.BooleanField(
        verbose_name=u'Pórticos diagonalizados')
    gates_of_steel_trusses = models.BooleanField(
        verbose_name=u'Pórticos de acero con cerchas')
    reinforced_concrete_walls_in_two_horizontal_directions = \
        models.BooleanField(
        verbose_name=u'Muros de concreto armado en dos direcciones horizontales')
    systems_with_reinforced_concrete_walls_in_one_direction = \
        models.BooleanField(
        verbose_name=u'Sistemas con muros de concreto' \
            u' armado en una sola dirección',
        help_text='como algunos sistemas del tipo túnel')
    pre_built_systems_based_on_large_panels_or_frames = models.BooleanField(
        verbose_name=u'Sistemas pre-fabricados a base de' \
            u' grandes paneles o de pórticos')
    confined_load_bearing_mosonry = models.BooleanField(
        verbose_name=u'Sistemas cuyos elementos portantes' \
            u'sean mampostería confinada')
    not_confined_load_bearing_masonry = models.BooleanField(
        verbose_name=u'Sistemas cuyos elementos portantos' \
            u' sean mampostería no confinada')
    steel_frames = models.BooleanField(verbose_name=u'Pórticos de acero')
    steel_frames_with_hollow = models.BooleanField(
        verbose_name=u'Pórticos de acero con perfiles tabulares')

    # 10. Floor scheme
    floor_scheme = models.CharField(
        verbose_name=u'', max_length='20',
        choices=(
            ('H', 'H'),
            ('L', 'L'),
            ('T', 'T'),
            ('O', 'O'),
            ('U', 'U'),
            ('rectangular', u'\u25AD o \u25AB'),
            ('esbeltez horizontal', 'Esbeltez horizontal'),
            ('ninguno', 'Ninguno'),),
        blank=False)

    # 11. Lifting scheme
    lifting_scheme = models.CharField(
        verbose_name=u'', max_length=20,
        choices=(
            ('T', 'T'),
            ('U', 'U'),
            ('L', 'L'),
            ('rectangular', u'\u25AF'),
            (u'pirámide invertida', u'Pirámide invertida'),
            ('piramidal', 'Piramidal'),
            ('esveltez vertical', 'Esbeltez, vertical'), # Limpiar la
                                                         # base de
                                                         # datos para
                                                         # cambiar
                                                         # esveltez
                                                         # por
                                                         # esbeltez
            ('ninguno', 'Ninguno'),),
        blank=False)
    # 12. Irregularities

    no_high_beams_on_one_or_two_directions = models.BooleanField(
        verbose_name=u'12.1 Ausencia de vigas altas en una o dos direcciones')
    presence_of_at_least_one_soft_or_weak_mezzanine = models.BooleanField(
        verbose_name=u'12.2 Presencia de al menos un entrepiso débil o blando')
    presence_of_short_columns = models.BooleanField(
        verbose_name=u'12.3 Presencia de columnas cortas')
    discontinuity_lines_of_columns = models.BooleanField(
        verbose_name=u'12.4 Discontinuidad de ejes de columnas')
    significant_openings_in_slabs = models.BooleanField(
        verbose_name=u'12.5 Aberturas significativas en losas')
    strong_asymmetry_in_plant_mass_or_stiffness = models.BooleanField(
        verbose_name=u'12.6 Fuerte asimetría de masas o rigideces en planta')
    separation_between_buildings = models.IntegerField(
        verbose_name=u'12.7 Separación entre edificios (cm)',
        help_text='Colocar algun valor, así sea cero (0)',
        null=True,
        blank=True
        )
    # attaching_slab_slab = models.BooleanField(
    #     verbose_name='12.8 Adosamiento: Losa contra losa')
    # attaching_slab_column = models.BooleanField(
    #     verbose_name='12.9 Adosamiento: Columna contra losa')
    attaching_slab_slab_column = models.CharField(
        max_length=15,
        verbose_name=u'12.8 Tipo de adosamiento',
        choices=(
            ('ninguno', 'Ninguno'),
            ('slab_slab', 'Losa contra losa'), # Limpiar la base de
                                               # datos para cambiar
                                               # slab_slab a losa
                                               # contra losa
            ('column_slab', 'Columna contra losa'),))

    # 13. Degree of degradation

    condition_of_concrete = models.CharField(
        verbose_name=u'13.1 Est. de Concreto',
        help_text='Agrietamiento en elementos estructurales' \
            ' y/o corrosión en acero de refuerzo',
        max_length=10,
        choices=(
            ('ninguno', 'Ninguno'),
            ('moderado', 'Moderado'),
            ('severo', 'Severo'),))
    condition_of_steel = models.CharField(
        verbose_name=u'13.2 Est. de Acero',
        help_text='Corrosión en elementos de acero y/o' \
            'deterioro de conexiones y/o pandeo',
        max_length=10,
        choices=(
            ('ninguno', 'Ninguno'),
            ('moderado', 'Moderado'),
            ('severo', 'Severo'),))
    fill_cracks_in_walls = models.CharField(
        verbose_name=u'13.3 Agrietamiento en paredes de relleno',
        max_length=10,
        choices=(
            ('ninguno', 'Ninguno'),
            ('moderado', 'Moderado'),
            ('severo', 'Severo'),))
    condition_of_upkeep = models.CharField(
        verbose_name=u'13.4 Estado general de mantenimiento ',
        max_length=10,
        choices=(
            ('bueno', 'Bueno'),
            ('regular', 'Regular'),
            ('bajo', 'Bajo'),))

    # 14. Observations
    observations = models.TextField(
        verbose_name=u'14. Observaciones', blank=True)

    # 15 Image Backup
    image_backup = models.FileField(
        verbose_name=u'15. Respaldo escaneado',
        upload_to=get_path_to_app_repo(
            project_name=settings.SETTINGS_MODULE.split('.')[0],
            app_name=__name__.split('.')[-2],
            model_name='Inspection'),
        null=True,
        blank=True)

    # 16 Building Pictures
    building_gallery = models.OneToOneField(
        Gallery, related_name=u'building_gallery',
        verbose_name=u'16 Fotos',
        blank=True,)

    # __. Threat Index
    caracas = models.BooleanField(
        verbose_name=u'¿Es en Caracas?',
        help_text='Solo para el revisor o el supervisor',
        choices=(
            (True, 'Sí'),
            (False, 'No'),))
    national_level_zonification = models.IntegerField(
        verbose_name=u'Nivel nacional_zonificación',
        null=True, blank=True,
        help_text='Solo para el revisor o el supervisor',
        choices=((1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7)))

    macrozone_ccs = models.CharField(
        max_length=20, blank=True,
        verbose_name=u'CCS_Macrozona',
        help_text='Solo para el revisor o el supervisor',
        choices=(
            ('sur', 'Sur'),
            ('centro_sur', 'Centro Sur'),
            ('centro_norte', 'Centro Norte'),
            ('norte', 'Norte')))
    microzone_ccs = models.CharField(
        max_length=3, blank=True,
        verbose_name=u'CCS_Microzona',
        help_text='Solo para el revisor o el supervisor',
        choices=(
            ('1-1', '1-1'),
            ('1-2', '1-2'),
            ('2-1', '2-1'),
            ('2-2', '2-2'),
            ('3-1', '3-1'),
            ('3-2', '3-2'),
            ('3-3', '3-3'),
            ('4-1', '4-1'),
            ('4-2', '4-2'),
            ('5', '5'),
            ('6', '6'),
            ('7-1', '7-1')))

    class Meta:
        verbose_name = u"Edificación"
        verbose_name_plural = u"Edificaciones"

    def __unicode__(self):
        return u"{0}:{1}:{2}".format(
            u' '.join(
                (
                    self.inspector.user.first_name,
                    self.inspector.user.last_name)).strip()
            or
            self.inspector, self.init_time, self.id)

    def has_topographic_effects(self):
        return \
            self.building_at == 'cima' \
            or \
            self.building_at == 'ladera' and self.ground_over

    def threat_index(self):
        '''[0.23, 1.0]'''
        from .analysis import \
            threat_index_by_macro_zones_caracas, \
            threat_index_by_macro_zones_national
        macro_zone_table = \
            threat_index_by_macro_zones_caracas \
            if self.caracas \
            else threat_index_by_macro_zones_national
        macro_zone_self_value = \
            self.macrozone_ccs \
            if self.caracas \
            else self.national_level_zonification

        try:
            return macro_zone_table[macro_zone_self_value][
                0 if not self.has_topographic_effects() else 1]
        except KeyError:
            return None

    def vulnerability_index(self):
        '''[6.5, 100.0]'''
        return 6.5

    def importance_index(self):
        '''[0.8, 1.0]'''
        return 0.8

    def priorization_index(self):
        return self.threat_index() * self.vulnerability_index() * \
            importance_index()

#VERIFICAR campos null y blank

class Bridge(models.Model):
    # Think about geolocalization
    # Maybe Djangogeo

    # 1. General
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    init_time = models.DateTimeField('1.1 Hora inicio')
    end_time = models.DateTimeField(u'1.2 Hora culminación')
    code = models.CharField(u'1.3 Código', max_length=20, blank=True)

    # 2. Participants
    inspector = models.ForeignKey(
        FVISUser, related_name=u'bridge_inspector',
        verbose_name=u'2.1 Inspector')
    reviewer = models.ForeignKey(
        FVISUser,
        related_name=u'bridge_reviewer',
        verbose_name=u'2.2 Revisor',
        limit_choices_to={'user__groups__name': u'revisores'})
    supervisor = models.ForeignKey(
        FVISUser, related_name=u'bridge_supervisor',
        verbose_name=u'2.3 Supervisor',
                limit_choices_to={'user__groups__name': u'supervisores'})

    # 3. General data and set location
    bridge_distributor_highway_name = models.CharField(
		max_length=50, 
		verbose_name=u'3.1 Nombre del Puente, Distribuidor o Autopista')
    road_function = models.CharField(
        max_length=20, verbose_name= u'3.2 Función vial',
        choices=(
            ('puente', 'Puente'),
            ('elevado', 'Tramo elevado'),
            ('distribuidor', 'Distribuidor'),),)
    state = models.CharField(
		max_length=25, verbose_name=u'3.3 Estado',  blank=True)
    city = models.CharField(
		max_length=25, verbose_name=u'3.4 Ciudad',  blank=True)
    municipality = models.CharField(
        max_length=100, verbose_name=u'3.5 Municipio')
    parish = models.CharField(
		max_length=100, verbose_name=u'3.6 Parroquia')
    urbanization = models.CharField(
        max_length=100, verbose_name=u'3.7 Urb, Sector, Barrio')
    
    # 4. Ramp or independent bridge identification and location
    name_or_direction_identification = models.CharField(
        max_length=50, 
		verbose_name=u'4.1 Nombre o identificación de sentidos')
    name_of_road_on_bridge = models.CharField(
		max_length=40,
		verbose_name=u'4.2.1 Nombre de vía sobre el puente',
        blank=True)
    road_type = models.CharField(
		max_length = 40,
        blank=True,
        verbose_name=u'4.2.2 Tipo',
		choices=(
			('autopista', 'Autopista'),
			('calle_o_avenida', 'Calle o Avenida'),),)
    under_bridge_element_name = models.CharField(
		max_length=50, 
        blank=True,
		verbose_name=u'4.3.1 Nombres de vías, ríos u otros elementos bajo el puente')
    under_bridge_element_type = models.CharField(
		max_length=30,
        blank=True, 
		verbose_name=u'4.3.2 Tipos de elementos bajo el puente',
		choices=(
			('autopista', u'Autopista'),
			('calle_o_avenida', u'Calle o Avenida'),
			('rio', u'Río'),
			('edificacion', u'Edificación'),
			('instalacion_importante', u'Instalación importante'),
			('otros', u'Otros'),),)
    access_to_important_facility = models.BooleanField(
            blank=False,
			verbose_name=u'4.4.1 ¿El puente da acceso a inst. importante?',
			choices=(
			    (True, 'Sí'),
			    (False, 'No'),),)
    name_of_important_facility = models.CharField(
		max_length=100,
        blank=True,
		verbose_name=u'4.4.2 Nombre de la inst. importante')
    coord_pins = models.FloatField(
        verbose_name=u'4.5.1 Coord. P.I. N-S', null=True, blank=True)
    coord_pieo = models.FloatField(
        verbose_name=u'4.5.2 Coord. P.I. E-O', null=True, blank=True)
    coord_pfns = models.FloatField(
        verbose_name=u'4.6.1 Coord. P.F. N-S', null=True, blank=True)
    coord_pfeo = models.FloatField(
        verbose_name=u'4.6.2 Coord. P.F. E-O', null=True, blank=True)

   	# 5. Bridge age
    year = models.IntegerField(
        verbose_name=u'5.1 Año', null=True, blank=True)
    source = models.CharField(
		max_length=50, verbose_name=u'5.2 Fuente')
    year_range = models.CharField(
        max_length=20, 
        verbose_name = '5.3 Rango del año de construcción',
        choices=(
            ('<1968', 'Antes de 1968'),
            ('[1968, 1985]', 'Entre 1968 y 1985'),
            ('[1986, 1998]', 'Entre 1986 y 1998'),
            ('>1998', 'Después de 1998'),))

    # 6. Ground conditions
    location = models.CharField(
        max_length=40, verbose_name=u'6.1 Ubicación',
        choices=(
            ('planicie_o_ladera_inferior', u'En Planicie o la mitad superior de una ladera'),
            ('ladera_superior_o_cima', u'En la mitad superior de una ladera o en la cima de una ladera'),),)

    maximum_ground_slope = models.CharField(
        max_length=10, verbose_name=u'6.2 Pendiente máxima de la ladera',
        choices=(
            ('<20', 'Menor a 20°(36%))'),
            ('>20', 'Mayor a 20°(36%))'),),
        )
    soil_weakness = models.CharField(
		max_length=20, 
		verbose_name=u'6.3 Susceptibilidad de licuación del suelo',
        choices=(
			('baja', 'Baja'),
			('moderada', 'Moderada'),
			('alta', 'Alta'),
			('desconocida', 'No se conoce'),),)

    # 7. Geometric and Structural Characteristics
    bridge_length = models.FloatField(
        verbose_name=u'7.1 Longitud del puente')
    bridge_width = models.FloatField(
        verbose_name=u'7.2 Ancho del puente')
    segment_number = models.FloatField(
        verbose_name=u'7.3 Número de tramos')
    maximum_distance_between_columns = models.FloatField(
        verbose_name=u'7.4 Luz máxima')
    maximum_column_height = models.FloatField(
        verbose_name=u'7.5 Altura máxima de pilas')
    joint_number_on_road = models.FloatField(
        verbose_name=u'7.6 Número de juntas en la losa del tablero')
    L_relation_between_close_segments = models.CharField(
        max_length=4,
        verbose_name=u'7.7 Relación L en tramos adyacentes',
        choices=(
            ('<2', '<2.0'),
            ('>2', '>2.0'),),)
    H_relation_between_close_columns = models.CharField(
        max_length=4,
        verbose_name=u'7.8 Relación H en pilas adyacentes',
        choices=(
            ('<2', '<2.0'),
            ('>2', '>2.0'),),)
    straight_bridge = models.BooleanField(
        verbose_name=u'7.9 Alineamiento del puente',
        blank=False,
        choices=(
		    (True, 'Recto'),
		    (False, 'Curvo'),),)
    subtended_angle = models.IntegerField(
        verbose_name=u'7.10 Ángulo Subtendido',
        )
    bridge_deviation = models.IntegerField(
        verbose_name=u'7.11 Esviaje del puente',
        )
    structure_continuity = models.CharField(
        max_length=40,
        verbose_name=u'7.12 Continuidad de la estructura',
        choices=(
            ('apoyados', 'Tableros simplemente apoyados'),
            ('continuos', u'Tableros contínuos'),
            ('totalmente_continuo', 'Estructura totalmente contínua'),),)
    superstructure_type = models.CharField(
        max_length=40,
        verbose_name=u'7.13 Tipo de superestructura',
        choices=(
            ('MACIZ', 'Losa maciza de concreto (MACIZ)'),
            ('VCON', 'Losa sobre viga de concreto (VCON)'),
            ('VPRE', 'Losa sobre vigas prefabricadas de concreto (VPRE)'),
            ('VCAJC', 'Losa sobre viga cajón de concreto (VCAJC)'),
            ('ACA', 'Arco de concreto (ACA)'),
            ('PMET', 'Losa sobre perfiles metálicos (PMET)'),
            ('VARM', 'Losa sobre vigas de acero armadas (VARM)'),
            ('VCAJM', 'Losa sobre viga cajón metálica (VCAJM)'),
            ('AMI', 'Armadura metálica con arriostramiento inferior (AMI)'),
            ('AMS', 'Armadura metálica con arriostramiento superior (AMS)'),
            ('AAC', 'Arco de acero (ACC)'),
            ('COLG', 'Puente colgante (COLG)'),
            ('ATIR', 'Puente atirantado (ATIR)'),
            ('MAMP', 'Puente de mamposteria (MAMP)'),
            ('MAD', 'Puente de madera (MAD)'),
            ('OTRO', 'Otro'),),)
    superstructural_type_other = models.CharField(
        max_length=40,
        verbose_name=u'OTRO - Otro, indique', 
        null=True, 
        blank=True)
    column_material_type = models.CharField(
        max_length=40,
        verbose_name=u'7.14.1 Tipo de pilas. Material',
        choices=(
            ('concreto', 'Concreto'),
            ('acero', 'Acero'),
            ('otro', 'Otro'),),)
    column_material_type_other = models.CharField(
        max_length=100,
        verbose_name=u'Otro. Indique',
        null=True, blank=True)
    column_geometry_type = models.CharField(
        max_length=40,
        verbose_name=u'7.14.2 Tipo de pilas. Geometría',
        choices=(
            ('monocolumnas', 'Pilas monocolumnas'),
            ('multicolumnas', 'Pilas multicolumnas'),
            ('muros', 'Pilas de muros'),
            ('estribos', 'Solo estribos'),
            ('otro', 'Otro'),),)
    column_geometry_type_other = models.CharField(
        max_length=100,
        verbose_name=u'Otro. Indique',
        null=True, blank=True)
    is_any_column_a_pergola = models.BooleanField(
        verbose_name=u'7.14.3 ¿Alguna de las pilas es de tipo pérgola?',
        blank=False,
        choices=(
		    (True, 'Sí'),
		    (False, 'No'),),)
    does_columns_had_side_capitals_tops = models.CharField(
        max_length=40,
        blank=False,
        verbose_name=u'7.15 ¿Las pilas tienen topes laterales en el capitel?',
        choices=(
            ('si', 'Sí'),
            ('no', 'No'),
            ('algunas', 'Sólo algunas') ,),)
    does_board_has_individuals_beams = models.BooleanField(
        verbose_name=u'7.16 ¿El tablero posee vigas individuales y esta soportado por columnas o pedestales individuales sin capitel?',
        blank=False,
        choices=(
		    (True, 'Sí'),
		    (False, 'No'),),)
    does_board_has_two_or_tree_beams = models.BooleanField(
        verbose_name=u'7.17 ¿El tablero posee 2 ó 3 vigas individuales y la viga exterior esta cerca del borde lateral del apoyo?',
        choices=(
		    (True, 'Sí'),
		    (False, 'No'),),)
    superstructure_number_of_discontinuities = models.IntegerField(
        verbose_name=u'7.18 Nro. de discontinuidades en la superestructura',
        )
    typical_joint_length = models.FloatField(
        verbose_name=u'7.19 Longitud de apoyo típica en las juntas',
        )
    does_bridge_horizontally_linked_to_others_structures = models.BooleanField(
        verbose_name=u'7.20.1 ¿La estructura del puente esta vinculada horizontalmente a otras estructuras?',
            choices=(
		    (True, 'Sí'),
		    (False, 'No'),))
    horizontally_linked_structures_names = models.CharField (
        max_length=100,
        verbose_name=u'7.20.2 Nombre de estructuras vinculadas horizontalmente:',
        blank=True,)
    does_bridge_vertically_linked_to_others_structures = models.BooleanField(
        verbose_name=u'7.21.1 ¿La estructura del puente esta vinculada verticalmente a otras estructuras?',
        blank=False,
            choices=(
		    (True, 'Sí'),
		    (False, 'No'),))
    verticallyy_linked_structures_names = models.CharField (
        max_length=100,
        verbose_name=u'7.21.2 Nombre de estructuras vinculadas verticalmente:',
        blank=True,)

    # 8. Damage Observed and Mantainment state of the bridge
    observations = models.TextField(
        verbose_name=u'8. Daños Observados y Estado General de Mantenimiento del Puente',
        )

    # 9. Additional Observations
    additional_observations = models.TextField(
        verbose_name=u'9. Observaciones Adicionales',
        blank=True,)

    # 10 Image Backup
    image_backup = models.FileField(
        verbose_name=u'10. Respaldo escaneado',
        upload_to=get_path_to_app_repo(
            project_name=settings.SETTINGS_MODULE.split('.')[0],
            app_name=__name__.split('.')[-2],
            model_name='Bridge'),
        null=True,
        blank=True)

    # 11 Bridge Pictures
    bridge_gallery = models.OneToOneField(
        Gallery, related_name=u'bridge_gallery',
        verbose_name=u'11 Fotos',
        blank=True,)

    def __unicode__(self):
        return u"{0}:{1}:{2}".format(
            u' '.join(
                (
                    self.inspector.user.first_name,
                    self.inspector.user.last_name)).strip()
            or
            self.inspector, self.init_time, self.id)

    class Meta:
        verbose_name = u"Puente"
        verbose_name_plural = u"Puentes"

