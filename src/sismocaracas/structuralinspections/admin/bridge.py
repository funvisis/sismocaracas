# -*- coding: utf-8 -*-

from ..models import Bridge

from django.contrib import admin

from funvisis.django.decorators import conditional_fieldsets

@conditional_fieldsets
class BridgeAdmin(admin.ModelAdmin):
    fieldsets_base = (
        (
            u'1. Datos Generales',
            {
                'fields': (
                    'init_time',
                    'end_time',
                    'code')}),
        (
            u'2. Datos de los participantes',
            {
                'fields': (
                    # 'inspector',
                    'reviewer',
                    'supervisor')}),
        (
            u'3. Datos Generales y ubicación administrativa',
            {
                'fields': (
                    'bridge_distributor_highway_name',
                    'road_function',
                    'state',
                    'city',
                    'municipality',
                    'parish',
                    'urbanization',)}),
        (
            u'4. Identificación y ubicación geográfica de la rampa o puente independiente',
            {
                'fields': (
                    'name_or_direction_identification',
                    'name_of_road_on_bridge',
                    'road_type',
                    'under_bridge_element_name',
                    'under_bridge_element_type',
                    'access_to_important_facility',
                    'name_of_important_facility',
                    'coord_pins',
                    'coord_pieo',
                    'coord_pfns',
                    'coord_pfeo'
                    )}),
        (
            u'5. Edad del puente',
            {
                'fields': (
                    'year',
                    'source',
                    'year_range',)}),
        (
            u'6. Condiciones del terreno',
            {
                'fields': (
                    'location',
                    'maximum_ground_slope',
                    'soil_weakness',)}),
        (
            u'7. Características geométricas y estructurales',
            {
                'fields': (
                    'bridge_length',
                    'bridge_width',
                    'segment_number',
                    'maximum_distance_between_columns',
                    'maximum_column_height',
                    'joint_number_on_road',
                    'L_relation_between_close_segments',
                    'H_relation_between_close_columns',
                    'straight_bridge',
                    'subtended_angle',
                    'bridge_deviation',
                    'structure_continuity',
                    'superstructure_type',
                    'superstructural_type_other',
                    'column_material_type',
                    'column_material_type_other',
                    'column_geometry_type',
                    'column_geometry_type_other',
                    'is_any_column_a_pergola',
                    'does_columns_had_side_capitals_tops',
                    'does_board_has_individuals_beams',
                    'does_board_has_two_or_tree_beams',
                    'superstructure_number_of_discontinuities',
                    'typical_joint_length',
                    'does_bridge_horizontally_linked_to_others_structures',
                    'horizontally_linked_structures_names',
                    'does_bridge_vertically_linked_to_others_structures',
                    'verticallyy_linked_structures_names',)}),
        (
            u'8. Daños observados y estado de mantenimiento del puente', {
                'fields': (
                    'observations',)}),
        (
            u'9. Observaciones adicionales',
            {
                'fields':
                    ('additional_observations',)}),
        (
            u'10. Respaldo digital',
            {
                'fields': (
                    'document_backup',)}),
        (
            u'11. Respaldo de fotos de la estructura',
            {
                'fields': (
                    'photos_backup',)}),)

    fieldsets_existent = (
        (
            u'12. Fotos de la estructura',
            {
                'fields' : (
                    'bridge_gallery',),}),)


    #    (
    #        u'Índice de amenaza',
    #        {
    #            'fields': (
    #                'caracas',
    #                'national_level_zonification',
    #                'macrozone_ccs',
    #                'microzone_ccs'),}),)


    conditioned_fieldsets = [
        (
            lambda request: True,
            fieldsets_base),

        (
            lambda request: \
                request.user.is_superuser or \
                request.user.groups.filter(name="supervisores") or \
                request.user.groups.filter(name="revisores"),
            fieldsets_super),
        ]



    date_hierarchy = 'init_time'

    list_display = (
        'inspector',
        'init_time',
        'city',
        'urbanization',
        )

    # list_filter = (
    #      'inspector',
    #     'city',)

    search_fields = [
        '^inspector__user__username',
        '^inspector__user__first_name',
        '^inspector__user__last_name',
        '=city',
        'urbanization']

    def save_model(self, request, obj, form, change): # The logged
                                                      # user is going
                                                      # to be the
                                                      # inspector
        if not change: # Only adding sets the inspector
            obj.inspector = request.user.fvisuser
        obj.save()

    def queryset(self, request):

        if request.user.groups.filter(name='supervisores') or \
                request.user.is_superuser:
            return Building.objects.all()

        return Building.objects.filter(inspector=request.user.fvisuser)


    class Media:
        js = ('js/admin/custom.js', ) 
