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


                 if ((fieldname=='purchase_price_tblproduct') || (fieldname=='margin_tblproduct')){ // if price related field changed then an additional salespriceupdate

                    setTimeout(function(){
                    $.ajax({
                    type: 'POST',
                    url: 'productsalespricefieldupdate/',

                    data: {
                        'postselector' : 'salespriceupdaterequestonly',
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
                    var salespricefromsql=data[0][2];
                    $('input[name="salesprice"][productid="' + productid + '"').val(salespricefromsql);

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
    $('.salespricechangerbutton').click(function() {
        var productid=$(this).attr( "productid" );

                    salespricefieldstate(this);
                    var salesprice=$('input[name="salesprice"][productid="' + productid + '"').val();
                    var purchaseprice=$('input[name="purchase_price_tblproduct"][productid="' + productid + '"').val();
                    var marginrequired=((salesprice-purchaseprice)/salesprice)*100


                        $.ajax({
                        type: 'POST',
                        url: 'productsalespricefieldupdate/',

                        data: {
                        'postselector' : 'salespriceupdaterequestwithpassingmarginrequired',
                        'marginrequired' : marginrequired,
                        'productidinproductjs' : productid,
                        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                        },

                        success: ajaxsuccess,
                        error: ajaxerror,
                        complete: ajaxcomplete,

                        datatype: 'json'

                        });



    function salespricefieldstate(that){

        if ($('input[name="salesprice"][productid="' + productid + '"').is(':disabled')){ // Salesprice is disabled
                setsalespricebuttontext('toenabled', that);

             } else { // Salesprice is enabled
                setsalespricebuttontext('todisabled', that);


        }
    }
    function setsalespricebuttontext(salespricebuttonstate, that2){

            switch(salespricebuttonstate) {
              case 'toenabled':
                $('input[name="salesprice"][productid="' + productid + '"').prop('disabled', false)
                $(that2).attr('value', 'Confirm');
                break;
              case 'todisabled':
                $('input[name="salesprice"][productid="' + productid + '"').prop('disabled', true)
                $(that2).attr('value', 'Change sales price');
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

});