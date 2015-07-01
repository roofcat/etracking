'use strict';

google.load('visualization', '1.0', {'packages': ['corechart', 'table'], 'language': 'es'});

var baseUrl = document.location.href;
var urlPath = 'statistics';
//var urlPath = 'teststat';

$( document ).ready( function () {
	console.log( baseUrl );
	// Seteo de fecha actual
	setDefaultDates();

	resetInputDates();

	$( '.datePicker' ).datetimepicker ({
		dayOfWeekStart: 1,
		lang: 'es',
		timepicker: false,
		format: 'd/m/Y',
		formatDate: 'Y/m/d',
	});

	// realizar carga por defecto
	$( "#run_search" ).click();

});

function resetInputDates () {
	var date_from = $( '#date_from' ).val( moment().subtract( 7, 'days' ).format( 'DD/MM/YYYY' ) );
	var date_to = $( '#date_to' ).val( moment().format( 'DD/MM/YYYY' ) );
};

$( '#run_search' ).on( 'click', function () {

	hideAlertsMessages();

	var date_from = $( '#date_from' ).val();
	var date_to = $( '#date_to' ).val();

	//if ( date_from && date_to )
	date_from = getDateAsTimestamp( date_from );
	date_to = getDateAsTimestamp( date_to );

	$.ajax({
		type: 'GET',
		url: baseUrl + urlPath,
		dataType: 'json',
		data: {
			'date_from': date_from,
			'date_to': date_to,
		},
		success: function ( data ) {
			console.log( baseUrl + urlPath )
			console.log( data );
			setBadgesDashboard( data.statistic );
			drawPieGraph( data.statistic );
			showSuccessMessage();
		},
		error: function ( jqXHR, textStatus, errorThrown ) {
			console.log( errorThrown );
			console.log( jqXHR );
			console.log( textStatus );
			showWarningMessage();
		},
	});

});

function showSuccessMessage () {
	$( "#successMessage" ).show();
};

function showWarningMessage () {
	$( "#warningMessage" ).show();
};

function hideAlertsMessages () {
	$( "#warningMessage" ).hide();
	$( "#successMessage" ).hide();
};

function setBadgesDashboard ( data ) {
	$( 'span.badge' ).empty();
	var total = $( '#badgeTotal' ).text( data.total );
	var processed = $( '#badgeProcessed' ).text( data.processed );
	var delivered = $( '#badgeDelivered' ).text( data.delivered );
	var opened = $( '#badgeOpened' ).text( data.opened );
	var bounced = $( '#badgeBounced' ).text( data.bounced );
	var dropped = $( '#badgeDropped' ).text( data.dropped );
};

function drawPieGraph ( data ) {
	var data = google.visualization.arrayToDataTable([
		[ 'Estadísticas', 'Correos' ],
		[ 'Enviados', data.delivered ],
		[ 'Rebotados', data.bounced ],
		[ 'Rechazados', data.dropped ],
		]);

	var options = {
		is3D: true,
		width: 400,
		height: 400,
	};

	var chart = new google.visualization.PieChart(document.getElementById( 'divPieChart' ));
	chart.draw( data, options );
};

function getDateAsTimestamp ( date ) {
	return moment( date, 'DD/MM/YYYY' ).unix();
};
function setDefaultDates () {
	var date_from = $( '#date_from' ).val( moment().subtract( 7, 'days' ).format( 'DD/MM/YYYY' ) );
	var date_to = $( '#date_to' ).val( moment().format( 'DD/MM/YYYY' ) );
};