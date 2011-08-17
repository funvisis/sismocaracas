# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import User

from funvisis.utils.djangorelated \
    import get_path_to_app_repo_ as get_path_to_app_repo

import os
import datetime
import time

# Information about extending auth.User:
# https://docs.djangoproject.com/en/dev/topics/auth/#storing-additional-information-about-users
class Participant(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField('teléfono', max_length=100)

    def __unicode__(self):
        return '{}'.format(self.user)

def create_participant(sender, instance, created, **kwargs):
    if created:
        Participant.objects.create(user=instance)

post_save.connect(create_participant, sender=User)

class Inspection(models.Model):
    # Think about geolocalization
    # Maybe Djangogeo

    # 1. General
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    date = models.DateField('1.1 fecha')
    init_time = models.DateTimeField('1.2 Hora inicio')
    end_time = models.DateTimeField('1.3 Hora culminación')
    code = models.CharField('1.4 Código', max_length=20, blank=True)

    # 2. Participants
    inspector = models.ForeignKey(
        User, related_name='inspector', verbose_name='2.1 Inspector')
    reviewer = models.ForeignKey(
        User, related_name='reviewer', verbose_name='2.2 Revisor')
    supervisor = models.ForeignKey(
        User, related_name='supervisor', verbose_name='2.3 Supervisor')

    # 3. Interviewee
    interviewee_building_relationship = models.CharField(
        '3.1 Relación con la Edif.', max_length=50)
    interviewee_name_last_name = models.CharField(
        '3.2 Nombre y apellido', max_length=50)
    interviewee_phone_number = models.CharField(
        '3.3 Teléfono', max_length=50, blank=True)
    interviewee_email = models.EmailField('3.4 Correo Electrónico', blank=True)

    # 4. Building identification and location
    name_or_number = models.CharField(
        max_length=50, verbose_name='4.1 Nombre o Nº')
    floors = models.IntegerField(verbose_name='4.2 Nº de pisos')
    semi_basements = models.IntegerField(verbose_name='4.3 Nº de semi-sótanos')
    basements = models.IntegerField(verbose_name='4.4 Nº de sótanos')
    state = models.CharField(max_length=50, verbose_name='4.5 Estado')
    city = models.CharField(max_length=100, verbose_name='4.6 Ciudad')
    municipality = models.CharField(
        max_length=100, verbose_name='4.7 Municipio')
    parish = models.CharField(max_length=100, verbose_name='4.8 Parroquia')
    urbanization = models.CharField(
        max_length=100, verbose_name='4.9 Urb, Sector, Barrio')
    street = models.CharField(
        max_length=100, verbose_name='4.10 Calle, Vereda, otro', blank=True)
    square = models.CharField(
        max_length=100, verbose_name='4.11 Manzana Nº', blank=True)
    plot = models.CharField(
        max_length=100, verbose_name='4.12 Nº Parcela', blank=True)
    coord_x = models.FloatField(
        verbose_name='4.13 Coord. X', null=True, blank=True)
    coord_y = models.FloatField(
        verbose_name='4.14 Coord. Y', null=True, blank=True)
    time_zone = models.FloatField(
        verbose_name='4.15 Huso', null=True, blank=True)

    # 5. Building usage
    governmental = models.BooleanField(verbose_name='Gubernamental')
    firemen = models.BooleanField(verbose_name='Bomberos')
    civil_defense = models.BooleanField(verbose_name='Protección Civil')
    police = models.BooleanField(verbose_name='Policial')
    military = models.BooleanField(verbose_name='Military')
    popular_housing = models.BooleanField(verbose_name='Vivienda Popular')
    single_family = models.BooleanField(verbose_name='Vivienda Unifamiliar')
    multifamily = models.BooleanField(verbose_name='Vivienda Multifamiliar')

    medical_care = models.BooleanField(verbose_name='Médico-Asistencial')
    educational = models.BooleanField(verbose_name='Educativo')
    sports_recreational = models.BooleanField(
        verbose_name='Deportivo-Recreativo')
    cultural = models.BooleanField(verbose_name='Cultural')

    industrial = models.BooleanField(verbose_name='Industrial')
    commercial = models.BooleanField(verbose_name='Comercial')
    office = models.BooleanField(verbose_name='Oficina')
    religious = models.BooleanField(verbose_name='Religioso')

    other = models.CharField(
        verbose_name='Otro (Especifique)', max_length='50', blank=True)

    # 6. Carrying Capacity
    people = models.IntegerField(
        verbose_name='6.1 Número de personas que ocupan el inmueble')
    occupation_during = models.CharField(
        max_length=10, verbose_name='6.2 Ocupación durante',
        choices=(
            (u'mañana', 'mañana'),
            ('tarde', 'tarde'),
            ('noche', 'noche'),),)

    # 7. Building age
    year = models.IntegerField(
        verbose_name='7.1 Año de construcción', null=True, blank=True)
    year_range = models.CharField(
        max_length=20, verbose_name = '7.2 Rango del año de construcción',
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
        max_length='10', verbose_name='8.1 Edificación en',
        choices=(
            ('planicie', 'Planicie'),
            ('ladera', 'Ladera'),
            ('base', 'Base'),
            ('cima', 'Cima'),))

    # 32.5 means (20º - 45º)
    # 67.5 means > 45º
    ground_slope = models.CharField(
        max_length='10', verbose_name='8.2 Pendiente del terreno',
        choices=(
            ('[20, 45]', '20º - 45º'),
            ('>45', 'Mayor a 45º'),),
        blank=True)
    ground_over = models.BooleanField(
        verbose_name='8.3 Localizada sobre la mitad superior de la ladera')
    talus_slope = models.FloatField(
        verbose_name='8.4 Pendiente del talud',
        choices=(
            (32.5, '20º - 45º'),
            (67.5, 'Mayor a 45º'),),
        null=True, blank=True)
    talus_separation_gt_H = models.BooleanField(
        verbose_name='8.5 Separación al talud',
        choices=(
            (False, 'Menor a H del Talud'),
            (True, 'Mayor a H del Talud')))
    drainage = models.BooleanField(verbose_name='8.6 Drenajes')

    # 9. Structural type
    gates_of_concrete = models.BooleanField(
        verbose_name='Pórticos de concreto armado')
    gates_of_concrete_block_walls_filled_with_clay_concrete = \
        models.BooleanField(
        verbose_name='Pórticos de concreto armado rellenos con paredes' \
            ' de bloques de arcilla de concreto')
    diagonalized_steel_frames = models.BooleanField(
        verbose_name='Pórticos diagonalizados')
    gates_of_steel_trusses = models.BooleanField(
        verbose_name='Pórticos de acero con cerchas')
    reinforced_concrete_walls_in_two_horizontal_directions = \
        models.BooleanField(
        verbose_name='Muros de concreto armado en dos direcciones horizontales')
    systems_with_reinforced_concrete_walls_in_one_direction = \
        models.BooleanField(
        verbose_name='Sistemas con muros de concreto' \
            ' armado en una sola dirección',
        help_text='como algunos sistemas del tipo túnel')
    pre_built_systems_based_on_large_panels_or_frames = models.BooleanField(
        verbose_name='Sistemas pre-fabricados a base de' \
            ' grandes paneles o de pórticos')
    confined_load_bearing_mosonry = models.BooleanField(
        verbose_name='Sistemas cuyos elementos portantes' \
            'sean mampostería confinada')
    not_confined_load_bearing_masonry = models.BooleanField(
        verbose_name='Sistemas cuyos elementos portantos' \
            ' sean mampostería no confinada')
    steel_frames = models.BooleanField(verbose_name='Pórticos de acero')
    steel_frames_with_hollow = models.BooleanField(
        verbose_name='Pórticos de acero con perfiles tabulares')

    # 10. Floor scheme
    floor_scheme = models.CharField(
        verbose_name='', max_length='20',
        choices=(
            ('H', 'H'),
            ('L', 'L'),
            ('T', 'T'),
            ('O', 'O'),
            ('U', 'U'),
            ('rectangular', u'\u25AD o \u25AB'),
            ('esbeltez horizontal', 'Esbeltez horizontal'),),
        blank=True)

    # 11. Lifting scheme
    lifting_scheme = models.CharField(
        verbose_name='', max_length=20,
        choices=(
            ('T', 'T'),
            ('U', 'U'),
            ('L', 'L'),
            ('rectangular', u'\u25AF'),
            ('pirámide invertida', 'Pirámide invertida'),
            ('piramidal', 'Piramidal'),
            ('esveltez vertical', 'Esveltez, vertical'),),
        blank=True)
    # 12. Irregularities

    no_high_beams_on_one_or_two_directions = models.BooleanField(
        verbose_name='12.1 Ausencia de vigías altas en una o dos direcciones')
    presence_of_at_least_one_soft_or_weak_mezzanine = models.BooleanField(
        verbose_name='12.2 Presencia de al menos un entrepiso débil o blando')
    presence_of_short_columns = models.BooleanField(
        verbose_name='12.3 Presencia de columnas cortas')
    discontinuity_lines_of_columns = models.BooleanField(
        verbose_name='12.4 Discontinuidad de ejes de columnas')
    significant_openings_in_slabs = models.BooleanField(
        verbose_name='12.5 Aberturas significativas en losas')
    strong_asymmetry_in_plant_mass_or_stiffness = models.BooleanField(
        verbose_name='12.6 Fuerte asimetría de masas o rigideces en planta')
    separation_between_buildings = models.IntegerField(
        verbose_name='12.7 Separación entre edificios (cm)',
        null=True, blank=True)
    attaching_slab_slab = models.BooleanField(
        verbose_name='12.8 Adosamiento: Losa contra losa')
    attaching_slab_column = models.BooleanField(
        verbose_name='12.9 Adosamiento: Columna contra losa')

    # 13. Degree of degradation

    condition_of_concrete = models.CharField(
        verbose_name='13.1 Est. de Concreto',
        help_text='Agrietamiento en elementos estructurales' \
            ' y/o corrosión en acero de refuerzo',
        max_length=10,
        choices=(
            ('ninguno', 'Ninguno'),
            ('moderado', 'Moderado'),
            ('severo', 'Severo'),))
    condition_of_steel = models.CharField(
        verbose_name='13.2 Est. de Acero',
        help_text='Corrosión en elementos de acero y/o' \
            'deterioro de conexiones y/o pandeo',
        max_length=10,
        choices=(
            ('ninguno', 'Ninguno'),
            ('moderado', 'Moderado'),
            ('severo', 'Severo'),))
    fill_cracks_in_walls = models.CharField(
        verbose_name='13.3 Agrietamiento en paredes de relleno',
        max_length=10,
        choices=(
            ('ninguno', 'Ninguno'),
            ('moderado', 'Moderado'),
            ('severo', 'Severo'),))
    condition_of_upkeep = models.CharField(
        verbose_name='13.4 Estado general de mantenimiento ',
        max_length=10,
        choices=(
            ('bueno', 'Bueno'),
            ('regular', 'Regular'),
            ('bajo', 'Bajo'),))

    # 14. Observations
    observations = models.TextField(
        verbose_name='14. Observaciones', blank=True)

    # 15 Image Backup
    image_backup = models.ImageField(
        verbose_name='15. Respaldo escaneado',
        upload_to=get_path_to_app_repo(
            project_name=settings.SETTINGS_MODULE.split('.')[0],
            app_name=__name__.split('.')[-2],
            model_name='Inspection'))

    # __. Threat Index
    caracas = models.BooleanField(
        verbose_name=u'¿Es en Caracas?',
        help_text='Solo para el revisor o el supervisor')
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

    def __unicode__(self):
        return "{}:{}:{}".format(
            ' '.join(
                (self.inspector.first_name, self.inspector.last_name)).strip()
            or
            self.inspector, self.date, self.id)

    def has_topographic_effects(self):
        return \
            self.building_at == 'cima' \
            or \
            self.building_at == 'ladera' and self.ground_over

    def threat_index(self):
        '''[0.23, 1.0]'''
        from inspections.analysis import \
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
