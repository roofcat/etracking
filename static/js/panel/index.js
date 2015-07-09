'use strict';

google.load('visualization', '1.0', {'packages': ['corechart','line','table'], 'language': 'es'});

var baseUrl = document.location.href;
var urlPath = 'statistics';
var jsonData;

$( document ).ready( function () {
	// Seteo de fecha actual
	setDefaultDates();
	resetInputDates();
	//$("#options").dropdown();

	$( '.datePicker' ).datetimepicker ({
		'dayOfWeekStart': 1,
		'lang': 'es',
		'timepicker': false,
		'format': 'd/m/Y',
		'formatDate': 'Y/m/d',
	});
	// realizar carga por defecto
	$( "#run_search" ).click();
});
$( window ).on( 'resize', function () {
	drawJsonData();
});
function resetInputDates () {
	var date_from = $( '#date_from' ).val( moment().subtract( 7, 'days' ).format( 'DD/MM/YYYY' ) );
	var date_to = $( '#date_to' ).val( moment().format( 'DD/MM/YYYY' ) );
};
$( '#run_search' ).on( 'click', function () {
	hideAlertsMessages();
	
	var date_from = $( '#date_from' ).val();
	var date_to = $( '#date_to' ).val();
	var options = $( '#options' ).val();
	date_from = getDateAsTimestamp( date_from );
	date_to = getDateAsTimestamp( date_to );

	$.ajax({
		'type': 'GET',
		'url': baseUrl + urlPath,
		'dataType': 'json',
		'data': {
			'date_from': date_from,
			'date_to': date_to,
			'options': options,
		},
		success: function ( data ) {
			jsonData = data;
			drawJsonData();
			showSuccessMessage();
			$( '#modalButton' ).click();
		},
		error: function ( jqXHR, textStatus, errorThrown ) {
			console.log( errorThrown );
			showWarningMessage();
		},
	});
});
function drawJsonData () {
	setBadgesDashboard( jsonData.statistic );
	drawPieGraph( jsonData.statistic );
	drawLineGraph( jsonData.results );
};
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
function drawLineGraph ( datas ) {
	var data = new google.visualization.arrayToDataTable( datas );
	var options = {
		'title': 'Estadísticas',
		'vAxis': {
			'viewWindow': {
				'min': 0,
			},
		},
	};
	var chart = new google.visualization.LineChart( document.getElementById( 'divLineChart' ) );
	chart.draw( data, options );
};
function drawPieGraph ( data ) {
	var data = google.visualization.arrayToDataTable([
		[ 'Estadísticas', 'Correos' ],
		[ 'Enviados', data.delivered ],
		[ 'Rebotados', data.bounced ],
		[ 'Rechazados', data.dropped ],
		]);

	var options = {
		is3D: false,
		width: 300,
		height: 300,
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