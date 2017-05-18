$(document).ready(function(){
  
$( "#botonBuscar" ).click(function() {

  // Si se presiona el boton y una fecha no se selecciono entonces se indica (ambas fechas son requeridas)
  // Arreglar las fechas que se muestran en la tabla..
  $("#tab_logic tbody > tr").remove()
  var desde = new Date( $('#fecha1').val() );
  var hasta = new Date( $('#fecha2').val() );
  console.log("fecha 1 = " + desde );
  console.log("fecha 2 = " + hasta );


  desde = desde.getFullYear().toString() + '/' + (desde.getMonth()+1).toString() + '/' + desde.getDate().toString() ;
  hasta = hasta.getFullYear().toString() + '/' + (hasta.getMonth()+1).toString() + '/' + hasta.getDate().toString() ;

  console.log(desde);
  console.log(hasta);

  valor_select = $('#sel_solicitudes').val();
  console.log(valor_select);

  
  $.ajax
  ({
      type:"GET" ,
      url: '/solicitudes-admin?desde='+desde+'&hasta='+hasta+'&tipo='+valor_select,
      dataType: "text",
      error: function (xhr, ajaxOptions, thrownError)
      {
          console.log(xhr.status); console.log(thrownError); console.log(ajaxOptions);
      },
      success: function(data)
      {    
          console.log(data);
          solicitudes = jQuery.parseJSON(data);
          console.log(solicitudes);
          var N = solicitudes.length;

          for (var i = 0; i < N; i++) {
            $('#tab_logic').append('<tr id="addr'+ i +'" onclick="editarSolicitud( '+solicitudes[i][0]+' )" style="cursor:pointer"></tr>');
            $('#addr'+i).html("<td>" + solicitudes[i][0] +"</td> "+
              "<td> "+ solicitudes[i][1] +" </td><td> "+ solicitudes[i][2] +" </td><td> "+ solicitudes[i][3] +" </td>" +
              "<td> "+ solicitudes[i][4] +" </td><td> "+ solicitudes[i][5] +" </td><td> "+ solicitudes[i][6] +" </td><td> "+ solicitudes[i][7] +"</td>");
          }
          

          



      }
  });

});



}); //Fin de document ready


function editarSolicitud(tracking) {

  // Aqui deberia insertar dinamicamente las opciones en el select
  // Por ahora lo hago cableado..

  items = ['POR PROCESAR', 'PROCESADO', 'EN RUTA', 'ENTREGADO'];



  $('#sel').append($('<option>', {
    value: 1 ,
    text: items[0]
  }));
  $('#sel').append($('<option>', {
    value: 2 ,
    text: items[1]
  }));
  $('#sel').append($('<option>', {
    value: 3 ,
    text: items[2]
  }));
  $('#sel').append($('<option>', {
    value: 4 ,
    text: items[3]
  }));

  $('#tracking').val(tracking);

  // $('#myModal').modal('toggle');
  $('#editModal').modal('show');
  // $('#myModal').modal('hide');

  console.log($('#sel').val() );



}


