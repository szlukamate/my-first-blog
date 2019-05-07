/*
customerorder.js
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
    $('#purchaseordermakebutton').click(function() {

        var customerordersnumber=0;
        var i;
        var docdetailslist=[];
        var docdetailslistmember;
        var tosorqtymember;

        customerordersnumberfunc();

        main();

            function main(){

                for (i = 1; i <= customerordersnumber; i++) {
                    getifchecked();

                }


            }

            function customerordersnumberfunc(){
            customerordersnumber=$('#customerordersnumber').attr( "customerordersnumber" ); //Number of Customer Order Items
            //itemnumbers--; // convert 1-x -> 0-(x-1)
            }
            function getifchecked(){

                    if ($('input[type="checkbox"][rowid="' + i + '"').is(":checked") ) {
                           docdetailslistmember=$('input[type="checkbox"][rowid="' + i + '"').attr( "docdetailsid" );
                           tosorqtymember=$('input[type="checkbox"][rowid="' + i + '"').attr( "tosorqty" );

                           docdetailslist.push(docdetailslistmember, tosorqtymember);
                           console.log('raw' + docdetailslist);
                    }

            }

            $.ajax({
                type: 'POST',
                url: 'purchaseordermake',

                data: {
                'docdetailslist': JSON.stringify(docdetailslist),

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

            console.log('stringified' + JSON.stringify(docdetailslist));

    });
});