var today = new Date();
var url = "http://rastreo-azurian.appspot.com";

google.load('visualization', '1.0', {'packages': ['corechart', 'table'], 'language': 'es'});


$( document ).ready( function () {
	$.ajax({
		type: 'GET',
		url: url + '/admin/users/list',
		success: function ( data ) {
			//google.setOnLoadCallback(load);
			console.log(data);
		},
		error: function ( jqXHR, textStatus, errorThrown ) {
			console.log( errorThrown );
		},
	});
});
/*
function load () {
	console.log("me llamaron");
	var data = google.visualization.arrayToDataTable(data);
	var options = {
		title: "Estadística Total"
	};
	var chart = new google.visualization.PieChart(document.getElementById('piechart'));
	chart.draw(data, options);
};
*/