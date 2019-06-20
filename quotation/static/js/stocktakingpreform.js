/*
stock.js
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

    $( "#dialog-message" ).dialog({
      autoOpen: false,
      height: 230,
      width: 350,
      modal: true,
      buttons: {
        Ok: function() {
          $( this ).dialog( "close" );
        }
      }
    });
    $('.labelbutton').click(function() {
        var productid = $(this).attr( "productid" );

            $.ajax({
                type: 'POST',
                url: 'stocklabellist',

                data: {
                'productid': productid,

                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                },

                success: function(data){

                    $('#stocklabellisttemplate').html(data);
                    //console.log(data);
                },
                error: function(){
                    alert('failure');
                },
                datatype: 'html'

            });

        $( "#dialog-message" ).dialog( "open" );
    });

});