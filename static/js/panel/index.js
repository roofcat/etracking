'use strict';

google.load('visualization', '1.0', {'packages': ['corechart', 'table'], 'language': 'es'});

var baseUrl = document.location.href;
var urlPath = 'statistics';
//var urlPath = 'teststat';

$( document ).ready( function () {
	console.log( baseUrl );
	// Seteo de fecha actual
	setDefaultDates();

	var date_from = $( '#date_from' ).val( moment().subtract( 7, 'days' ).format( 'DD/MM/YYYY' ) );
	var date_to = $( '#date_to' ).val( moment().format( 'DD/MM/YYYY' ) );

	$( '.datePicker' ).datetimepicker ({
		dayOfWeekStart: 1,
		lang: 'es',
		timepicker: false,
		format: 'd/m/Y',
		formatDate: 'Y/m/d',
	});

});

$( '#run_search' ).on( 'click', function () {

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
		},
		error: function ( jqXHR, textStatus, errorThrown ) {
			console.log( errorThrown );
			console.log( jqXHR );
			console.log( textStatus );
		},
	});

});

function setBadgesDashboard ( data ) {
	$( 'span' ).empty();
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
		title: 'Gráfico de Actividad',
		is3D: true,
		width: 500,
		height: 500,
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