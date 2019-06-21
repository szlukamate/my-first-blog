/*
stocktakingpreform.js
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

    $('.newbutton').click(function() {
        var stockid = $(this).attr( "stockid" );

            $.ajax({
                type: 'POST',
                url: 'stocknewdocforstocktaking',

                data: {
                'stockid': stockid,

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
    $('.copybutton').click(function() {
        var stockid = $(this).attr( "stockid" );
        var latestdisabledstocktakingdenotimestamp = $(this).attr( "latestdisabledstocktakingdenotimestamp" );

            $.ajax({
                type: 'POST',
                url: 'stockcopyfromtimestampforstocktaking',

                data: {
                'stockid': stockid,
                'latestdisabledstocktakingdenotimestamp': latestdisabledstocktakingdenotimestamp,

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