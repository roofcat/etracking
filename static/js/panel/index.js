'use strict';

google.load('visualization', '1.0', {'packages': ['corechart','line','table'], 'language': 'es'});

var baseUrl = document.location.href;
var urlPath = 'api/statistics/globalstats/';
var urlExport = 'export/stats/';
var jsonData;

$( document ).ready( function () {
	// Seteo de fecha actual
	setDefaultDates();
	resetInputDates();
	putDownloadLink();

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

// Validar los campos de fecha
$( 'input:text' ).on( 'change', function () {
	var date_from = $( '#date_from' ).val();
	var date_to = $( '#date_to' ).val();

	date_from = moment( date_from, 'DD/MM/YYYY' ).unix();
	date_to = moment( date_to, 'DD/MM/YYYY' ).unix();

	if ( date_from > date_to ) {
		resetInputDates();
	};
	putDownloadLink();
});

function resetInputDates () {
	var date_from = $( '#date_from' ).val( moment().subtract( 7, 'days' ).format( 'DD/MM/YYYY' ) );
	var date_to = $( '#date_to' ).val( moment().format( 'DD/MM/YYYY' ) );
};

function putDownloadLink () {
	var date_from = $( '#date_from' ).val();
	var date_to = $( '#date_to' ).val();
	var options = $( '#options' ).val();
	date_from = getDateAsTimestamp( date_from );
	date_to = getDateAsTimestamp( date_to );
	var link = baseUrl + urlExport + date_from + '/' + date_to + '/' + options + '/';
	$( '#export' ).attr('href', link );
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
		'url': baseUrl + urlPath + date_from + '/' + date_to + '/' + options + '/',
		'dataType': 'json',
		success: function ( data ) {
			jsonData = data;
			drawJsonData();
			showSuccessMessage();
			$( '#modalButton' ).click();
		},
		error: function ( jqXHR, textStatus, errorThrown ) {
			$( '#modalButton' ).click();
			showWarningMessage();
			console.log( errorThrown );
		},
	});
});

function drawJsonData () {
	if ( jsonData.statistic ) {
		setBadgesDashboard( jsonData.statistic );
		drawStatusPieGraph( jsonData.statistic );
	};
	if ( jsonData.results ) {
		drawLineGraph( jsonData.results );
	};
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
	var total = $( '#badgeTotal' ).empty().text( data.total );
	var processed = $( '#badgeProcessed' ).empty().text( data.processed );
	var delivered = $( '#badgeDelivered' ).empty().text( data.delivered );
	var opened = $( '#badgeOpened' ).empty().text( data.opened );
	var bounced = $( '#badgeBounced' ).empty().text( data.bounced );
	var dropped = $( '#badgeDropped' ).empty().text( data.dropped );
};

function drawLineGraph ( datas ) {
	var data = new google.visualization.arrayToDataTable( datas );
	var options = {
		'width': '85%',
		'height': '85%',
		'chartArea': {
			'left': "3%",
			'top': "3%",
			'height': "79%",
			'width': "79%",
		},
		'vAxis': {
			'viewWindow': {
				'min': 0,
			},
		},
		'legend': {
			'position': 'right',
		},
	};
	var chart = new google.visualization.LineChart( document.getElementById( 'divLineChart' ) );
	chart.draw( data, options );
};

function drawStatusPieGraph ( data ) {
	var data = google.visualization.arrayToDataTable([
		[ 'Estadísticas', 'Correos' ],
		[ 'Enviados', data.delivered ],
		[ 'Rebotados', data.bounced ],
		[ 'Rechazados', data.dropped ],
		]);

	var options = {
		'pieHole': 0.5,
		'width': '100%',
		'height': '100%',
		'forceIFrame': true,
		'chartArea': {
			'left': "3%",
			'top': "3%",
			'height': "94%",
			'width': "94%",
		},
		'legend': { 'position': 'none', },
	};

	var chart = new google.visualization.PieChart(document.getElementById( 'divStatusPieChart' ));
	chart.draw( data, options );
};

function getDateAsTimestamp ( date ) {
	return moment( date, 'DD/MM/YYYY' ).unix();
};

function setDefaultDates () {
	var date_from = $( '#date_from' ).val( moment().subtract( 7, 'days' ).format( 'DD/MM/YYYY' ) );
	var date_to = $( '#date_to' ).val( moment().format( 'DD/MM/YYYY' ) );
};