/*
quotation.js
*/

            var msg="Hello Javascript2";
                    console.log(msg);

                    // Store
localStorage.lastname = "Smith";
// Retrieve
 console.log(localStorage.lastname);
/*
$(window).on("unload", function(){
  alert('Bye.');
});
*/
$(function () {


   $('.updateabletbldoc').change(function() {

        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        var fieldvalue = $(this).val();
        var docid = $('#entrydocid').text();
        var fieldname = $(this).attr( "name" );
        var tbl="tblDoc";

          $.ajax({
            type: 'POST',
            url: '',

            data: {
           'tbl' : tbl,
           'fieldvalue': fieldvalue,
           'rowid' : 0,
           'docid' : docid,
           'fieldname': fieldname,
           'csrfmiddlewaretoken': CSRFtoken,
           },
           success: updatesuccess,
           error: updateerror,
           datatype: 'html'
          });

        function updatesuccess (data, textStatus, jqXHR){
            console.log('datafromsql:' + data);
            $('input[name="' + fieldname + '"][docid="' + docid + '"').val(data);
            $('#sqlsaving').html('<span  class="glyphicon glyphicon-hdd"></span>');

            setTimeout(
              function()
              {
                $('#sqlsaving').html("");

              }, 500);
            console.log(fieldvalue);
        };
        function updateerror (){
            console.log('Failure in saving');
        };


   });
   $('.selection').change(function() {

        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        var fieldvalue = $(this).val();
        var entrydocid = $('#entrydocid').text();
        var fieldnameclone = $(this).attr( "fieldnameclone" );
        var fieldnameto = $(this).attr( "fieldnameto" );

            $.ajax({
            type: 'POST',
            url: 'accountentryuniversalselections/',

            data: {
           'fieldvalue': fieldvalue,
           'entrydocid' : entrydocid,
           'fieldnameto': fieldnameto,
           'csrfmiddlewaretoken': CSRFtoken,
           },
           success: updatesuccess,
           error: updateerror,
           datatype: 'html'
          });

        function updatesuccess (data, textStatus, jqXHR){
            console.log('datafromsql:' + data);
            var fromsql= data[0]

            $('select[class="selection"][fieldnameto="' + fieldnameto + '"] option:selected').html(fromsql);


            $('#sqlsaving').html('<span  class="glyphicon glyphicon-hdd"></span>');

            setTimeout(
              function()
              {
                $('#sqlsaving').html("");

              }, 500);

        };
        function updateerror (){
            console.log('Failure in saving');
        };

   });

});