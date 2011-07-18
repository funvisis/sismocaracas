# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

import os
import datetime

def get_image_backup_path(instance, filename):
    filename_splitted = filename.rsplit('.', 1)
    return os.path.join('sismocaracas/inspections/%Y/%m/%d/', '.'.join([filename_splitted[0], datetime.datetime.now().isoformat(), filename_splitted[1]]))

# Information about extending auth.User:
# https://docs.djangoproject.com/en/dev/topics/auth/#storing-additional-information-about-users
class Participant(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField('teléfono', max_length=100)

    def __unicode__(self):
        return '{} {}'.format(self.function, self.user)

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
    code = models.CharField('1.4 Código', max_length=20)

    # 2. Participants
    inspector = models.ForeignKey(User, null=True, related_name='inspector', verbose_name='2.1 Inspector')
    reviewer = models.ForeignKey(User, null=True, related_name='reviewer', verbose_name='2.2 Revisor')
    supervisor = models.ForeignKey(User, null=True, related_name='supervisor', verbose_name='2.3 Supervisor')
    
    # 3. Interviewee
    interviewee_building_relationship = models.CharField('3.1 Relación con la Edif.', max_length=50)
    interviewee_name_last_name = models.CharField('3.2 Nombre y apellido', max_length=50)
    interviewee_phone_number = models.CharField('3.3 Teléfono', max_length=50)
    interviewee_email = models.EmailField('3.4 Correo Electrónico')

    # 4. Building identification and location
    name_or_number = models.CharField(max_length=50, verbose_name='4.1 Nombre o Nº')
    floors = models.IntegerField(verbose_name='4.2 Nº de pisos')
    semi_basements = models.IntegerField(verbose_name='4.3 Nº de semi-sótanos')
    basements = models.IntegerField(verbose_name='4.4 Nº de sótanos')
    state = models.CharField(max_length=50, verbose_name='4.5 Estado')
    city = models.CharField(max_length=100, verbose_name='4.6 Ciudad')
    municipality = models.CharField(max_length=100, verbose_name='4.7 Municipio')
    parish = models.CharField(max_length=100, verbose_name='4.8 Parroquia')
    urbanization = models.CharField(max_length=100, verbose_name='4.9 Urb, Sector, Barrio')
    street = models.CharField(max_length=100, verbose_name='4.10 Calle, Vereda, otro')
    square = models.CharField(max_length=100, verbose_name='4.11 Manzana Nº')
    plot = models.CharField(max_length=100, verbose_name='4.12 Nº Parcela')
    coord_x = models.FloatField(verbose_name='4.13 Coord. X')
    coord_y = models.FloatField(verbose_name='4.14 Coord. Y')
    time_zone = models.FloatField(verbose_name='4.15 Huso')

    # 5. Building usage
    # building_usage = models.CharField(max_length=50, choices=(
    #         ('Gubernamental',         'Gubernamental'),
    #         ('Bomberos',              'Bomberos'),
    #         ('Protección Civil',      'Protección Civil'),
    #         ('Policial',              'Policial'),
    #         ('Militar',               'Militar'),
    #         ('Vivienda Popular',      'Vivienda Popular'),
    #         ('Vivienda Unifamiliar',  'Vivienda Unifamiliar'),
    #         ('Vivienda Multifamiliar','Vivienda Multifamiliar'),
    #         ('Médico-Asistencial',    'Médico-Asistencial'),
    #         ('Educativo',             'Educativo'),
    #         ('Deportivo-Recreativo',  'Deportivo-Recreativo'),
    #         ('Cultural',              'Cultural'),
    #         ('Industrial',            'Industrial'),
    #         ('Comercial',             'Comercial'),
    #         ('Oficina',               'Oficina'),
    #         ('Religioso',             'Religioso'),
    #         ('Otro',                  'Otro'), # TODO: Otro should able insert the text
    #         ),
                                      # help_text='TODO: "Otro" será un campo de textocuando se elija.'
                                      # )

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
    sports_recreational = models.BooleanField(verbose_name='Deportivo-Recreativo')
    cultural = models.BooleanField(verbose_name='Cultural')

    industrial = models.BooleanField(verbose_name='Industrial')
    commercial = models.BooleanField(verbose_name='Comercial')
    office = models.BooleanField(verbose_name='Oficina')
    religious = models.BooleanField(verbose_name='Religioso')

    other = models.CharField(verbose_name='Otro (Especifique)', max_length='50')
    
    # 6. Carrying Capacity
    people = models.IntegerField(verbose_name='6.1 Número de personas que ocupan el inmueble')
    occupation_during = models.CharField(max_length=10, verbose_name='6.2 Ocupación durante', choices=(
            (u'mañana', 'mañana'),
            ('tarde', 'tarde'),
            ('noche', 'noche'),
            ),
                                         )

    # 7. Building age
    year = models.IntegerField(verbose_name='7.1 Año de construcción')
    year_range = models.CharField(max_length=20, verbose_name = '7.2 Rango del año de construcción', choices=(
            ('<1940', 'Antes de 1940'),
            ('[1940, 1947]', 'Entre 1940 y 1947'),
            ('[1948, 1955]', 'Entre 1948 y 1955'),
            ('[1956, 1967]', 'Entre 1956 y 1967'),
            ('[1968, 1982]', 'Entre 1968 y 1982'),
            ('[1999, 2001]', 'Entre 1999 y 2001'),
            ('>2001', 'Después de 2001'),
            ))

    # 8. Ground conditions
    building_at = models.CharField(max_length="10", verbose_name='8.1 Edificación en', choices=(
            ('Planicie', 'Planicie'),
            ('Ladera', 'Ladera'),
            ('Base', 'Base'),
            ('Cima', 'Cima'),
            )
                                   )

    # 32.5 means (20º - 45º)
    # 67.5 means > 45º
    ground_slope = models.FloatField(verbose_name='8.2 Pendiente del terreno', choices=(
            (32.5, '20º - 45º'),
            (67.5, 'Mayor a 45º'),
            )
                              )
    ground_over = models.BooleanField(verbose_name='8.3 Localizada sobre la mitad superior de la ladera')

    talus_slope = models.FloatField(verbose_name='8.4 Pendiente del talud', choices=(
            (32.5, '20º - 45º'),
            (67.5, 'Mayor a 45º'),
            )
                              )
    talus_separation_gt_H = models.BooleanField(verbose_name='8.5 Separación al talud', choices=((False, 'Menor a H del Talud'), (True, 'Mayor a H del Talud')))
    drainage = models.BooleanField(verbose_name='8.6 Drenajes')

    # 9. Structural type
    gates_of_concrete = models.BooleanField(verbose_name='Pórticos de concreto armado')
    gates_of_concrete_block_walls_filled_with_clay_concrete = models.BooleanField(verbose_name='Pórticos de concreto armado rellenos con paredes de bloques de arcilla de concreto')
    diagonalized_steel_frames = models.BooleanField(verbose_name='Pórticos diagonalizados')
    gates_of_steel_trusses = models.BooleanField(verbose_name='Pórticos de acero con cerchas')
    reinforced_concrete_walls_in_two_horizontal_directions = models.BooleanField(verbose_name='Muros de concreto armado en dos direcciones horizontales')
    systems_with_reinforced_concrete_walls_in_one_direction = models.BooleanField(verbose_name='Sistemas con muros de concreto armado en una sola dirección', help_text='como algunos sistemas del tipo túnel')
    pre_built_systems_based_on_large_panels_or_frames = models.BooleanField(verbose_name='Sistemas pre-fabricados a base de grandes paneles o de pórticos')
    confined_load_bearing_mosonry = models.BooleanField(verbose_name='Sistemas cuyos elementos portantes sean mampostería confinada')
    not_confined_load_bearing_masonry = models.BooleanField(verbose_name='Sistemas cuyos elementos portantos sean mampostería no confinada')
    steel_frames = models.BooleanField(verbose_name='Pórticos de acero')
    steel_frames_with_hollow = models.BooleanField(verbose_name='Pórticos de acero con perfiles tabulares')

    # 10. Floor scheme
    floor_scheme = models.CharField(verbose_name='', max_length='20', choices=(
            ('H', 'H'),
            ('L', 'L'),
            ('T', 'T'),
            ('O', 'O'),
            ('U', 'U'),
            ('rectangular', u'\u25AD o \u25AB'),
            ('esbeltez horizontal', 'esbeltez horizontal'),
            ('ninguno', 'Ninguno'),
            )
                                    )

    # 11. Lifting scheme
    lifting_scheme = models.CharField(verbose_name='', max_length=20, choices=(
            ('T', 'T'),
            ('U', 'U'),
            ('L', 'L'),
            ('rectangular', u'\u25AF'),
            ('pirámide invertida', 'Pirámide invertida'),
            ('piramidal', 'Piramidal'),
            ('esveltez vertical', 'Esveltez, vertical'),
            ('ninguno', 'Ninguno'),
            )
                                      )
    # 12. Irregularities

    strong_asymmetry_in_plant_mass_or_stiffness = models.BooleanField(verbose_name='Fuerte asimetría de masas o rigideces en planta')
    no_high_beams_on_one_or_two_directions = models.BooleanField(verbose_name='Ausencia de vigías altas en una o dos direcciones')
    presence_of_at_least_one_soft_or_weak_mezzanine = models.BooleanField(verbose_name='Presencia de al menos un entrepiso débil o blando')

    # 13. Degree of degradation
    
    condition_of_concrete = models.CharField(verbose_name='13.1 Est. de Concreto', help_text='Agrietamiento en elementos estructurales y/o corrosión en acero de refuerzo',
                                             max_length=10,
                                             choices=(
            ('ninguno', 'Ninguno'),
            ('moderado', 'Moderado'),
            ('severo', 'Severo'),
            )
                                             )
    condition_of_steel = models.CharField(verbose_name='13.2 Est. de Acero', help_text='Corrosión en elementos de acero y/o deterioro de conexiones y/o pandeo',
                                          max_length=10,
                                          choices=(
            ('ninguno', 'Ninguno'),
            ('moderado', 'Moderado'),
            ('severo', 'Severo'),
            )
                                          )
    fill_cracks_in_walls = models.CharField(verbose_name='13.3 Agrietamiento en paredes de relleno',
                                          max_length=10,
                                          choices=(
            ('ninguno', 'Ninguno'),
            ('moderado', 'Moderado'),
            ('severo', 'Severo'),
            )
                                          )
    condition_of_upkeep = models.CharField(verbose_name='13.4 Estado general de mantenimiento ',
                                          max_length=10,
                                          choices=(
            ('bueno', 'Bueno'),
            ('regular', 'Regular'),
            ('bajo', 'Bajo'),
            )
                                          )

    # 14. Observations
    observations = models.TextField()

    # 15 Image Backup
    image_backup = models.ImageField(upload_to=get_image_backup_path)
    
    def __unicode__(self):
        return "".format(self.code, self.date, self.inspector)

