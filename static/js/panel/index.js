'use strict';

google.load('visualization', '1.0', {'packages': ['corechart', 'table'], 'language': 'es'});

$( document ).ready( function () {

	$( '.datePicker' ).datetimepicker ({
		dayOfWeekStart: 1,
		lang: 'es',
		timepicker: false,
		format: 'd/m/Y',
		formatDate: 'Y/m/d',
	});

});