/*
customerinvoice.js
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
        var xmlexists = $('#xmlexists').text();
        var pdfexists = $('#pdfexists').text();

//                    console.log(xmlexists, pdfexists);

// Dialog "Dispatching..." begin
    $( "#dialog-message" ).dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        Ok: function() {
          $( this ).dialog( "close" );
        }
      }
    });

            if ( xmlexists == 1 && pdfexists == 0 ) { // Dispatching...
                $( "#dialog-message" ).dialog("option", "buttons", {}); //remove OK button
                $( "#dialog-message" ).dialog( "open" );
            }
// Dialog "Dispatching..." end




// customerinvoice xml begin
           var dispatchthexml = 0;

            //dispatchthexml variable check from def begin
           $.ajax({
            type: 'POST',
            url: '',

            data: {
           'selector' : 'dispatchthexmlcheck',
           'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
           },
           success: updatesuccess,
           error: updateerror,
           ContentType: 'json'
          });

        function updatesuccess (json, textStatus, jqXHR){
            dispatchthexml = json[0]; //if there is xml and pdf dont send xml again (dispatchthexml = 0)
                                    console.log(dispatchthexml);

              if (dispatchthexml == '1') {

                  // pre-fill FormData from the form
 //                                   console.log(formData);
                  var xmlfilecontent =json[1];
//                                    console.log('xmlfilecontent: ' + xmlfilecontent);

                  var form = $('#szamlazzform')[0];
                  var blob = new Blob([xmlfilecontent], { type: "file"});
                  let formData = new FormData(form);
                  formData.append("action-xmlagentxmlfile", blob, "xml");

///*
                  // send it out
                  let xhr = new XMLHttpRequest();
                  xhr.open("POST","https://cors-anywhere.herokuapp.com/https://www.szamlazz.hu/szamla/"); // https://cors-anywhere.herokuapp.com the header exchanger proxy server
                  xhr.send(formData);

                  xhr.onload = function (){ // if the response received the pdf is read and sent to stack
                  $xml = $( $.parseXML( xhr.response ) );
                  pdfstringbase64 = $xml.find('pdf').text()
                                    console.log(pdfstringbase64);
                  //pdfstring = pdfstringbase64

                    $.ajax({ // stack the pdf in def call
                        type: 'POST',
                        url: 'customerinvoicexmlresponsepdfstacking',

                        data: {
                        'customerinvoicedocid' : $('#customerinvoicedocid').text(),
                        'pdfstringbase64' : pdfstringbase64,
                        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                        },

                        success: function(url){
                        window.location.href = url; // show invoice pdf

                        },
                        error: function(){

                            alert('failure');
                        },
                        datatype: 'html'

                    });

                  };
//*/
              };


        };
        function updateerror (){
            console.log('Failure in saving');
        };
            //dispatchthexml variable check from def end

// customerinvoice xml end

//$("#tabs").tabs({ active: 0 });
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
           'selector' : 'update',
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
        var docid = $('#customerinvoicedocid').text();
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
           'selector' : 'update',
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
    $('#newdeliverynoterowsignonhtml').click(function() {
        var deliverynoteid=$('#deliverynotedocid').text();

            $.ajax({
                type: 'POST',
                url: 'deliverynotenewrowadd',

                data: {
                'deliverynoteid' : deliverynoteid,
                'docdetailsid' : 0, // New row in docdetails the 0 shows it (the deliverynotenewrowadd def in vw_deliverynote.py recognizes it)
                'nextfirstnumonhtml' : $('#nextfirstnumonhtml').val(),
                'nextsecondnumonhtml' : $('#nextsecondnumonhtml').val(),
                'nextthirdnumonhtml' : $('#nextthirdnumonhtml').val(),
                'nextfourthnumonhtml' : $('#nextfourthnumonhtml').val(),

                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                },

                success: function(data){

                    $('#deliverynotetemplate').html(data);
                    console.log(data);
                },
                error: function(){
                    alert('failure');
                },
                datatype: 'html'

            });



    });

    $('[name="deliverynoteproductforrow"]').click(function() {
        var deliverynoteid=$('#deliverynotedocid').text();
        var docdetailsid=$(this).attr( "rowid" );
        var productid=$('input[name="Productid_tblDoc_details_id"][rowid="' + docdetailsid + '"]').val();
        console.log('in');
            $.ajax({
                type: 'POST',
                url: 'deliverynotenewrowadd',

                data: {
                'deliverynoteid' : deliverynoteid,
                'docdetailsid' : docdetailsid, // Only product update the !0 shows it (the deliverynotenewrowadd def in vw_deliverynote.py recognizes it)
                'nextfirstnumonhtml' :    $('input[name="firstnum_tblDoc_details"][rowid="' + docdetailsid + '"').val(),
                'nextsecondnumonhtml' : $('input[name="secondnum_tblDoc_details"][rowid="' + docdetailsid + '"').val(),
                'nextthirdnumonhtml' : $('input[name="thirdnum_tblDoc_details"][rowid="' + docdetailsid + '"').val(),
                'nextfourthnumonhtml' : $('input[name="fourthnum_tblDoc_details"][rowid="' + docdetailsid + '"').val(),

                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                },

                success: function(data){

                    $('#deliverynotetemplate').html(data);
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
        var quotationdocid = $('#customerinvoicedocid').text();
        var fieldname = $(this).attr( "fieldname" );
//        console.log('quotationdocid:' + quotationdocid);
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

    $( "#dialog-form" ).dialog({
          autoOpen: false,
          height: 210,
          width: 350,
          modal: true,
          buttons: {
            "Add New Label": function() {
                $.ajax({
                    type: 'POST',
                    url: 'deliverynotenewlabel',

                    data: {
                    'newlabelid' : $('#newlabelid').val(),
//                    'deliverynotedocid' : $('#deliverynotedocid').text(),
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                    },

                    success: function(data){
//                    window.location.href = url;
                    window.parametertostocktaking = data;
                    console.log('data:' + data);

                    },
                    error: function(){

                        alert('failure');
                    },
                    datatype: 'html'

                });
                        setTimeout(
                          function()
                          {

                          console.log('parametertostocktaking:' + window.parametertostocktaking);

                            $('#parametertostocktaking').val(window.parametertostocktaking.trim());

                            switch(window.parametertostocktaking.trim()) {
                              case 'noneproduct':
                                $( "#dialog-form" ).dialog( "close" );
                                $( "#dialog-form-noneproduct" ).dialog( "open" );
                                break;
                              case 'indiscreteproduct':
                                $( "#dialog-form" ).dialog( "close" );
                                $( "#dialog-form-indiscreteproduct" ).dialog( "open" );
                                break;
                              case 'discreteproduct':
                                $( "#dialog-form" ).dialog( "close" );
                                $( "#dialog-form-discreteproduct" ).dialog( "open" );
                                break;
                              case 'serviceproduct':
                                $( "#dialog-form" ).dialog( "close" );
                                $( "#dialog-form-serviceproduct" ).dialog( "open" );
                                break;
                              default:
                                // code block
                            }

                          }, 500);




            },
            Cancel: function() {
                    $( this ).dialog( "close" );
            }
          },
          close: function() {
                    $( this ).dialog( "close" );
          }



    });

    $('#newlabelbutton').click(function() {
            $( "#dialog-form" ).dialog( "open" );

    });
    $( "#dialog-form-indiscreteproduct" ).dialog({
      autoOpen: false,
      height: 210,
      width: 350,
      modal: true,
      buttons: {
        "Send Qty": function() {
            $.ajax({
                type: 'POST',
                url: 'deliverynoteafternewlabel',

                data: {
                'newlabelid' : $('#newlabelid').val(),
                'deliverynotedocid' : $('#deliverynotedocid').text(),
                'indiscreteqty' : $('#indiscreteqty').val(),
                'parametertostocktaking' : $('#parametertostocktaking').val(),
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
    $( "#dialog-form-noneproduct" ).dialog({
          autoOpen: false,
          height: 210,
          width: 350,
          modal: true,
          buttons: {
          Close: function() {
                    $( this ).dialog( "close" );
          }
          }


    });
    $( "#dialog-form-discreteproduct" ).dialog({
      autoOpen: false,
      height: 210,
      width: 350,
      modal: true,
      open: function() {
            $.ajax({
                type: 'POST',
                url: 'deliverynoteafternewlabel',

                data: {
                'newlabelid' : $('#newlabelid').val(),
                'deliverynotedocid' : $('#deliverynotedocid').text(),
                'indiscreteqty' : $('#indiscreteqty').val(),
                'parametertostocktaking' : $('#parametertostocktaking').val(),
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

            setTimeout(function() {

                $( "#dialog-form-discreteproduct" ).dialog( "close" );
            }, 1000);
        },
      close: function() {
                $( this ).dialog( "close" );
      }



    });
    $( "#dialog-form-serviceproduct" ).dialog({
          autoOpen: false,
          height: 210,
          width: 350,
          modal: true,
          buttons: {
          Close: function() {
                    $( this ).dialog( "close" );
          }
          }


    });


    $('#showpdfbutton').click(function() {
                $.ajax({
                    type: 'POST',
                    url: 'customerinvoiceshowpdfbutton',

                    data: {
                    'customerinvoicedocid' : $('#customerinvoicedocid').text(),

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