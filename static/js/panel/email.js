'use strict';

var baseUrl = document.location.href;
var urlPath = 'api/statistics/email';
var jsonData;

$( document ).ready( function () {
	// preparación de la url api
	baseUrl = baseUrl.split('/');
	delete baseUrl[3];
	baseUrl = baseUrl.join('/')
	console.log( baseUrl + urlPath );

});

$( window ).on( 'resize', function () {
});

$( '#run_search' ).on( 'click', function () {

	var correo = $( "#correo" );

	if ( !correo.val() ) {
		alert( "Debes llenar el campo de correo que deseas buscar." );
		correo.focus();
		return false;
	} else {
		$( '#modalButton' ).click();

		$.ajax({
			'type': 'GET',
			'url': baseUrl + urlPath,
			//'dataType': 'json',
			'data': {
				'correo': correo.val(),
			},
			success: function ( data ) {
				jsonData = data;
				console.log( jsonData );
				if ( jsonData ) {
					console.log( jsonData );
					drawData( jsonData );
				};
				$( '#modalButton' ).click();
			},
			error: function ( jqXHR, textStatus, errorThrown ) {
				$( '#modalButton' ).click();
				console.log( errorThrown );
			},
		});

	};

});

function drawData ( data ) {
	var div = $( "#divData" );
	console.log( data );
	for ( var i in data ) {
		div.append(
			"<div class='well'>" + data[i] + "</div>"
		);
	};
};