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
//$("#tabs").tabs({ active: 0 });

// Dialog "Connecting..." begin
    $( "#dialog-message-connecting" ).dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        Ok: function() {
          $( this ).dialog( "close" );
        }
      }
    });

// Dialog "Connecting..." end


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
        var docid = $('#quotationdocid').text();
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
            var docidinquotationjs = $('#quotationdocid').text();
            $.ajax({
                type: 'POST',
                url: 'searchquotationcontacts/',

                data: {
                'search_text' : $('#search').val(),
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'docidinquotationjs' : docidinquotationjs
                },

                success: SearchSuccess,
                error: function(){
                    alert('failure');
                },
                datatype: 'html'

            });

            console.log(docidinquotationjs)
            function SearchSuccess(data, textStatus, jqXHR)
            {

            $('#search-results').html(data);

            }
   });
    $('#newquotationrowsignonhtml').click(function() {
        var quotationid=$('#quotationdocid').text();

            $.ajax({
                type: 'POST',
                url: 'quotationnewrowadd',

                data: {
                'quotationid' : quotationid,
                'docdetailsid' : 0, // New row in docdetails the 0 shows it (the quotationnewrowadd def in vw_quotation.py recognizes it)
                'nextfirstnumonhtml' : $('#nextfirstnumonhtml').val(),
                'nextsecondnumonhtml' : $('#nextsecondnumonhtml').val(),
                'nextthirdnumonhtml' : $('#nextthirdnumonhtml').val(),
                'nextfourthnumonhtml' : $('#nextfourthnumonhtml').val(),

                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                },

                success: function(data){

                    $('#quotationtemplate').html(data);
                    console.log(data);
                },
                error: function(){
                    alert('failure');
                },
                datatype: 'html'

            });



    });

    $('[name="quotationproductforrow"]').click(function() {
        var quotationid=$('#quotationdocid').text();
        var docdetailsid=$(this).attr( "rowid" );
        var productid=$('input[name="Productid_tblDoc_details_id"][rowid="' + docdetailsid + '"]').val();
        console.log('in');
            $.ajax({
                type: 'POST',
                url: 'quotationnewrowadd',

                data: {
                'quotationid' : quotationid,
                'docdetailsid' : docdetailsid, // Only product update the !0 shows it (the quotationnewrowadd def in vw_quotation.py recognizes it)
                'nextfirstnumonhtml' :    $('input[name="firstnum_tblDoc_details"][rowid="' + docdetailsid + '"').val(),
                'nextsecondnumonhtml' : $('input[name="secondnum_tblDoc_details"][rowid="' + docdetailsid + '"').val(),
                'nextthirdnumonhtml' : $('input[name="thirdnum_tblDoc_details"][rowid="' + docdetailsid + '"').val(),
                'nextfourthnumonhtml' : $('input[name="fourthnum_tblDoc_details"][rowid="' + docdetailsid + '"').val(),

                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                },

                success: function(data){

                    $('#quotationtemplate').html(data);
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
        var quotationdocid = $('#quotationdocid').text();
        var fieldname = $(this).attr( "fieldname" );
        console.log('quotationdocid:' + quotationdocid);
            $.ajax({
            type: 'POST',
            url: 'quotationuniversalselections/',

            data: {
           'fieldvalue': fieldvalue,
           'quotationdocid' : quotationdocid,
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

    $('#itsbutton').click(function() {
        var quotationid=$('#quotationdocid').text();

                  // send it out
                  let xhr = new XMLHttpRequest();
                  xhr.open("GET","https://cors-anywhere.herokuapp.com/http://13.58.18.245:3000//time_entries.xml?key=6a722899382b3495828b3f2d6c41f93d19adb5f6&project_id=4"); // https://cors-anywhere.herokuapp.com the header exchanger proxy server
                  xhr.send();
                  $( "#dialog-message-connecting" ).dialog("option", "buttons", {}); //remove OK button
                  $( "#dialog-message-connecting" ).dialog( "open" );

                  xhr.onload = function (){
                                    console.log(xhr.response);
                  $( "#dialog-message-connecting" ).dialog( "close" );

                    $.ajax({
                        type: 'POST',
                        url: 'quotationissuetrackingsystem',

                        data: {
                        'quotationid' : quotationid,
                        'xmlresponsestring' : xhr.response,
                        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                        },

                        success: function(data){
                    $('#quotationtemplate').html(data);
//                    console.log(data);

                        },
                        error: function(){

                            alert('failure');
                        },
                        datatype: 'html'

                    });

                  };


    });

    $('body').on("click", ".timeentriestoquotationbutton", function() {
                var issuetrackingsystemnumberofitems= $('#issuetrackingsystemnumberofitems').text();
                var itemdatalist=[];
                var itemdataliststringified;
                var quotationdocid = $('#quotationdocid').text();

        main();

            function main(){


                for (i = 1; i <= issuetrackingsystemnumberofitems; i++) {
                    itemdatacollect(i);

                }
                itemdataliststringified = JSON.stringify(itemdatalist);

                datatransmit();

            }
            function itemdatacollect(i){
              timeentryandissueid=$('td[class="timeentryandissueid"][rowid="' + (i - 1) + '"]').text();
              projectname=$('td[class="projectname"][rowid="' + (i - 1) + '"]').text();
              username=$('td[class="username"][rowid="' + (i - 1) + '"]').text();
              activityname=$('td[class="activityname"][rowid="' + (i - 1) + '"]').text();
              hours=$('td[class="hours"][rowid="' + (i - 1) + '"]').text();
              comments=$('td[class="comments"][rowid="' + (i - 1) + '"]').text();
              spenton=$('td[class="spenton"][rowid="' + (i - 1) + '"]').text();
              itemdatalist.push(timeentryandissueid, projectname, username, activityname, hours, comments, spenton);

            }

            function datatransmit(){

                $.ajax({
                    type: 'POST',
                    url: 'quotationissuetrackingsystemitemstoquotation',

                    data: {
                    'quotationdocid' : quotationdocid,
                    'issuetrackingsystemnumberofitems' : issuetrackingsystemnumberofitems,
                    'itemdatalist': itemdataliststringified,

                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                    },

                    success: function(url){
                    console.log('success');

                    window.location.href = url;

                    },
                    error: function(){
                        alert('failure');
                    },
                    datatype: 'html'

                });
            }






    });


});