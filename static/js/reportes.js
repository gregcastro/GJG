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


}); //Fin de document ready
