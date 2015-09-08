'use strict';

$.material.init();

$( '#menuControl' ).on( 'click', function () {
	var lateralMenu = $( '#menuPanel' );

	if ( lateralMenu.is( ':hidden' ) ) {
		lateralMenu.removeClass('hidden-xs hidden-sm');
	} else {
		lateralMenu.addClass('hidden-xs hidden-sm');
	};

});