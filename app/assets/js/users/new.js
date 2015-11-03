'use strict';

$( 'form input' ).on( 'keyup', function () {
	var field = $( this );
	var type = $( this ).attr( 'type' );
	formValidation( field, type );
});

$( 'form input' ).on( 'click', function () {
	var field = $( this );
	var type = $( this ).attr( 'type' );
	formValidation( field, type );
});

function formValidation ( field, type ) {
	switch ( type ) {
		case 'text':
			textFieldValidation( field );
			break;
		case 'email':
			emailFieldValidation( field );
		break;
		case 'password':
			passwordFieldValidation();
			break;
	};
};

function textFieldValidation ( field ) {
	if ( $( field ).val().length > 0 ) {
		$( field ).parent().removeClass( 'has-error' ).addClass( 'has-success' );
		return true;
	} else {
		$( field ).parent().removeClass( 'has-success' ).addClass( 'has-error' );
		return false;
	};
};

function emailFieldValidation ( field ) {
	var regex = /[\w-\.]{2,}@([\w-]{2,}\.)*([\w-]{2,}\.)[\w-]{2,4}/;
	if ( regex.test( $( field ).val().trim() ) ) {
    	$( field ).parent().removeClass( 'has-error' ).addClass( 'has-success' );
    	return true;
	} else {
		$( field ).parent().removeClass( 'has-success' ).addClass( 'has-error' );
		return false;
	};
};

function passwordFieldValidation () {
	var password1 = $( '#password1' );
	var password2 = $( '#password2' );
	if ( password1.val() > 0 && password1.val() >0 && password1.val() ===  password2.val() ) {
		password1.parent().removeClass( 'has-error' ).addClass( 'has-success' );
		password2.parent().removeClass( 'has-error' ).addClass( 'has-success' );
		return true;
	} else {
		password1.parent().removeClass( 'has-success' ).addClass( 'has-error' );
		password2.parent().removeClass( 'has-success' ).addClass( 'has-error' );
		return false;
	};
};