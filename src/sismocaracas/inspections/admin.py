# -*- coding: utf-8 -*-

from models import Participant
from models import Inspection

from django.contrib import admin
from django.contrib.admin.sites import AdminSite

class InspectionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('1. Datos Generales', {
                'fields': ('date', 'init_time', 'end_time', 'code')
                }),
        ('2. Datos de los participantes', {
                'fields': ('inspector', 'reviewer', 'supervisor')
                }),
        ('3. Datos del entrevistado', {
                'fields': ('interviewee_building_relationship', 'interviewee_name_last_name', 'interviewee_phone_number', 'interviewee_email')
                }),
        ('4. Identificación y ubicación del edificio', {
                'fields': ('name_or_number', 'floors', 'semi_basements', 'basements', 'state', 'city', 'municipality', 'parish', 'urbanization', 'street', 'square', 'plot', 'coord_x', 'coord_y', 'time_zone')
                }),
        ('5. Uso de la edificación', {
                'fields': ('governmental', 'firemen', 'civil_defense', 'police', 'military', 'popular_housing', 'single_family', 'multifamily', 'medical_care', 'educational', 'sports_recreational', 'cultural', 'industrial', 'commercial', 'office', 'religious', 'other')
                }),
        ('6. Capacidad de ocupación', {
                'fields': ('people', 'occupation_during')
                }),
        ('7. Año de la construcción', {
                'fields': ('year', 'year_range')
                }),
        ('8. Condición del terreno', {
                'fields': ('building_at', 'ground_slope', 'ground_over', 'talus_slope', 'talus_separation_gt_H', 'drainage')
                }),
        ('9. Tipo estructural', {
                'fields': ('gates_of_concrete', 'gates_of_concrete_block_walls_filled_with_clay_concrete', 'diagonalized_steel_frames', 'gates_of_steel_trusses', 'reinforced_concrete_walls_in_two_horizontal_directions', 'systems_with_reinforced_concrete_walls_in_one_direction', 'pre_built_systems_based_on_large_panels_or_frames', 'confined_load_bearing_mosonry', 'not_confined_load_bearing_masonry', 'steel_frames', 'steel_frames_with_hollow')
                }),
        ('10. Esquema de planta', {
                'fields': ('floor_scheme',)
                }),
        ('11. Esquema de elevación', {
                'fields': ('lifting_scheme',)
                }),

        ('12. Irregularidades', {
                'fields': ('no_high_beams_on_one_or_two_directions', 'presence_of_at_least_one_soft_or_weak_mezzanine', 'presence_of_short_columns', 'discontinuity_lines_of_columns', 'significant_openings_in_slabs', 'strong_asymmetry_in_plant_mass_or_stiffness', 'separation_between_buildings', 'attaching_slab_slab', 'attaching_slab_column')
                }),
        ('13. Grado de deterioro', {
                'fields': ('condition_of_concrete', 'condition_of_steel', 'fill_cracks_in_walls', 'condition_of_upkeep')
                }),
        ('14. Observaciones', {
                'fields': ('observations',)
                }),
        ('15. Respaldo de la planilla', {
                'fields': ('image_backup',)
                }),
        (u'_. Índice de amenaza (Solo para el revisor o el supervisor) ._', {
                'fields': ('caracas', 'national_level_zonification', 'macrozone_ccs', 'microzone_ccs'),
                'classes': ['collapse']
                }),
        )
    
    class Media:
        js = ('js/admin/custom.js', )

admin_site = AdminSite('admin_site')

# admin.site.register(Inspection)
# admin.site.register(Participant)
admin_site.register(Inspection, InspectionAdmin)
admin_site.register(Participant)
# admin_site.register(Participant)
