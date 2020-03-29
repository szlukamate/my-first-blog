/*
acustomerorder.js
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
    var stockradios = $('input:radio[name=stockradio]');
    if(stockradios.is(':checked') === false) {
        stockradios.filter('[value="9"]').prop('checked', true);
    }
    $( "#stockradiobutton" ).dialog({
      autoOpen: false,
      height: 330,
      width: 350,
      modal: true,
      buttons: {
        Ok: function() {
          $( this ).dialog( "close" );
        var customerorderid=$('#customerorderdocid').text();
        var selectedstockid=$('input[type="radio"]:checked').val();
        console.log(selectedstockid);


            $.ajax({
                type: 'POST',
                url: 'deliverynotepre',

                data: {
                'customerorderid' : customerorderid,
                'selectedstockid' : selectedstockid,

                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                },

                success: function(data){

                    $('#deliverynotepretemplate').html(data);
                    console.log(data);

                },
                error: function(){
                    alert('failure');
                },
                datatype: 'html'

            });

        }
      }
    });

    $( "input[type='radio']" ).checkboxradio();

    var index1 = 'qpsstats-active-tab1';
    //  Define friendly data store name
    var dataStore1 = window.sessionStorage;
    var oldIndex1 = 0;
    //  Start magic!
    try {
        // getter: Fetch previous value
        oldIndex1 = dataStore1.getItem(index1);
    } catch(e) {}

    $( "#tabs1" ).tabs({
        active: oldIndex1,
        activate: function(event, ui) {
            //  Get future value
            var newIndex1 = ui.newTab.parent().children().index(ui.newTab);
            //  Set future value
            try {
                dataStore1.setItem( index1, newIndex1 );
            } catch(e) {}
        }
    });


    var index2 = 'qpsstats-active-tab2';
    //  Define friendly data store name
    var dataStore2 = window.sessionStorage;
    var oldIndex2 = 0;
    //  Start magic!
    try {
        // getter: Fetch previous value
        oldIndex2 = dataStore2.getItem(index2);
    } catch(e) {}

    $( "#tabs2" ).tabs({
        active: oldIndex2,
        activate: function(event, ui) {
            //  Get future value
            var newIndex2 = ui.newTab.parent().children().index(ui.newTab);
            //  Set future value
            try {
                dataStore2.setItem( index2, newIndex2 );
            } catch(e) {}
        }
    });
$('#title').click(function() {
    $('#title').hide();

});
   $('.updateabletbldocdetails').change(function() {

        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        var fieldvalue = $(this).val();
        var rowid = $(this).attr( "rowid" );
        var fieldname = $(this).attr( "name" );
        var tbl="tblDoc_details";

           $.ajax({
            type: 'POST',
            url: '',

            data: {
           'tbl' : tbl,
           'fieldvalue': fieldvalue,
           'rowid' : rowid,
           'docid' : 0,
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

   });
   $('.updateabletbldoc').change(function() {

        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        var fieldvalue = $(this).val();
        var docid = $('#customerorderdocid').text();
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
    /*
    $('.updateabletbldocdetails').click(function() {
        $(this).css("background-color", "yellow");
    });
    $('.updateabletbldocdetails').focusout(function() {
        $(this).css("background-color", "white");
    });
    */



   $('#search').keyup(function() {
            var docidincustomerorderjs = $('#customerorderdocid').text();
            $.ajax({
                type: 'POST',
                url: 'searchcustomerordercontacts/',

                data: {
                'search_text' : $('#search').val(),
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'docidincustomerorderjs' : docidincustomerorderjs
                },

                success: SearchSuccess,
                error: function(){
                    alert('failure');
                },
                datatype: 'html'

            });

            console.log(docidincustomerorderjs)
            function SearchSuccess(data, textStatus, jqXHR)
            {

            $('#search-results').html(data);

            }
   });
    $('#newcustomerorderrowsignonhtml').click(function() {
        var customerorderid=$('#customerorderdocid').text();

            $.ajax({
                type: 'POST',
                url: 'customerordernewrowadd',

                data: {
                'customerorderid' : customerorderid,
                'docdetailsid' : 0, // New row in docdetails the 0 shows it (the customerordernewrowadd def in vw_customerorder.py recognizes it)
                'nextfirstnumonhtml' : $('#nextfirstnumonhtml').val(),
                'nextsecondnumonhtml' : $('#nextsecondnumonhtml').val(),
                'nextthirdnumonhtml' : $('#nextthirdnumonhtml').val(),
                'nextfourthnumonhtml' : $('#nextfourthnumonhtml').val(),

                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                },

                success: function(data){

                    $('#customerordertemplate').html(data);
                    console.log(data);
                },
                error: function(){
                    alert('failure');
                },
                datatype: 'html'

            });



    });

    $('[name="customerorderproductforrow"]').click(function() {
        var customerorderid=$('#customerorderdocid').text();
        var docdetailsid=$(this).attr( "rowid" );
        var productid=$('input[name="Productid_tblDoc_details_id"][rowid="' + docdetailsid + '"').val()
        console.log('in');
            $.ajax({
                type: 'POST',
                url: 'customerordernewrowadd',

                data: {
                'customerorderid' : customerorderid,
                'docdetailsid' : docdetailsid, // Only product update the !0 shows it (the customerordernewrowadd def in vw_customerorder.py recognizes it)
                'nextfirstnumonhtml' :    $('input[name="firstnum_tblDoc_details"][rowid="' + docdetailsid + '"').val(),
                'nextsecondnumonhtml' : $('input[name="secondnum_tblDoc_details"][rowid="' + docdetailsid + '"').val(),
                'nextthirdnumonhtml' : $('input[name="thirdnum_tblDoc_details"][rowid="' + docdetailsid + '"').val(),
                'nextfourthnumonhtml' : $('input[name="fourthnum_tblDoc_details"][rowid="' + docdetailsid + '"').val(),

                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                },

                success: function(data){

                    $('#customerordertemplate').html(data);
                    console.log(data);
                    location.href = "#" + productid;
                },
                error: function(){
                    alert('failure');
                },
                datatype: 'html'

            });



    });
    $('.selection').change(function() {

        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        var fieldvalue = $(this).val();
        var customerorderdocid = $('#customerorderdocid').text();
        var fieldname = $(this).attr( "fieldname" );
        console.log('customerorderdocid:' + customerorderdocid);
            $.ajax({
            type: 'POST',
            url: 'customerorderuniversalselections/',

            data: {
           'fieldvalue': fieldvalue,
           'customerorderdocid' : customerorderdocid,
           'fieldname': fieldname,
           'csrfmiddlewaretoken': CSRFtoken,
           },
           success: updatesuccess,
           error: updateerror,
           datatype: 'html'
          });

        function updatesuccess (data, textStatus, jqXHR){
            console.log('datafromsql:' + data);
            var fromsql= data[0]

            $('select[class="selection"][fieldname="' + fieldname + '"] option:selected').html(fromsql);


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
    $('#choosestockbutton').click(function() {
            $( "#stockradiobutton" ).dialog( "open" );

    });

});