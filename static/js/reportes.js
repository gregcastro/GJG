$(document).ready(function(){

	$( "#boton_generar" ).click(function() {

		valor_select = $('#tipo').val();
  		console.log(valor_select);

  		select_fecha = $('#select_fecha').val();

  		if (valor_select == "Solicitudes Despachadas" || valor_select == "Solicitudes Pendientes") {
  			
  			$("#tipo_fecha").val(select_fecha);

  			if (select_fecha == 'Intervalo de Tiempo') {

  				if ($('#fecha1').val() == "" || $('#fecha2').val() == "") {
			      alert("Los campos de fecha son requeridos");
			    } else {
	  				var desde = new Date( $('#fecha1').val() );
					var hasta = new Date( $('#fecha2').val() );

					desde = desde.getFullYear().toString() + '/' + (desde.getMonth()+1).toString() + '/' + desde.getDate().toString() ;
					hasta = hasta.getFullYear().toString() + '/' + (hasta.getMonth()+1).toString() + '/' + hasta.getDate().toString() ;


			  		$("#desde_real").val(desde);
		  			$("#hasta_real").val(hasta);
		  			$("#solicitud_real").val(valor_select);
  					$("#formulario_real").submit();

		  		}

  			} else if (select_fecha == 'Día') {

  				if ($('#fecha1').val() == "") {
  					alert("El campo de fecha es requerido");
  				} else {
	  				var fecha = new Date( $('#fecha1').val() );

	  				fecha = fecha.getFullYear().toString() + '/' + (fecha.getMonth()+1).toString() + '/' + fecha.getDate().toString() ;
	  				$("#desde_real").val(fecha);
	  				$("#solicitud_real").val(valor_select);
	  				$("#formulario_real").submit();

	  			}

  			} else if (select_fecha == 'Mes') {

  				if ($('#fecha3').val() == "") {
  					alert("El campo de fecha es requerido");
  				} else {
	  				var fecha = $('#fecha3').val();

	  				desde = fecha + '/01';
	  				hasta = fecha + '/31';

	  				// console.log(desde + ' ' + hasta);

	  				$("#desde_real").val(desde);
	  				$("#hasta_real").val(hasta);
	  				$("#solicitud_real").val(valor_select);
	  				$("#formulario_real").submit();

  				}

  			} else if (select_fecha == 'Año') {

  				if ($('#fecha4').val() == "") {
  					alert("El campo de fecha es requerido");
  				} else {
	  				var fecha = $('#fecha4').val();

	  				desde = fecha + '/01/01';
	  				hasta = fecha + '/12/31';

	  				// console.log(desde + ' ' + hasta);

	  				$("#desde_real").val(desde);
	  				$("#hasta_real").val(hasta);
	  				$("#solicitud_real").val(valor_select);
	  				$("#formulario_real").submit();

  				}

  			}

  		} 
  		
	});

	$( "#boton_generar_aux" ).click(function() {

		valor_select = $('#tipo').val();
  		console.log(valor_select);

  		select_fecha = $('#select_fecha').val();

  		if (valor_select == "Solicitudes Despachadas" || valor_select == "Solicitudes Pendientes") {
  			
  			$("#tipo_fecha").val(select_fecha);

  			if (select_fecha == 'Intervalo de Tiempo') {
  				var desde = new Date( $('#fecha1').val() );
				var hasta = new Date( $('#fecha2').val() );

				desde = desde.getFullYear().toString() + '/' + (desde.getMonth()+1).toString() + '/' + desde.getDate().toString() ;
				hasta = hasta.getFullYear().toString() + '/' + (hasta.getMonth()+1).toString() + '/' + hasta.getDate().toString() ;


		  		$("#desde_real").val(desde);
	  			$("#hasta_real").val(hasta);

  			} else if (select_fecha == 'Día') {
  				var fecha = new Date( $('#fecha1').val() );

  				fecha = fecha.getFullYear().toString() + '/' + (fecha.getMonth()+1).toString() + '/' + fecha.getDate().toString() ;
  				$("#desde_real").val(fecha);

  			} else if (select_fecha == 'Mes') {

  				var fecha = $('#fecha3').val();

  				desde = fecha + '/01';
  				hasta = fecha + '/31';

  				// console.log(desde + ' ' + hasta);

  				$("#desde_real").val(desde);
  				$("#hasta_real").val(hasta);

  			} else if (select_fecha == 'Año') {

  				var fecha = $('#fecha4').val();

  				desde = fecha + '/01/01';
  				hasta = fecha + '/12/31';

  				// console.log(desde + ' ' + hasta);

  				$("#desde_real").val(desde);
  				$("#hasta_real").val(hasta);

  			}

  		} 

  		$("#solicitud_real").val(valor_select);
  		$("#formulario_real").submit();

	});


	$('#tipo').on('change', function() {

  		valor_select = $('#tipo').val();

		if (valor_select != "Solicitudes Despachadas" && valor_select != "Solicitudes Pendientes") {
			$('#fecha1').hide();
			$('#fecha2').hide();
			$('#span1').hide();
			$('#span2').hide();
			$('#date1').hide();
			$('#date2').hide();
			$('#rango_fechas').hide();	
			$('#select_fecha').hide();
			$('#boton_generar').hide();
			$('#boton_generar_aux').show();
		} else {
			$('#fecha1').show();
			$('#fecha2').show();
			$('#span1').show();
			$('#span2').show();
			$('#date1').show();
			$('#date2').show();
			$('#rango_fechas').show();			
			$('#select_fecha').show();
			$('#boton_generar').show();
			$('#boton_generar_aux').hide();
		}
	})


	$('#select_fecha').on('change', function() {

  		valor_select = $('#select_fecha').val();

		if (valor_select == "Día") {
			$('#fecha1').show();
			$('#span1').show();
			$('#date1').show();

			$('#fecha2').hide();
			$('#span2').hide();
			$('#date2').hide();

			$('#fecha3').hide();
			$('#span3').hide();
			$('#date3').hide();

			$('#fecha4').hide();
			$('#span4').hide();
			$('#date4').hide();

		}else if (valor_select == "Intervalo de Tiempo") {
			$('#fecha1').show();
			$('#span1').show();
			$('#date1').show();

			$('#fecha2').show();
			$('#span2').show();
			$('#date2').show();

			$('#fecha3').hide();
			$('#span3').hide();
			$('#date3').hide();

			$('#fecha4').hide();
			$('#span4').hide();
			$('#date4').hide();

			
		} else if (valor_select == "Mes") {

			$('#fecha3').show();
			$('#span3').show();
			$('#date3').show();

			$('#fecha1').hide();
			$('#span1').hide();
			$('#date1').hide();

			$('#fecha2').hide();
			$('#span2').hide();
			$('#date2').hide();

			$('#fecha4').hide();
			$('#span4').hide();
			$('#date4').hide();

		} else {
			$('#fecha3').hide();
			$('#span3').hide();
			$('#date3').hide();

			$('#fecha1').hide();
			$('#span1').hide();
			$('#date1').hide();

			$('#fecha2').hide();
			$('#span2').hide();
			$('#date2').hide();

			$('#fecha4').show();
			$('#span4').show();
			$('#date4').show();

		}

	})






}); //Fin de document ready
