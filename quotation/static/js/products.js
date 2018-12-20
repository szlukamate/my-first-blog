/*
quotation.js
*/

            var msg="Hello Javascript2";
                    console.log(msg);
$(function () {

    $('#title').click(function() {
        $('#title').hide();

    });
   $('.updateable').focusout(function() {

        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        var fieldvalue = $(this).val();
        var productid = $(this).attr( "productid" );
        var fieldname = $(this).attr( "name" );


             if (fieldname!=='salesprice') {

                   $.ajax({
                        type: 'POST',
                        url: '',

                        data: {
                        'fieldvalue': fieldvalue,
                        'rowid' : productid,
                        'fieldname': fieldname,
                        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                        },
                        success:function(data, textStatus, jqXHR){
                            console.log('datafromsql:' + data);
                            $('input[name="' + fieldname + '"][productid="' + productid + '"').css("background-color", "white").val(data);
                            $('#sqlsavingfeedbackproduct').html('<span  class="glyphicon glyphicon-hdd"></span>');

                            setTimeout(
                              function()
                              {
                                $('#sqlsavingfeedbackproduct').html("");

                              }, 500);
                            console.log(fieldvalue);
                                    },
                        error: function(){
                            alert('Failure in saving');
                        },


                        datatype: 'html'


                    });
             };
             setTimeout( function(){

             if ((fieldname=='purchase_price_tblproduct') || (fieldname=='margin_tblproduct')){

                $.ajax({
                type: 'POST',
                url: 'productsalespricefieldupdate/',

                data: {
                    'postselector' : 'salespriceupdaterequestonly',
                    'productidinproductjs' : productid,
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                    },

                success:function(data, textStatus, jqXHR){
                console.log('Success requery!!!');
                console.log(data);
                var salespricefromsql=data[0][2];
                $('input[name="salesprice"][productid="' + productid + '"').val(salespricefromsql);

                },
                error: function(){
                console.log('Failure requery');
                },
                complete: function(){
                console.log('ajax done');
                }
                });
             };

             },500);

            if (fieldname=='salesprice'){


                console.log('not disabled');
                $('input[name="salesprice"][productid="' + productid + '"').prop('disabled', true)
                $(this).attr('value', 'Change sales price');
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

                    success: function (data, textStatus, jqXHR){
                    console.log(data);
                    var marginnewfromsql=data[0][1];
                    $('input[name="margin_tblproduct"][productid="' + productid + '"').val(marginnewfromsql);

                    },
                    error: function(){
                       console.log('ajax failure');
                    },
                    complete: function(){

                        console.log('ajax done');
                    },

                    datatype: 'json'

                    });
                $('input[name="salespricechangerbutton"][productid="' + productid + '"').attr('value', 'Change');
                $('input[name="' + fieldname + '"][productid="' + productid + '"').css("background-color", "white")
            };



   });

   $('.updateable').click(function() {
        $(this).css("background-color", "yellow");


   });
    $('.salespricechangerbutton').click(function() {
        var productid=$(this).attr( "productid" );

            if ($('input[name="salesprice"][productid="' + productid + '"').is(':disabled')){
            // Salesprice is disabled
                console.log('yes disabled');
                $('input[name="salesprice"][productid="' + productid + '"').prop('disabled', false)
                $(this).attr('value', 'Confirm');
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