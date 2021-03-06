# -*- coding: utf-8 -*-

from ..models import Building

from django.contrib import admin

from funvisis.misc.decorators import conditional_fieldsets

@conditional_fieldsets
class BuildingAdmin(admin.ModelAdmin):

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
            u'3. Datos del entrevistado',
            {
                'fields': (
                    'interviewee_building_relationship',
                    'interviewee_name_last_name',
                    'interviewee_phone_number',
                    'interviewee_email')}),
        (
            u'4. Identificación y ubicación del edificio',
            {
                'fields': (
                    'name_or_number',
                    'floors',
                    'semi_basements',
                    'basements',
                    'state',
                    'city',
                    'municipality',
                    'parish',
                    # 'urbanization',
                    'urbanization_neighborhood',
                    'sector',
                    'street',
                    'square',
                    'plot',
                    'coord_x',
                    'coord_y',
                    )}),
        (
            u'5. Uso de la edificación',
            {
                'fields': (
                    'governmental',
                    'firemen',
                    'civil_defense',
                    'police',
                    'military',
                    'popular_housing',
                    'single_family',
                    'multifamily',
                    'medical_care',
                    'educational',
                    'sports_recreational',
                    'cultural',
                    'industrial',
                    'commercial',
                    'office',
                    'religious',
                    'other')}),
        (
            u'6. Capacidad de ocupación',
            {
                'fields': (
                    'people',)}),
        (
            u'7. Períodos de ocupación',
            {
                'fields': (
                    'occupation_during_morning',
                    'occupation_during_afternoon',
                    'occupation_during_evening',)}),
        (
            u'8. Año de la construcción', {
                'fields': (
                    'year',
                    'year_range')}),
        (
            u'9. Condición del terreno',
            {
                'fields':
                    ('building_at',
                     'ground_slope',
                     'ground_over',
                     'talus_slope',
                     'talus_separation_gt_H',
                     'drainage')}),
        (
            u'10. Tipo estructural',
            {
                'fields': (
                    'gates_of_concrete',
                    'gates_of_concrete_block_walls_filled_with_clay_concrete',
                    'reinforced_concrete_walls_in_two_horizontal_directions',
                    'systems_with_reinforced_concrete_walls_in_one_direction',
                    'steel_frames',
                    'steel_frames_with_hollow',
                    'diagonalized_steel_frames',
                    'gates_of_steel_trusses',
                    'pre_built_systems_based_on_large_panels_or_frames',
                    'confined_load_bearing_mosonry_wall',
                    'confined_load_bearing_mosonry_wall_floors',
                    'not_confined_load_bearing_masonry_wall',
                    'not_confined_load_bearing_masonry_wall_floors',
                    'frames_and_low_quality_masonry_mixed',
                    'frames_and_low_quality_masonry_mixed_floors',
                    'one_floor_bahareque',
                    'precorious',)}),
        (
            u'11. Esquema de planta',
            {
                'fields': (
                    'floor_scheme',)}),
        (
            u'12. Esquema de elevación',
            {
                'fields': (
                    'lifting_scheme',)}),

        (
            u'13. Irregularidades',
            {
                'fields': (
                    'no_high_beams_on_one_or_two_directions',
                    'presence_of_at_least_one_soft_or_weak_mezzanine',
                    'presence_of_short_columns',
                    'discontinuity_lines_of_columns',
                    'significant_openings_in_slabs',
                    'strong_asymmetry_in_plant_mass_or_stiffness',
                    'one_direction_wall_absence',
                    # 'attaching_slab_slab_column',
                    'attaching_slab_slab',
                    'attaching_slab_column',
                    'separation_between_buildings',)}),
        (
            u'14. Grado de deterioro',
            {
                'fields': (
                    'condition_of_concrete',
                    'condition_of_steel',
                    'fill_cracks_in_walls',
                    'condition_of_upkeep')}),
        (
            u'15. Observaciones',
            {
                'fields': (
                    'observations',)}),
        (
            u'16. Respaldo de la planilla',
            {
                'fields': (
                    'image_backup',)}),)

    fieldsets_super = (
        (
            u'Índice de amenaza',
            {
                'fields': (
                    'caracas',
                    'national_level_zonification',
                    'macrozone_ccs',
                    'microzone_ccs'),}),)

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

    def usage_list_display(self, obj):
        text_length = 50
        usage_fields = [
            'governmental',
            'firemen',
            'civil_defense',
            'police',
            'military',
            'popular_housing',
            'single_family',
            'multifamily',
            'medical_care',
            'educational',
            'sports_recreational',
            'cultural',
            'industrial',
            'commercial',
            'office',
            'religious',]
        result = ', '.join(
            [
                Building._meta.get_field(_).verbose_name
                for _ in usage_fields
                if getattr(obj, _)] + [obj.other])

        return result

    list_display = (
        'inspector',
        'init_time',
        'city',
        # 'urbanization',
        'urbanization_neighborhood',
        'sector',
        'usage_list_display',
        )

    # list_filter = (
    #      'inspector',
    #     'city',)

    search_fields = [
        '^inspector__user__username',
        '^inspector__user__first_name',
        '^inspector__user__last_name',
        '=city',
        # 'urbanization',
        'urbanization_neighborhood',
        'sector',]


    # def get_form(self, request, obj=None, **kwargs):
    #     """
    #     Exclude some fields based on the request.user.
    #     """

    #     self.fieldsets = self.fieldsets_infra

    #     if (
    #         request.user.is_superuser or
    #         request.user.groups.filter(name="supervisores") or
    #         request.user.groups.filter(name="revisores")):

    #         self.fieldsets += self.fieldsets_super # FIXME: use some
    #                                                # argument or
    #                                                # custom ModelAdmin
    #                                                # field to mark the
    #                                                # fields to
    #                                                # remove. Later,
    #                                                # make a custom
    #                                                # ModelAdmin
    #                                                # classdefine that
    #                                                # field, and others
    #                                                # like the
    #                                                # condition to
    #                                                # evaluate to
    #                                                # remove the
    #                                                # fields.

    #     if obj is not None and not(
    #                 request.user.is_superuser or
    #                 request.user.groups.filter(name="supervisores") or
    #                 request.user.groups.filter(name="revisores")):
    #         self.readonly_fields = ('supervisor', 'reviewer')
    #     else:
    #         try:
    #             del self.readonly_fields
    #         except AttributeError:
    #             pass

    #     return super(BuildingAdmin, self).get_form(request, obj=obj, **kwargs)

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
