$(document).ready(function(){
    
  // items = ['POR PROCESAR', 'PROCESADO', 'EN RUTA', 'ENTREGADO'];

  // $('#sel').append($('<option>', {
  //   value: 1 ,
  //   text: items[0]
  // }));
  // $('#sel').append($('<option>', {
  //   value: 2 ,
  //   text: items[1]
  // }));
  // $('#sel').append($('<option>', {
  //   value: 3 ,
  //   text: items[2]
  // }));
  // $('#sel').append($('<option>', {
  //   value: 4 ,
  //   text: items[3]
  // }));

  // Cuando el paquete se quiere colocar como ENTREGADO entonces el campo "Locacion" debe desaparecer
  $('#sel').change(function() {

    var valor = $('#sel').val();
    
    if (valor == 4) {
      $('#locacion').hide();
      $('#locacion_label').hide();
    } else {
      $('#locacion').show();
      $('#locacion_label').show();
    }

  });

  // Buscar encargos en un intervalo de fechas dado
  $( "#botonBuscar" ).click(function() {

    if ($('#fecha1').val() == "" || $('#fecha2').val() == "") {
      alert("Los campos de fecha son requeridos");
    } else {
      $("#tab_logic tbody > tr").remove()
      var datearray = $('#fecha1').val().split("/");
      var newdate = datearray[1] + '/' + datearray[0] + '/' + datearray[2];
      var desde = new Date(newdate);
      datearray = $('#fecha2').val().split("/");
      newdate = datearray[1] + '/' + datearray[0] + '/' + datearray[2];
      var hasta = new Date(newdate);
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

                var date = new Date(solicitudes[i][4]);
                var fechaCompra = date.getDate() + '/' + (date.getMonth() + 1) + '/' +  date.getFullYear();
                date = new Date(solicitudes[i][5]);
                var fechaEstimada = date.getDate() + '/' + (date.getMonth() + 1) + '/' +  date.getFullYear();
                $('#tab_logic').append('<tr id="addr'+ i +'" onclick="editarSolicitud( '+solicitudes[i][0]+' )" style="cursor:pointer"></tr>');
                $('#addr'+i).html("<td>" + solicitudes[i][0] +"</td> "+
                  "<td> "+ solicitudes[i][1] +" </td><td> "+ solicitudes[i][2] +" </td><td> "+ solicitudes[i][3] +" </td>" +
                  "<td> "+ fechaCompra +" </td><td> "+ fechaEstimada +" </td><td> "+ solicitudes[i][6] +" </td><td> "+ solicitudes[i][7] +"</td>");
              }
              
          }
      });
    }

      

  });






}); //Fin de document ready


function editarSolicitud(tracking) {
  $('#tracking').val(tracking);

  var d = new Date();

  var month = d.getMonth()+1;
  var day = d.getDate();

  var fecha = d.getFullYear() + '/' +
      (month<10 ? '0' : '') + month + '/' +
      (day<10 ? '0' : '') + day;

  $('#fecha').val(fecha);


  $.ajax
    ({
        type:"GET" ,
        url: '/estatusEncargo?tracking='+tracking,
        dataType: "text",
        error: function (xhr, ajaxOptions, thrownError)
        {
            console.log(xhr.status); console.log(thrownError); console.log(ajaxOptions);
        },
        success: function(data)
        {    
            
            $("#sel").val(data);
            
        }
    });



  $('#editModal').modal('show');

}


