'use strict';

var API_URL = 'https://azurian-rastreo.appspot.com/testcursor/';

$(document).ready( function () {
	drawJqueryTable();
});

function drawJqueryTable () {
	$( '#tableCards' ).dataTable({
		"processing": true,
		//"ajax": API_URL,
		"ajaxSource": API_URL,
		//"lengthChange": false,
		//"pageLength": 50,
		//"paging": true,
		"scrollCollapse": true,
		"scrollX": "100%",
		"scrollY": "450px",
		//"searching": true,
		"serverSide": true,
		//"destroy": true,
		"columns": [
			{
				'title': 'Resumen de envío',
				'render': function ( data, type, row, meta ) {
					var popBody = '<div style="font-size:11px;">';
					var rowBody = "";
					if ( row['processed_event'] ) {
						rowBody += "<span class='label label-default'> </span>&nbsp;";
						popBody += '<p><span class="label label-default"> </span>&nbsp;';
						popBody += ' Procesado el ' + row['processed_date'] + '</p>';
					};
					if ( row['delivered_event'] ) {
						rowBody += "<span class='label label-primary'> </span>&nbsp;";
						popBody += '<p><span class="label label-primary"> </span>&nbsp;';
						popBody += ' Enviado el ' + row['delivered_date'] + '</p>';
					};
					if ( row['opened_event'] ) {
						rowBody += "<span class='label label-success'> </span>&nbsp;";
						popBody += '<p><span class="label label-success"> </span>&nbsp;';
						popBody += ' Leído el ' + row['opened_first_date'] + '<br>';
						popBody += ' IP ' + row['opened_ip'] + ' ' + row['opened_count'] + ' veces.</p>';
					};
					if ( row['dropped_event'] ) {
						rowBody += "<span class='label label-warning'> </span>&nbsp;";
						popBody += '<p><span class="label label-warning"> </span>&nbsp;';
						popBody += ' Rechazado el ' + row['dropped_date'] + '<br> ';
						popBody += ' Motivo: ' + row['dropped_reason'] + '</p>';
					};
					if ( row['bounce_event'] ) {
						rowBody += "<span class='label label-danger'> </span>&nbsp;";
						popBody += '<p><span class="label label-danger"> </span>&nbsp;';
						popBody += ' Rebotado el ' + row['bounce_date'] + '<br> ';
						popBody += ' Motivo: ' + row['bounce_reason'] + '</p>';
					};
					if ( row['unsubscribe_event'] ) {
						rowBody += "<span class='label label-info'> </span>&nbsp;";
						popBody += '<p><span class="label label-info"> </span>&nbsp;';
						popBody += ' Desuscrito el ' + row['dropped_date'] + '</p>';
					};
					popBody += '</div>';
					var html = "<div id='divPopOver' rel='popover' data-animation='true' data-trigger='hover' " + 
								" data-html='true' data-placement='right' data-container='body' " + 
								"data-toggle='popover' data-content='" + popBody + "'>" + rowBody + "</div>";
					return html;
				},
			},
			{
				'data': 'attachs',
				'title': 'Adjuntos',
				'render': function ( data, type, row, meta ) {
					var html = '<div style="font-size:11px;">';
					for ( var i in data ) {
						var attach = data[i];
						html += '<a href="' + attach + '/" title="Ver archivo adjunto" target="_blank"><span class="mdi-editor-attach-file"></span></a>';
					};
					html += '</div>';
					return html;
				},
			},
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
					return ( !data ) ? "" : moment( data ).format( 'DD-MM-YYYY H:mm:ss' );
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
					return ( !data ) ? "$0.-" : "$" + data + ".-";
				},
			},
			{ 
				'data': 'fecha_emision',
				'title': 'Fecha emisión',
				'render': function ( data, type, row, meta ) {
					return ( !data ) ? "" : moment( data ).format( 'DD-MM-YYYY H:mm:ss' );
				},
			},
			{ 
				'data': 'fecha_recepcion',
				'title': 'Fecha recepción',
				'render': function ( data, type, row, meta ) {
					return ( !data ) ? "" : moment( data ).format( 'DD-MM-YYYY H:mm:ss' );
				},
			},
			{ 
				'data': 'estado_documento',
				'title': 'Estado documento',
			},
			{ 
				'data': 'tipo_operacion',
				'title': 'Tipo operación',
			},
			{ 
				'data': 'tipo_receptor',
				'title': 'Tipo receptor',
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
            "processing": "Cargando, espere...",
            "search": "Buscar",
            "zeroRecords": "No se encontraron registros.",
        },
	})
	.removeClass('display')
	.addClass('table table-hover table-striped table-condensed table-responsive');
};