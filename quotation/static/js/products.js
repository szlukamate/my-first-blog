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
                console.log(fieldname, fieldvalue, productid);
           //     window.location.reload();
    });

   $('.updateable').click(function() {
        $(this).css("background-color", "yellow");

//          console.log(data);
//            console.log('click event');

   });
/*
   $('#search').keyup(function() {
            $.ajax({
                type: 'POST',
                url: 'searchquotationcontacts/',

                data: {
                'search_text' : $('#search').val(),
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                },

                success: SearchSuccess,
                error: function(){
 //                   alert('failure');
                },
                datatype: 'html'

            });

            console.log('Works')
            function SearchSuccess(data, textStatus, jqXHR)
            {

            $('#search-results').html(data);
            console.log(data);

            }
    });
*/
    $('.salespricechangerbutton').click(function() {
        var productid=$(this).attr( "productid" );

            if ($('input[name="salesprice"][productid="' + productid + '"').is(':disabled')){
            // Salesprice is disabled
                console.log('yes disabled');
                $('input[name="salesprice"][productid="' + productid + '"').prop('disabled', false)
                $(this).attr('value', 'Confirm');
            } else
            // Salesprice is not disabled
            {
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
                    'marginrequired' : marginrequired,
                    'productidinproductjs' : productid,
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

       //             console.log('Works the updatejs')

            function UpdateSuccess(data, textStatus, jqXHR)
            {
        //    console.log('ajax success!!!');
        //    $('#search-results').html(data);
            console.log(data);
            var marginnewfromsql=data[0][1];
            $('input[name="margin_tblproduct"][productid="' + productid + '"').val(marginnewfromsql);

            }
            }

      //          $('input[name="salesprice"][productid="' + productid + '"').prop('disabled', false).val('q');
      //          $(this).attr('value', 'Confirm');
       //         console.log('works', productid);

    });

});