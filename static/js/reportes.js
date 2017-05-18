$(document).ready(function(){

	$( "#boton_generar" ).click(function() {

		var desde = new Date( $('#fecha1').val() );
		var hasta = new Date( $('#fecha2').val() );

		desde = desde.getFullYear().toString() + '/' + (desde.getMonth()+1).toString() + '/' + desde.getDate().toString() ;
		hasta = hasta.getFullYear().toString() + '/' + (hasta.getMonth()+1).toString() + '/' + hasta.getDate().toString() ;

		console.log(desde);
  		console.log(hasta);

		valor_select = $('#tipo').val();
  		console.log(valor_select);

  		$("#solicitud_real").val(valor_select);
  		$("#desde_real").val(desde);
  		$("#hasta_real").val(hasta);
  		$("#formulario_real").submit();

	});


	$('#tipo').on('change', function() {

  		valor_select = $('#tipo').val();

		if (valor_select != "Solicitudes Despachadas" && valor_select != "Solicitudes Pendientes") {
			$('#fecha1').hide();
			$('#fecha2').hide();
			$('#span1').hide();
			$('#span2').hide();

		} else {
			$('#fecha1').show();
			$('#fecha2').show();
			$('#span1').show();
			$('#span2').show();
		}
	})






}); //Fin de document ready
