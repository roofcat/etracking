'use strict';

//google.load('visualization', '1.0', {'packages': ['corechart','table', 'controls',], 'language': 'es'});

var baseUrl = document.location.href;
// urls busquedas
var emailUrl = 'api/search/email/';
var folioUrl = 'api/search/folio/';
var rutUrl = 'api/search/rut/';
var fallidosUrl = 'api/search/fallidos/';
var montosUrl = 'api/search/montos/';
// urls export
var emailExportUrl = '/export/email/';
var folioExportUrl = '/export/folio/';
var rutExportUrl = '/export/rut/';
var fallidosExportUrl = '/export/fallidos/';
var montosExportUrl = '/export/montos/';

var tabPosition = '#correo';

$( document ).ready( function () {

	baseUrl = baseUrl.split('/');
	delete baseUrl[4];
	delete baseUrl[3];
	baseUrl = baseUrl.join('/')
	baseUrl = baseUrl.substring( 0, baseUrl.length - 1 );
	
	$( '.datePicker' ).datetimepicker ({
		'dayOfWeekStart': 1,
		'lang': 'es',
		'timepicker': false,
		'format': 'd/m/Y',
		'formatDate': 'Y/m/d',
	});

	setDefaultDates();

	$( '#menuModal' ).modal( 'show', true );
	
});

$( '#run_search' ).on( 'click', function () {

	if ( !formValidate() ) {
		$( '#errorModal' ).modal( 'show', true );
		return;
	};

	$( '#closeMenuModal' ).click();
	$( '#loadingModal' ).modal( 'show', true );
	
	switch ( tabPosition ) {

		case '#correo':
			var date_from = $( '#date_from1' ).val();
			var date_to = $( '#date_to1' ).val();
			var correoDestinatario = $( '#correoDestinatario' ).val();

			date_from = getDateAsTimestamp( date_from );
			date_to = getDateAsTimestamp( date_to );
			correoDestinatario = encodeURIComponent( correoDestinatario );

			var link = baseUrl + emailUrl + date_from + '/' + date_to + '/' + correoDestinatario + '/';
			ajaxService( link );
			break;

		case '#folio':
			var numeroFolio = $( '#numeroFolio' ).val();

			var link = baseUrl + folioUrl + numeroFolio + '/';
			ajaxService( link );
			break;

		case '#rutreceptor':
			var date_from = $( '#date_from2' ).val();
			var date_to = $( '#date_to2' ).val();
			var rutReceptor = $( '#rutReceptor' ).val();

			date_from = getDateAsTimestamp( date_from );
			date_to = getDateAsTimestamp( date_to );

			if ( validaRut( rutReceptor ) ) {
				console.log("rut valido");
			};

			var link = baseUrl + rutUrl + date_from + '/' + date_to + '/' + rutReceptor + '/';
			ajaxService( link );
			break;

		case '#fallidos':
			var date_from = $( '#date_from3' ).val();
			var date_to = $( '#date_to3' ).val();

			date_from = getDateAsTimestamp( date_from );
			date_to = getDateAsTimestamp( date_to );

			var link = baseUrl + fallidosUrl + date_from + '/' + date_to + '/';
			ajaxService( link );
			break;

		case '#monto':
			var date_from = $( '#date_from4' ).val();
			var date_to = $( '#date_to4' ).val();
			date_from = getDateAsTimestamp( date_from );
			date_to = getDateAsTimestamp( date_to );

			var mount_from = $( '#mount_from' ).val();
			var mount_to = $( '#mount_to' ).val();
			mount_from = parseInt( mount_from, 10 );
			mount_to = parseInt( mount_to, 10 );

			var link = baseUrl + montosUrl + date_from + '/' + date_to + '/' + mount_from + '/' + mount_to + '/';
			ajaxService( link );
			break;
	};
});

function ajaxService ( link ) {
	$.ajax({
		'type': 'GET',
		'url': link,
		success: function ( data ) {
			if ( data.data ) {
				// Dibujar tabla de visualization
				//drawTable( data.data );
				// Dibujar tabla de jquery table
				drawJqueryTable( data.data );
			};
			$( '#closeLoadingModal' ).click();
		},
		error: function ( jqXHR, textStatus, errorThrown ) {
			console.log( errorThrown );
			$( '#closeLoadingModal' ).click();
		},
	});
};

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
			( !row.input_datetime ) ? '' : row.input_datetime, 
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
		'height': 450,
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

		case '#monto':
			var date_from = $( '#date_from4' ).val();
			var date_to = $( '#date_to4' ).val();
			var mount_from = $( '#mount_from' ).val();
			var mount_to = $( '#mount_to' ).val();
			if ( date_from && date_to && mount_from && mount_to ) {
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
});

// Validar los campos de fecha
$( '.datePicker' ).on( 'change', function () {
	var date_from1 = $( '#date_from1' ).val();
	var date_from2 = $( '#date_from2' ).val();
	var date_from3 = $( '#date_from3' ).val();
	var date_from4 = $( '#date_from4' ).val();
	var date_to1 = $( '#date_to1' ).val();
	var date_to2 = $( '#date_to2' ).val();
	var date_to3 = $( '#date_to3' ).val();
	var date_to4 = $( '#date_to4' ).val();

	date_from1 = moment( date_from1, 'DD/MM/YYYY' ).unix();
	date_from2 = moment( date_from2, 'DD/MM/YYYY' ).unix();
	date_from3 = moment( date_from3, 'DD/MM/YYYY' ).unix();
	date_from4 = moment( date_from4, 'DD/MM/YYYY' ).unix();
	date_to1 = moment( date_to1, 'DD/MM/YYYY' ).unix();
	date_to2 = moment( date_to2, 'DD/MM/YYYY' ).unix();
	date_to3 = moment( date_to3, 'DD/MM/YYYY' ).unix();
	date_to4 = moment( date_to4, 'DD/MM/YYYY' ).unix();

	if ( date_from1 > date_to1 ) {
		setDefaultDates();
	};

	if ( date_from2 > date_to2 ) {
		setDefaultDates();
	};

	if ( date_from3 > date_to3 ) {
		setDefaultDates();
	};

	if ( date_from4 > date_to4 ) {
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
	$( '#date_from4' ).val( moment().subtract( 7, 'days' ).format( 'DD/MM/YYYY' ) );
	$( '#date_to1' ).val( moment().format( 'DD/MM/YYYY' ) );
	$( '#date_to2' ).val( moment().format( 'DD/MM/YYYY' ) );
	$( '#date_to3' ).val( moment().format( 'DD/MM/YYYY' ) );
	$( '#date_to4' ).val( moment().format( 'DD/MM/YYYY' ) );
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

function drawJqueryTable ( data ) {
	$( '#tableCards' ).dataTable({
		"destroy": true,
		"scrollY": "450px",
		"scrollX": "100%",
		"scrollCollapse": true,
		"data": data,
		"searching": true,
		"lengthChange": false,
		"pageLength": 50,
		"columns": [
			{ 
				'data': 'numero_folio',
				'title': 'Folio',
			},
			{ 
				'data': 'correo',
				'title': 'Correo',
			},
			{ 
				'data': 'input_datetime',
				'title': 'Fecha envío',
				'render': function ( data, type, row, meta ) {
					return moment( data ).format( 'DD-MM-YYYY H:mm:ss' );
				},
			},
			{ 
				'data': 'rut_receptor',
				'title': 'Rut receptor',
			},
			{ 
				'data': 'nombre_cliente',
				'title': 'Nombre cliente',
			},
			{ 
				'data': 'rut_emisor',
				'title': 'Rut emisor',
			},
			{ 
				'data': 'empresa',
				'title': 'Nombre emisor',
			},
			{ 
				'data': 'tipo_envio',
				'title': 'Tipo envío',
			},
			{ 
				'data': 'tipo_dte',
				'title': 'Tipo DTE',
			},
			{ 
				'data': 'resolucion_receptor',
				'title': 'Resolucion receptor',
			},
			{ 
				'data': 'resolucion_emisor',
				'title': 'Resolucion emisor',
			},
			{ 
				'data': 'monto',
				'title': 'Monto',
				'render': function ( data, type, row, meta ) {
					return (!data) ? "$0.-" : "$" + data + ".-";
				},
			},
			{ 
				'data': 'fecha_emision',
				'title': 'Fecha emisión',
			},
			{ 
				'data': 'fecha_recepcion',
				'title': 'Fecha recepción',
			},
			{ 
				'data': 'estado_documento',
				'title': 'Estad documento',
			},
			{ 
				'data': 'tipo_operacion',
				'title': 'Tipo operación',
			},
			{ 
				'data': 'tipo_receptor',
				'title': 'Tipo receptor',
			},
			{ 
				'data': 'processed_event',
				'title': 'Estado proceso',
			},
			{ 
				'data': 'processed_date',
				'title': 'Fecha proceso',
			},
			{ 
				'data': 'delivered_event',
				'title': 'Estado envío',
			},
			{ 
				'data': 'delivered_date',
				'title': 'Fecha envío',
			},
			{ 
				'data': 'opened_event',
				'title': 'Estado leído',
			},
			{ 
				'data': 'opened_first_date',
				'title': 'Fecha leído',
			},
			{ 
				'data': 'opened_ip',
				'title': 'Ip lectura',
			},
			{ 
				'data': 'opened_count',
				'title': 'Nº lecturas',
			},
			{ 
				'data': 'dropped_event',
				'title': 'Estado rechazo',
			},
			{ 
				'data': 'dropped_date',
				'title': 'Fecha rechazo',
			},
			{ 
				'data': 'dropped_reason',
				'title': 'Motivo rechazo',
			},
			{ 
				'data': 'bounce_event',
				'title': 'Estado rebote',
			},
			{ 
				'data': 'bounce_date',
				'title': 'Fecha rebote',
			},
			{ 
				'data': 'bounce_type',
				'title': 'Tipo rebote',
			},
			{ 
				'data': 'bounce_status',
				'title': 'Código rebote',
			},
			{ 
				'data': 'unsubscribe_event',
				'title': 'Estado desuscrito',
			},
			{ 
				'data': 'unsubscribe_date',
				'title': 'Fecha desuscripción',
			},
		],
		"language": {
			"emptyTable": "No se encontraron registros.",
            "info": "Página _PAGE_ de _PAGES_",
            "infoEmpty": "No se encontraron registros.",
            "infoFiltered": "(Filtrado de _MAX_ registros).",
            "loadingRecords": "Cargando...",
            "paginate": {
            	"previous": "Anterior",
            	"next": "Siguiente",
            },
            "processing": "Proceso en curso.",
            "search": "Buscar",
            "zeroRecords": "No se encontraron registros.",
        },
	})
	.removeClass('display')
	.addClass('table table-hover table-striped table-condensed table-responsive');
};