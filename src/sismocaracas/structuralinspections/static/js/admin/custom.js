function set_visibility(d, v)
{
    // console.log(v);
    for each(var f in d[v])
	f[0][f[1]]('slow');
}

(function($) {
    $(document).ready(function($) {
	console.log('HOLA');
	alert("HOLA");
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
    });
})(django.jQuery);
