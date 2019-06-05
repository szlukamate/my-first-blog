/*
quotation.js
*/

            var msg="Hello Javascript2";
                    console.log(msg);
$(function () {

    $('a[href="/quotation/products/0/"]').parent().addClass('active'); //activate products tab on navbar

    $('#title').click(function() {
        $('#title').hide();

    });
   $('.updateable').focusout(function() {

        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        var fieldvalue = $(this).val();
        var productid = $(this).attr( "productid" );
        var fieldname = $(this).attr( "name" );



                   $.ajax({
                        type: 'POST',
                        url: '',

                        data: {
                        'fieldvalue': fieldvalue,
                        'rowid' : productid,
                        'fieldname': fieldname,
                        'csrfmiddlewaretoken': CSRFtoken
                        },
                        success: updatesuccess,
                        error: updateerror,




                        datatype: 'html'


                   });
                            function updatesuccess (data, textStatus, jqXHR){
                                console.log('datafromsql:' + data);
                                $('input[name="' + fieldname + '"][productid="' + productid + '"').css("background-color", "white").val(data);
                                $('#sqlsavingfeedbackproduct').html('<span  class="glyphicon glyphicon-hdd"></span>');

                                setTimeout(
                                  function()
                                  {
                                    $('#sqlsavingfeedbackproduct').html("");

                                  }, 500);
                                console.log(fieldvalue);
                            };
                            function updateerror (){
                                alert('Failure in saving');
                            };


                 if ((fieldname=='purchase_price_tblproduct') || (fieldname=='margin_tblproduct')){ // if price related field changed then an additional listpriceupdate

                    setTimeout(function(){
                    $.ajax({
                    type: 'POST',
                    url: 'productlistpricefieldupdate/',

                    data: {
                        'postselector' : 'listpriceupdaterequestonly',
                        'productidinproductjs' : productid,
                        'csrfmiddlewaretoken': CSRFtoken
                        },

                    success:requerysuccess,
                    error: requeryerror,
                    complete: completerequery,
                    })
                    }, 500); // delay to ensure to get valid data

                    function requerysuccess (data, textStatus, jqXHR){
                    console.log('Success requery!!!');
                    var listpricefromsql=data[0][2];
                    $('input[name="listprice"][productid="' + productid + '"').val(listpricefromsql);

                    };
                    function requeryerror (){
                        alert('Failure in requery');
                    };
                    function completerequery (){
                        console.log('ajax done');
                    };
                 };





   });

   $('.updateable').click(function() {
        $(this).css("background-color", "yellow");


   });
    $('.listpricechangerbutton').click(function() {
        var productid=$(this).attr( "productid" );

                    listpricefieldstate(this);
                    var listprice=$('input[name="listprice"][productid="' + productid + '"').val();
                    var purchaseprice=$('input[name="purchase_price_tblproduct"][productid="' + productid + '"').val();
                    var marginrequired=((listprice-purchaseprice)/listprice)*100


                        $.ajax({
                        type: 'POST',
                        url: 'productlistpricefieldupdate/',

                        data: {
                        'postselector' : 'listpriceupdaterequestwithpassingmarginrequired',
                        'marginrequired' : marginrequired,
                        'productidinproductjs' : productid,
                        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                        },

                        success: ajaxsuccess,
                        error: ajaxerror,
                        complete: ajaxcomplete,

                        datatype: 'json'

                        });



    function listpricefieldstate(that){

        if ($('input[name="listprice"][productid="' + productid + '"').is(':disabled')){ // listprice is disabled
                setlistpricebuttontext('toenabled', that);

             } else { // listprice is enabled
                setlistpricebuttontext('todisabled', that);


        }
    }
    function setlistpricebuttontext(listpricebuttonstate, that2){

            switch(listpricebuttonstate) {
              case 'toenabled':
                $('input[name="listprice"][productid="' + productid + '"').prop('disabled', false)
                $(that2).attr('value', 'Confirm');
                break;
              case 'todisabled':
                $('input[name="listprice"][productid="' + productid + '"').prop('disabled', true)
                $(that2).attr('value', 'Change list price');
                break;
              default:
                // code block
            }
    }
    function ajaxsuccess (data, textStatus, jqXHR){
    var marginnewfromsql=data[0][1];
    $('input[name="margin_tblproduct"][productid="' + productid + '"').val(marginnewfromsql);

    }

    function ajaxerror (){
       console.log('ajax failure');
    }
    function ajaxcomplete (){

        console.log('ajax done');
    }


    });

    $('.currencyselection').change(function() {
        var productid=$(this).attr( "productid" );
                    $.ajax({
                    type: 'POST',
                    url: 'productupdatecurrencyisocode/',

                    data: {

                    'currencyidinjs' : $(this).val(),
                    'productidinjs' : $(this).attr( "productid" ),
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                    },

                    success: UpdateSuccess,
                    error: function(){
                       console.log('ajax failure');
                    },
                    complete: function(){

                        console.log('ajax done');
                    },

                    datatype: 'json'

                    });

                    function UpdateSuccess(data, textStatus, jqXHR)
                    {
                    console.log(data);
                    var currencyidsql= data[0]
                    $('select[class="currencyselection"][productid="' + productid + '"] option:selected').html(currencyidsql);


                    }

    });
    $('.supplierselection').change(function() {
        var productid=$(this).attr( "productid" );
                    $.ajax({
                    type: 'POST',
                    url: 'productupdatesupplier/',

                    data: {

                    'supplieridinjs' : $(this).val(),
                    'productidinjs' : $(this).attr( "productid" ),
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                    },

                    success: UpdateSuccess,
                    error: function(){
                       console.log('ajax failure');
                    },
                    complete: function(){

                        console.log('ajax done');
                    },

                    datatype: 'json'

                    });

                    function UpdateSuccess(data, textStatus, jqXHR)
                    {
                    console.log(data);
                    var supplieridsql= data[0]
                    $('select[class="supplierselection"][productid="' + productid + '"] option:selected').html(supplieridsql);


                    }

    });
    $( "#dialog-form" ).dialog({
          autoOpen: false,
          height: 260,
          width: 350,
          modal: true,
          buttons: {
            "Service": function() {
                $.ajax({
                    type: 'POST',
                    url: 'productnew/',

                    data: {
                    'serviceflag' : 1,
                    'discreteflag' : 0,
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                    },

                    success: function(url){
                    //window.location.href = url;

                    },
                    error: function(){

                        alert('failure');
                    },
                    datatype: 'html'

                });
            },
            "Product/InDiscrete": function() {
                    $( this ).dialog( "close" );
            },
            "Product/Discrete": function() {
                    $( this ).dialog( "close" );
            },
            Cancel: function() {
                    $( this ).dialog( "close" );
            }
          },
          close: function() {
                    $( this ).dialog( "close" );
          }
    });
   $('#newproductsign').click(function() {
            $( "#dialog-form" ).dialog( "open" );


   });

});