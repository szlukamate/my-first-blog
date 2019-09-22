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
$(document).ready(function () {
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

              $('#fillingdate').datepicker({ dateFormat: 'yy-mm-dd' });

                var d = new Date();
                var toyear = d.getFullYear();
                var tomonth = d.getMonth()+1; // +1 cause 0-11 the javascript months
                var today = d.getDate();
                var tooutput = toyear + '-' +
                    (tomonth<10 ? '0' : '') + tomonth + '-' +
                    (today<10 ? '0' : '') + today;
              $('#fillingdate').val(tooutput); //today date to fillingdate default
              $('#receiveds').prop('checked', false);
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
                'receivedstatus': $('#receiveds').prop('checked'),

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

    });
    $('body').on("click", ".pohandlerarrivalbutton", function() {

        var fillingdateval = $('#fillingdate').val();
        var pohandlerarrivalbuttonrowid = $(this).attr( "rowid" );

        $('input[name2="dateofarrivalinput"][rowid="' + pohandlerarrivalbuttonrowid + '"]').val(fillingdateval);
        $('input[class="updateable"][rowid="' + pohandlerarrivalbuttonrowid + '"]').trigger('change');
                    console.log('na3');





    });

    $( "#dialog-form" ).dialog({
          autoOpen: false,
          height: 210,
          width: 350,
          modal: true,
          buttons: {
            "Split": function() {
                $.ajax({
                    type: 'POST',
                    url: 'pohandlersplit',

                    data: {
                    'rowid' : $('#rowid').html(),
                    'newqty' : $('#qtydialog').val(),
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
            },
            Cancel: function() {
                    $( this ).dialog( "close" );
            }
          },
          close: function() {
                    $( this ).dialog( "close" );
          }
    });

    $('body').on("click", ".pohandlersplitbutton", function() {
            var rowid = $(this).attr( "rowid" );
            var oldqty=$('td[name="qty"][rowid="' + rowid + '"]').text();
            $('#qtydialog').val(oldqty);
            $('#rowid').html(rowid);
            $( "#dialog-form" ).dialog( "open" );





    });
    $('#pohandlerreceptionbutton').click(function() {

        var porowsnumber=0;
        var i;
        var dateofarrivallist=[];
        var podocdetailsid;
        var podocid;
        var cordocid;

        var dateofarrival = $('#select-resultarrivaldates').text()
        porowsnumberfunc();

        main();

            function main(){
                porowsnumberfunc();

                for (i = 1; i <= porowsnumber; i++) {
                    getifchecked();  // more precisely: getifchecked => getarrived

                }


            }

            function porowsnumberfunc(){
            porowsnumber=$('#porowsnumber').attr( "porowsnumber" ); //Number of PO rows arrived
            }
            function getifchecked(){

                    if ($('input[type="text"][loopid="' + i + '"][name2="dateofarrivalinput"]').val() == dateofarrival) {
                           podocdetailsid=$('input[type="text"][loopid="' + i + '"').attr( "podocdetailsid" );
                           podocid=$('input[type="text"][loopid="' + i + '"').attr( "podocid" );
                           cordocid=$('input[type="text"][loopid="' + i + '"').attr( "cordocid" );

                           dateofarrivallist.push(podocdetailsid, podocid, cordocid, dateofarrival);
                           console.log('raw' + dateofarrivallist);
                    }

            }

            $.ajax({
                type: 'POST',
                url: 'pohandlerreception',

                data: {
                'dateofarrival' : $('#select-resultarrivaldates').text(),
                'dateofarrivallist': JSON.stringify(dateofarrivallist),

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

            console.log('stringified' + JSON.stringify(dateofarrivallist));

    });
});