'use strict';

var baseUrl = document.location.href;
var emailUrl = 'api/search/';
var folioUrl = 'api/search/';
var rutUrl = 'api/search/';
var fallidosUrl = 'api/search/';

var tabPosition = '#correo';

$( document ).ready( function () {

	console.log( baseUrl );
	baseUrl = baseUrl.split('/');
	delete baseUrl[4];
	delete baseUrl[3];
	baseUrl = baseUrl.join('/')
	baseUrl = baseUrl.substring( 0, baseUrl.length - 1 );
	console.log( baseUrl  );
	
	$( '.datePicker' ).datetimepicker ({
		'dayOfWeekStart': 1,
		'lang': 'es',
		'timepicker': false,
		'format': 'd/m/Y',
		'formatDate': 'Y/m/d',
	});

	setDefaultDates();
	
});

$( '#run_search' ).on( 'click', function () {

	if ( !formValidate() ) {
		$( '#errorModal' ).modal( 'show', true );
		return;
	};
	
	switch ( tabPosition ) {
		case '#correo':
			console.log(tabPosition);
			var date_from = $( '#date_from' ).val();
			var date_to = $( '#date_to' ).val();
			var correoDestinatario = $( '#correoDestinatario' ).val();
			break;
		case '#folio':
			console.log(tabPosition);
			var numeroFolio = $( '#numeroFolio' ).val();
			break;
		case '#rutreceptor':
			console.log(tabPosition);
			var date_from = $( '#date_from' ).val();
			var date_to = $( '#date_to' ).val();
			var rutReceptor = $( '#rutReceptor' ).val();
			break;
		case '#fallidos':
			console.log(tabPosition);
			var date_from = $( '#date_from' ).val();
			var date_to = $( '#date_to' ).val();
			break;
	};

	$( '#closeMenuModal' ).click();
});

function formValidate () {

	switch ( tabPosition ) {
		case '#correo':
			var date_from = $( '#date_from' ).val();
			var date_to = $( '#date_to' ).val();
			var correoDestinatario = $( '#correoDestinatario' ).val();
			if ( date_from && date_to && correoDestinatario ) {
				return true;
			} else {
				return false;
			};
			break;
		case '#folio':
			var numeroFolio = $( '#numeroFolio' ).val();
			if ( numeroFolio ) {
				return true;
			} else {
				return false;
			};
			break;
		case '#rutreceptor':
			var date_from = $( '#date_from' ).val();
			var date_to = $( '#date_to' ).val();
			var rutReceptor = $( '#rutReceptor' ).val();

			if ( date_from && date_to && rutReceptor ) {
				return true;
			} else {
				return false;
			};
			break;
		case '#fallidos':
			var date_from = $( '#date_from' ).val();
			var date_to = $( '#date_to' ).val();
			if ( date_from && date_to ) {
				return true;
			} else {
				return false;
			};
			break;
	};

};

function clearForm () {
	$( '#numeroFolio' ).val( '' );
	$( '#rutReceptor' ).val( '' );
	$( '#correoDestinatario' ).val( '' );
	setDefaultDates();
};

$( '#showMenu' ).on( 'click', function () {
	$( '#menuModal' ).modal( 'show', true );
});

$( '.datePicker' ).on( 'change', function () {
	var date_from = $( '#date_from' ).val();
	var date_to = $( '#date_to' ).val();

	date_from = moment( date_from, 'DD/MM/YYYY' ).unix();
	date_to = moment( date_to, 'DD/MM/YYYY' ).unix();

	if ( date_from > date_to ) {
		setDefaultDates();
	};
});

$( '.nav-pills' ).on('click', 'a', function () {
	tabPosition = $( this ).attr( 'href' );
	console.log( tabPosition );
});

function setDefaultDates () {
	var date_from = $( '#date_from' ).val( moment().subtract( 7, 'days' ).format( 'DD/MM/YYYY' ) );
	var date_to = $( '#date_to' ).val( moment().format( 'DD/MM/YYYY' ) );
};