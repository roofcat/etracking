'use strict';

var baseUrl = document.location.href;
var urlUser = 'api/profile/user/update/';
var urlPass = 'api/profile/user/password/';
var tabPosition = '#general';

$( document ).ready( function () {
	baseUrl = baseUrl.split('/');
	delete baseUrl[4];
	delete baseUrl[3];
	baseUrl = baseUrl.join('/')
	baseUrl = baseUrl.substring( 0, baseUrl.length - 1 );
});

$( '.nav-tabs' ).on('click', 'a', function () {
	tabPosition = $( this ).attr( 'href' );
});

function ajaxService ( link, data ) {
	if ( link && data ) {
		$.ajax({
			'type': 'GET',
			'url': link,
			'data': data,
			success: function ( data ) {
				console.log( data );
				$( '#closeLoadingModal' ).click();
			},
			error: function ( jqXHR, textStatus, errorThrown ) {
				console.log( errorThrown );
				$( '#closeLoadingModal' ).click();
			},
		});
	};
};

$( 'button' ).on( 'click', function () {
	if ( !formValidate() ) {
		$( '#errorModal' ).modal( 'show', true );
		return;
	};
	//$( '#loadingModal' ).modal( 'show', true );
	
	switch ( tabPosition ) {
		case '#general':
			var first_name = $( '#first_name' ).val();
			var last_name = $( '#last_name' ).val();
			var data = {
				'first_name': first_name,
				'last_name': last_name,
			};

			var link = baseUrl + urlUser;
			ajaxService( link, data );
			break;

		case '#security':
			var old_pass = $( '#old_pass' ).val();
			var new_pass1 = $( '#new_pass1' ).val();
			var new_pass2 = $( '#new_pass2' ).val();
			var data = {
				'old_pass': old_pass,
				'new_pass1': new_pass1,
				'new_pass2': new_pass2,
			};
			var link = baseUrl + urlPass;
			ajaxService( link, data );
			break;
	};
});

function formValidate () {

	switch ( tabPosition ) {

		case '#general':
			var first_name = $( '#first_name' ).val();
			var last_name = $( '#last_name' ).val();
			if ( first_name && last_name ) {
				return true;
			} else {
				return false;
			};
			break;

		case '#security':
			var old_pass = $( '#old_pass' ).val();
			var new_pass1 = $( '#new_pass1' ).val();
			var new_pass2 = $( '#new_pass2' ).val();
			if ( old_pass && new_pass1 && new_pass2 ) {
				return true;
			} else {
				return false;
			};
			break;
	};

};