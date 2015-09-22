'use strict';

google.load('visualization', '1.0', {'packages': ['corechart','table', 'controls',], 'language': 'es'});

var baseUrl = document.location.href;
var emailUrl = 'api/search/email/';
var folioUrl = 'api/search/folio/';
var rutUrl = 'api/search/rut/';
var fallidosUrl = 'api/search/fallidos/';

var tabPosition = '#correo';

$( document ).ready( function () {

	baseUrl = baseUrl.split('/');
	delete baseUrl[4];
	delete baseUrl[3];
	baseUrl = baseUrl.join('/')
	baseUrl = baseUrl.substring( 0, baseUrl.length - 1 );
	console.log( baseUrl  );
	
	$( '.datePicker' ).datetimepicker ({
		'dayOfWeekStart': 1,
		'lang': 'es',
		'timepicker': false,
		'format': 'd/m/Y',
		'formatDate': 'Y/m/d',
	});

	setDefaultDates();
	
});

$( '#run_search' ).on( 'click', function () {

	if ( !formValidate() ) {
		$( '#errorModal' ).modal( 'show', true );
		return;
	};
	
	switch ( tabPosition ) {
		case '#correo':
			console.log(tabPosition);
			var date_from = $( '#date_from1' ).val();
			var date_to = $( '#date_to1' ).val();
			var correoDestinatario = $( '#correoDestinatario' ).val();

			date_from = getDateAsTimestamp( date_from );
			date_to = getDateAsTimestamp( date_to );
			correoDestinatario = encodeURIComponent( correoDestinatario );

			var link = baseUrl + emailUrl + date_from + '/' + date_to + '/' + correoDestinatario + '/';

			console.log( link );
			
			$.ajax({
				'type': 'GET',
				'url': link,
				success: function ( data ) {
					console.log( data['message'] );
					//loadData( data.data );
					drawTable( data.data );
				},
				error: function ( jqXHR, textStatus, errorThrown ) {
					console.log( errorThrown );
				},
			});

			break;
		case '#folio':
			console.log(tabPosition);
			var numeroFolio = $( '#numeroFolio' ).val();

			var link = baseUrl + folioUrl + '/' + numeroFolio;

			break;

		case '#rutreceptor':
			console.log(tabPosition);
			var date_from = $( '#date_from2' ).val();
			var date_to = $( '#date_to2' ).val();
			var rutReceptor = $( '#rutReceptor' ).val();

			date_from = getDateAsTimestamp( date_from );
			date_to = getDateAsTimestamp( date_to );

			if ( validaRut( rutReceptor ) ) {
				console.log("rut valido");
			};

			var link = baseUrl + rutUrl + '/' + date_from + '/' + date_to + '/' + rutReceptor + '/';

			break;

		case '#fallidos':
			console.log(tabPosition);
			var date_from = $( '#date_from3' ).val();
			var date_to = $( '#date_to3' ).val();

			date_from = getDateAsTimestamp( date_from );
			date_to = getDateAsTimestamp( date_to );

			var link = baseUrl + fallidosUrl + '/' + date_from + '/' + date_to + '/';

			break;
			
	};

	$( '#closeMenuModal' ).click();
});

function drawTable ( datas ) {
	var data = new google.visualization.DataTable();
	data.addColumn( 'string', 'Folio' );
	data.addColumn( 'string', 'Correo' );
	data.addColumn( 'string', 'Fecha Envío' );
	data.addColumn( 'string', 'Rut Receptor' );
	data.addColumn( 'string', 'Nombre Cliente' );
	data.addColumn( 'string', 'Rut Emisor' );
	data.addColumn( 'string', 'Nombre Emisor' );
	data.addColumn( 'string', 'Tipo Envío' );
	data.addColumn( 'string', 'Tipo DTE' );
	data.addColumn( 'string', 'Resolución Receptor' );
	data.addColumn( 'string', 'Resolución Emisor' );
	data.addColumn( 'number', 'Monto' );
	data.addColumn( 'string', 'Fecha Emisión' );
	data.addColumn( 'string', 'Fecha Recepción' );
	data.addColumn( 'string', 'Estado Documento' );
	data.addColumn( 'string', 'Tipo Operación' );
	data.addColumn( 'string', 'Tipo Receptor' );
	data.addColumn( 'string', 'Estado proceso' );
	data.addColumn( 'string', 'Fecha proceso' );
	data.addColumn( 'string', 'Estado envío' );
	data.addColumn( 'string', 'Fecha envío' );
	data.addColumn( 'string', 'Estado leído' );
	data.addColumn( 'string', 'Fecha leído' );
	data.addColumn( 'string', 'Ip leído' );
	data.addColumn( 'string', 'Nº lecturas' );
	data.addColumn( 'string', 'Estado rechazo' );
	data.addColumn( 'string', 'Fecha rechazo' );
	data.addColumn( 'string', 'Motivo rechazo' );
	data.addColumn( 'string', 'Estado rebote' );
	data.addColumn( 'string', 'Fecha rebote' );
	data.addColumn( 'string', 'Tipo rebote' );
	data.addColumn( 'string', 'Código rebote' );
	data.addColumn( 'string', 'Estado desuscrito' );
	data.addColumn( 'string', 'Fecha desuscrito' );

	var rows = new Array();

	for ( var i = 0; i < datas.length; i++ ) {
		var row = datas[i];
		rows.push([
			( !row.numero_folio ) ? '' : row.numero_folio, 
			( !row.correo ) ? '' : row.correo, 
			( !row.input_date ) ? '' : row.input_date, 
			( !row.rut_receptor ) ? '' : row.rut_receptor, 
			( !row.nombre_cliente ) ? '' : row.nombre_cliente, 
			( !row.rut_emisor ) ? '' : row.rut_emisor, 
			( !row.empresa ) ? '' : row.empresa, 
			( !row.tipo_envio ) ? '' : row.tipo_envio,
			( !row.tipo_dte ) ? '' : row.tipo_dte, 
			( !row.resolucion_receptor ) ? '' : row.resolucion_receptor, 
			( !row.resolucion_emisor ) ? '' : row.resolucion_emisor,
			( !row.monto ) ? 0 : parseInt( row.monto, 10 ), 
			( !row.fecha_emision ) ? '' : row.fecha_emision, 
			( !row.fecha_recepcion ) ? '' : row.fecha_recepcion, 
			( !row.estado_documento ) ? '' : row.estado_documento, 
			( !row.tipo_operacion ) ? '' : row.tipo_operacion, 
			( !row.tipo_receptor ) ? '' : row.tipo_receptor, 
			( !row.processed_event ) ? '' : row.processed_event, 
			( !row.processed_date ) ? '' : row.processed_date, 
			( !row.delivered_event ) ? '' : row.delivered_event, 
			( !row.delivered_date ) ? '' : row.delivered_date, 
			( !row.opened_event ) ? '' : row.opened_event, 
			( !row.opened_first_date ) ? '' : row.opened_first_date, 
			( !row.opened_ip ) ? '' : row.opened_ip, 
			( !row.opened_count ) ? '' : row.opened_count, 
			( !row.dropped_event ) ? '' : row.dropped_event, 
			( !row.dropped_date ) ? '' : row.dropped_date, 
			( !row.dropped_reason ) ? '' : row.dropped_reason, 
			( !row.bounce_event ) ? '' : row.bounce_event, 
			( !row.bounce_date ) ? '' : row.bounce_date, 
			( !row.bounce_type ) ? '' : row.bounce_type,
			( !row.bounce_status ) ? '' : row.bounce_status, 
			( !row.unsubscribe_event ) ? '' : row.unsubscribe_event, 
			( !row.unsubscribe_date ) ? '' : row.unsubscribe_date
		]);
	};

	data.addRows( rows );

	var formatCurrency = new google.visualization.NumberFormat({
		pattern: '$###.###',
	});

	formatCurrency.format( data, 11 );

	var options = {
		'showRowNumber': true,
		'width': '100%',
		'height': 400,
		'page': 'enable',
		'pageSize': 50,
		'allowHtml': true,
		'cssClassNames': {
			'headerCell': 'header-table',
			'tableCell': 'body-table',
		},
	};

	var table = new google.visualization.Table( document.getElementById( 'divCards' ) );
	table.draw( data, options );
};

function loadData ( data ) {
	var divCards = $( '#divCards' );
	var htmlCard = '';
	divCards.empty();

	for ( var i = 0; i < data.length; i++ ) {
		var correo = data[i];
		htmlCard += '<div class="col-xs-12 col-sm-6 col-md-6 col-lg-6">';
		htmlCard += '<div class="panel panel-material-deep-orange">';
		htmlCard += '<div class="panel-heading"> ';
		htmlCard += ' <strong>Folio Nº:</strong> ' + correo.numero_folio;
		htmlCard += ' <strong> Correo:</strong> ' + correo.correo;
		htmlCard += ' <strong> Fecha:</strong> ' + correo.input_date;
		htmlCard += ' </div>';
		htmlCard += '<div class="panel-body" style="font-size:12px;"> ';
		htmlCard += ' <strong>Rut receptor: </strong>' + correo.rut_receptor + ' - <strong>Cliente: </strong> ' +correo.nombre_cliente + '<br>';
	    htmlCard += ' <strong>Rut emisor: </strong>' + correo.rut_emisor + ' - <strong>Emisor: </strong> ' + correo.empresa + '<br>';
	    htmlCard += ' <strong>Tipo envío: </strong>' + correo.tipo_envio;
	    htmlCard += ' <strong>Tipo dte: </strong>' + correo.tipo_dte;
	    htmlCard += ' <strong>Resolución receptor: </strong> ';
	    if ( correo.resolucion_receptor ) { correo.resolucion_receptor };
    	htmlCard += ' <strong>Resolución emisor: </strong>' + correo.resolucion_emisor;
    	htmlCard += ' <strong>Monto: </strong>' + correo.monto;
    	htmlCard += ' <strong>Fecha emisión: </strong>' + correo.fecha_emision;
    	htmlCard += ' <strong>Fecha recepción: </strong>' + correo.fecha_recepcion;
    	htmlCard += ' <strong>Estado documento: </strong>' + correo.estado_documento;
    	htmlCard += ' <strong>Tipo operación: </strong>' + correo.tipo_operacion;
    	htmlCard += ' <strong>Tipo receptor: </strong>' + correo.tipo_receptor;
		htmlCard += ' <br> ';
		htmlCard += ' <strong>Estados del correo</strong><br> ';
		if ( correo.processed_event != 'None' ) {
			htmlCard += '<span class="label label-default"> ';
			htmlCard += correo.processed_event + ' - ' + correo.processed_date;
			htmlCard += ' </span><br> ';
		};
		if ( correo.delivered_event != 'None' ) {
			htmlCard += '<span class="label label-primary"> ';
			htmlCard += correo.delivered_event + ' - ' + correo.delivered_date;
			htmlCard += ' </span><br> ';
		};
		if ( correo.opened_event != 'None' ) {
			htmlCard += '<span class="label label-success"> ';
	    	htmlCard += correo.opened_event + ' - ' +  correo.opened_first_date + ' - ' + correo.opened_ip + ' - ';
		    htmlCard += correo.opened_user_agent + ' - ' + '<strong>Veces visto </strong>' + correo.opened_count;
			htmlCard += ' </span><br> ';
		};
		if ( correo.dropped_event != 'None' ) {
			htmlCard += '<span class="label label-warning"> ';
			htmlCard += correo.dropped_event + ' - ' + correo.dropped_reason + ' - ' + correo.dropped_date;
			htmlCard += ' </span><br> ';
		};					
		if ( correo.bounce_event != 'None' ) {
			htmlCard += '<span class="label label-danger"> ';
			htmlCard += correo.bounce_event + ' - ' + correo.bounce_date + ' - ' + correo.bounce_type + ' - ' + correo.bounce_status;
			htmlCard += ' </span><br>';
			htmlCard += '<p class="alert alert-danger">' + correo.bounce_reason + '</p><br> ';
		};
		if ( correo.unsubscribe_event != 'None' ) {
			htmlCard += '<span class="label label-info"> ';
		    htmlCard += correo.unsubscribe_event + ' - ' + correo.unsubscribe_date;
			htmlCard += ' </span>';
		};
		htmlCard += '<br>';
		htmlCard += '</div>';
		htmlCard += '</div>';
		htmlCard += '</div>';
	}; //endfor
	divCards.append( htmlCard );
};

function formValidate () {

	switch ( tabPosition ) {
		case '#correo':
			var date_from = $( '#date_from1' ).val();
			var date_to = $( '#date_to1' ).val();
			var correoDestinatario = $( '#correoDestinatario' ).val();
			if ( date_from && date_to && correoDestinatario ) {
				return true;
			} else {
				return false;
			};
			break;

		case '#folio':
			var numeroFolio = $( '#numeroFolio' ).val();
			if ( numeroFolio ) {
				return true;
			} else {
				return false;
			};
			break;

		case '#rutreceptor':
			var date_from = $( '#date_from2' ).val();
			var date_to = $( '#date_to2' ).val();
			var rutReceptor = $( '#rutReceptor' ).val();

			if ( date_from && date_to && rutReceptor ) {
				return true;
			} else {
				return false;
			};
			break;

		case '#fallidos':
			var date_from = $( '#date_from3' ).val();
			var date_to = $( '#date_to3' ).val();
			if ( date_from && date_to ) {
				return true;
			} else {
				return false;
			};
			break;
	};

};

function clearForm () {
	$( '#numeroFolio' ).val( '' );
	$( '#rutReceptor' ).val( '' );
	$( '#correoDestinatario' ).val( '' );
	setDefaultDates();
};

$( '#showMenu' ).on( 'click', function () {
	$( '#menuModal' ).modal( 'show', true );
});

$( '.datePicker' ).on( 'change', function () {
	var date_from = $( '#date_from' ).val();
	var date_to = $( '#date_to' ).val();

	date_from = moment( date_from, 'DD/MM/YYYY' ).unix();
	date_to = moment( date_to, 'DD/MM/YYYY' ).unix();

	if ( date_from > date_to ) {
		setDefaultDates();
	};
});

$( '.nav-pills' ).on('click', 'a', function () {
	tabPosition = $( this ).attr( 'href' );
	console.log( tabPosition );
});

// Validar los campos de fecha
$( '.datePicker' ).on( 'change', function () {
	var date_from1 = $( '#date_from1' ).val();
	var date_from2 = $( '#date_from2' ).val();
	var date_from3 = $( '#date_from3' ).val();
	var date_to1 = $( '#date_to1' ).val();
	var date_to2 = $( '#date_to2' ).val();
	var date_to3 = $( '#date_to3' ).val();

	date_from1 = moment( date_from1, 'DD/MM/YYYY' ).unix();
	date_from2 = moment( date_from2, 'DD/MM/YYYY' ).unix();
	date_from3 = moment( date_from3, 'DD/MM/YYYY' ).unix();
	date_to1 = moment( date_to1, 'DD/MM/YYYY' ).unix();
	date_to2 = moment( date_to2, 'DD/MM/YYYY' ).unix();
	date_to3 = moment( date_to3, 'DD/MM/YYYY' ).unix();

	if ( date_from1 > date_to1 ) {
		setDefaultDates();
	};

	if ( date_from2 > date_to2 ) {
		setDefaultDates();
	};

	if ( date_from3 > date_to3 ) {
		setDefaultDates();
	};
});

function getDateAsTimestamp ( date ) {
	return moment( date, 'DD/MM/YYYY' ).unix();
};

function setDefaultDates () {
	$( '#date_from1' ).val( moment().subtract( 7, 'days' ).format( 'DD/MM/YYYY' ) );
	$( '#date_from2' ).val( moment().subtract( 7, 'days' ).format( 'DD/MM/YYYY' ) );
	$( '#date_from3' ).val( moment().subtract( 7, 'days' ).format( 'DD/MM/YYYY' ) );
	$( '#date_to1' ).val( moment().format( 'DD/MM/YYYY' ) );
	$( '#date_to2' ).val( moment().format( 'DD/MM/YYYY' ) );
	$( '#date_to3' ).val( moment().format( 'DD/MM/YYYY' ) );
};

function validaRut ( rut ) {
  var rexp = new RegExp(/^([0-9])+\-([kK0-9])+$/);

  if ( rut.match( rexp ) ) {

    var RUT	= rut.split( "-" );
    var elRut = RUT[0].split( '' );
    var factor = 2;
    var suma = 0;
    var dv;
    
    for ( var i = ( elRut.length - 1 ); i >= 0; i-- ) {
      factor = factor > 7 ? 2 : factor;
      suma += parseInt( elRut[i], 10 ) * parseInt( factor++, 10 );
    };

    dv = 11 - ( suma % 11 );
    if ( dv == 11 ) {
      dv = 0;
    } else if ( dv == 10 ) {
      dv = "k";
    };

    if ( dv == RUT[1].toLowerCase() ) {
      //console.log( "El rut es valido." );
      return true;
    } else {
      alert( "El rut es incorrecto." );
      return false;
    };
  } else {
    alert( "Formato rut incorrecto. El formato es 12345678-9" );
    return false;
  };
};