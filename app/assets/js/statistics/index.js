'use strict';

google.load('visualization', '1.0', {'packages': ['corechart', 'table'], 'language': 'es'});

var url = "https://azurian-rastreo.appspot.com/admin/statistics/stats";
//var url = "http://localhost:8080/admin/statistics/stats";

$( document ).ready( function () {
	$( '#tabs' ).tabs();

	var dayDiv = $( 'dailyGraph' );
	var weeklyDiv = $( '#weeklyGraph' );
	var byweeklyDiv = $( '#byweekGraph' );
	var monthDiv = $( '#monthlyGraph' );
	var customDiv = $( '#cusomGraph' );

	var today = moment().unix();
	var week = moment().subtract( 7, 'days' ).unix();
	var byweek = moment().subtract( 15, 'days' ).unix();
	var month = moment().subtract( 30, 'days' ).unix();

	getData( week, today, weeklyDiv );
});

function loadGraph ( values ) {
	var data = google.visualization.arrayToDataTable([
		[ 'Estadísticas', 'Correos' ],
		[ 'Enviados', values.delivered ],
		[ 'Rebotados', values.bounced ],
		[ 'Rechazados', values.dropped ],
		]);

	var options = {
		title: 'Actividad',
		is3D: true,
		width: 500,
		height: 500,
	};

	var chart = new google.visualization.PieChart(document.getElementById( 'weeklyGraph' ));
	chart.draw( data, options );
};

function getData ( from, to, div ) {
	$.ajax({
		type: 'get',
		url: url,
		dataType: 'json',
		data: {
			'from_date': from,
			'to_date': to,
		},
		success: function ( data ) {
			loadGraph( data.week );
		},
		error: function ( jqXHR, textStatus, errorThrown ) {
			console.log( errorThrown );
		},
	});
};