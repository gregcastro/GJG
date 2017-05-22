$(document).ready(function(){
 
  // Buscar logs en un intervalo de fechas dado
  $( "#botonBuscar" ).click(function() {

    if ($('#fecha1').val() == "" || $('#fecha2').val() == "") {

      $("#dialog").dialog("open");

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

      $.ajax
      ({
          type:"GET" ,
          url: '/get-logs?desde='+desde+'&hasta='+hasta,
          dataType: "text",
          error: function (xhr, ajaxOptions, thrownError)
          {
              console.log(xhr.status); console.log(thrownError); console.log(ajaxOptions);
          },
          success: function(data)
          {    
              console.log(data);
              logs = jQuery.parseJSON(data);
              console.log(logs);
              var N = logs.length;

              for (var i = 0; i < N; i++) {

                var date = new Date(logs[i][3]);
                var fecha = date.getDate() + '/' + (date.getMonth() + 1) + '/' +  date.getFullYear();
                $('#tab_logic').append('<tr id="addr'+ i +'"></tr>');
                $('#addr'+i).html("<td>" + fecha +"</td> "+
                  "<td> "+ logs[i][0] +" </td><td> "+ logs[i][1] +" </td><td> "+ logs[i][2] +"</td>");
              }
              
          }
      });      
        
    }

  });

}); //Fin de document ready