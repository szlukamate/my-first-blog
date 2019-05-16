/*
pohandler.js
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
            setTimeout(
              function()
              {

                    $('#aux1').trigger('click');
              }, 500);

    $('#aux1').click(function() {
            setTimeout(
              function()
              {
                    $.ajax({
                        type: 'POST',
                        url: 'pohandlerrowsourceforarrivaldates',

                        data: {
                        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                        },

                        success: ArrivaldatesSuccess,
                        error: function(){
                            alert('failure');
                        },
                        datatype: 'html'

                    });
              }, 500);

            function ArrivaldatesSuccess(data, textStatus, jqXHR)
            {

                $('#selectablearrivaldates').html(data);

            }

    });
    $( "#selectablearrivaldates" ).selectable({
        stop: function() {
           var result = $( "#select-resultarrivaldates" ).empty();
            $( ".ui-selected", this ).each(function() {
            result.append( $(this).text() );
            });
        }
    });
    setTimeout(
      function()
      {
//            $('#docnumber').val(sessionStorage.docnumber);
//            $('#dockindname').val(sessionStorage.dockindname);
                var dfrom = new Date();

                var fromyear = dfrom.getFullYear()-1; //-1 cause one year diff between fromdate and todate
                var frommonth = dfrom.getMonth()+1; // +1 cause 0-11 the javascript months
                var fromday = dfrom.getDate();

                var fromoutput = fromyear + '-' +
                    (frommonth<10 ? '0' : '') + frommonth + '-' +
                    (fromday<10 ? '0' : '') + fromday;


                var dto = new Date();

                var toyear = dto.getFullYear();
                var tomonth = dto.getMonth()+1; // +1 cause 0-11 the javascript months
                var today = dto.getDate();

                var tooutput = toyear + '-' +
                    (tomonth<10 ? '0' : '') + tomonth + '-' +
                    (today<10 ? '0' : '') + today;

            if (typeof sessionStorage.fromdate === 'undefined') {

//                sessionStorage.fromdate = fromoutput;
                $('#fromdate').val(fromoutput);
                //console.log(sessionStorage.fromdate);

            } else {
            $('#fromdate').val(sessionStorage.fromdate);

            }

            if (typeof sessionStorage.todate === 'undefined') {

                sessionStorage.todate = tooutput;
                $('#todate').val(tooutput);


                //console.log(sessionStorage.todate);

            } else {
            $('#todate').val(sessionStorage.todate);

            }

              $('#fillingdate').datepicker({ dateFormat: 'yy-mm-dd' });
              $('#fillingdate').val(tooutput); //today date to fillingdate default

//            $('#company').val(sessionStorage.company);

            $('#pohandlersearchbutton').trigger('click');

      }, 500);

   $('body').on("change", ".updateable", function() {

        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        var fieldvalue = $(this).val();
        var rowid = $(this).attr( "rowid" );
        var fieldname = $(this).attr( "name" );

           $.ajax({
            type: 'POST',
            url: 'pohandlerfieldsupdate',

            data: {
           'fieldvalue': fieldvalue,
           'rowid' : rowid,
           'fieldname': fieldname,
           'csrfmiddlewaretoken': CSRFtoken,
           },
           success: updatesuccess,
           error: updateerror,
           datatype: 'html'
          });

        function updatesuccess (data, textStatus, jqXHR){
            console.log('datafromsql:' + data);
            $('input[name="' + fieldname + '"][rowid="' + rowid + '"').val(data);
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

        $('#aux1').trigger('click');

   });
    $('#pohandlersearchbutton').click(function() {

            $.ajax({
                type: 'POST',
                url: 'pohandlersearchresults',

                data: {
//                'docnumber': $('#docnumber').val(),
//                'dockindname': $('#dockindname').val(),
                'fromdate': $('#fromdate').val(),
                'todate': $('#todate').val(),
//                'company': $('#company').val(),

                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                },

                success: function(data){

                    $('#pohandlertemplate').html(data);
                    //console.log(data);
                },
                error: function(){
                    alert('failure');
                },
                datatype: 'html'

            });
                setTimeout(
                  function()
                  {
//                    var companyvalueaccumulator=$('select#company').val(); // swap options of select element after html template refresh
//                    var companyswap=$('select#companyswap').html();
//                    $('select#company').html(companyswap);
//                    $('select#company').val(companyvalueaccumulator);

//                    var dockindnamevalueaccumulator=$('select#dockindname').val();
//                    var dockindnameswap=$('select#dockindnameswap').html();
//                    $('select#dockindname').html(dockindnameswap);
//                    $('select#dockindname').val(dockindnamevalueaccumulator);

                  }, 500);
//        sessionStorage.docnumber = $('#docnumber').val();
//        sessionStorage.dockindname = $('#dockindname').val();
//        sessionStorage.fromdate = $('#fromdate').val();
//        sessionStorage.todate = $('#todate').val();
//        sessionStorage.company = $('#company').val();

    });
    $('body').on("click", ".pohandlerarrivalbutton", function() {

        var fillingdateval = $('#fillingdate').val();
        var pohandlerarrivalbuttonrowid = $(this).attr( "rowid" );

        $('input[name2="dateofarrivalinput"][rowid="' + pohandlerarrivalbuttonrowid + '"]').val(fillingdateval);
        $('input[class="updateable"][rowid="' + pohandlerarrivalbuttonrowid + '"]').trigger('change');





    });
    $('#pohandlerreceptionbutton').click(function() {

            $.ajax({
                type: 'POST',
                url: 'pohandlerreception',

                data: {
                'dateofarrival' : $('#select-resultarrivaldates').val(),
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                },

                success: function(url){
                window.location.href = url;

                },
                error: function(){
                    alert('failure');
                },
                datatype: 'html'

            });


    });
});