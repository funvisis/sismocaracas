(function($) {
    $(document).ready(function($) {
	$('.ground_slope').hide('slow');
	$('.ground_over').hide('slow');
	$('.talus_slope').hide('slow');
	$('.talus_separation_gt_H').hide('slow');
	$('#id_building_at').change(function(event){
	    // console.log($(this).val());
	    switch($(this).val()){
	    case 'Planicie':
		$('.ground_slope').hide('slow');
		$('.ground_over').hide('slow');
		$('.talus_slope').hide('slow');
		$('.talus_separation_gt_H').hide('slow');
		break;
	    case 'Ladera':
		$('.ground_slope').show('slow');
		$('.ground_over').show('slow');
		$('.talus_slope').hide('slow');
		$('.talus_separation_gt_H').hide('slow');
		break;
	    case 'Base':
	    case 'Cima':
		$('.ground_slope').hide('slow');
		$('.ground_over').hide('slow');
		$('.talus_slope').show('slow');
		$('.talus_separation_gt_H').show('slow');
		break;
	    }
	});
    });
})(django.jQuery);

// $(document).ready(function(){
//     alert("It Worked");
// });

