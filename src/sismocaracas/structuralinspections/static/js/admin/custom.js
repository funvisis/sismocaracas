function set_visibility(d, v)
{
    // console.log(v);
    for each(var f in d[v])
	f[0][f[1]]('slow');
}

(function($) {
    $(document).ready(function($) {
	d = {};
	d['planicie'] = [
	    [$('.ground_slope'), 'hide'],
	    [$('.ground_over'), 'hide'],
	    [$('.talus_slope'), 'hide'],
	    [$('.talus_separation_gt_H'), 'hide']
	];
	d[''] = d['planicie'];
	d['ladera'] = [
	    [$('.ground_slope'), 'show'],
	    [$('.ground_over'), 'show'],
	    [$('.talus_slope'), 'hide'],
	    [$('.talus_separation_gt_H'), 'hide']
	];
	d['base'] = [
	    [$('.ground_slope'), 'hide'],
	    [$('.ground_over'), 'hide'],
	    [$('.talus_slope'), 'show'],
	    [$('.talus_separation_gt_H'), 'show']
	];
	d['cima'] = d['base'];

	v = $('#id_building_at').val();
	set_visibility(d, v);
	
	$('#id_building_at').change(function(event){
	    v = $(this).val();
	    set_visibility(d, v);
	});

	d2 = {};
	d2[''] = [
	    [$('.separation_between_buildings'), 'hide']
	];
	d2['ninguno'] = d2[''];
	d2['slab_slab'] = [
	    [$('.separation_between_buildings'), 'show']
	];
	d2['column_slab'] = d2['slab_slab']

	v2 = $('#id_attaching_slab_slab_column').val();
	set_visibility(d2, v2);

	$('#id_attaching_slab_slab_column').change(function(event){
	    v2 = $(this).val();
	    set_visibility(d2, v2);
	});
	
    });
})(django.jQuery);
