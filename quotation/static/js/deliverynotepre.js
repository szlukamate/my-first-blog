/*
deliverynotepre.js
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
    $('#deliverynotemakebutton').click(function() {
        var rowsnumber=0;
        var i;
        var productidlist=[];
        var poproductid;
        var podocid;
        var cordocid;

        var dateofarrival = $('#select-resultarrivaldates').text()

        main();

            function main(){
                rowsnumberfunc();

                for (i = 1; i <= rowsnumber; i++) {
                    getrowdetails();

                }


            }

            function rowsnumberfunc(){
            rowsnumber=$('#rowsnumber').attr( "rowsnumber" );
            }
            function getrowdetails(){

                    if ($('td[loopid="' + i + '"][name="onstock"]').text() != '0.0') {
                           productid=$('td[loopid="' + i + '"').attr( "productid" );

                           productidlist.push(productid);
                           console.log('raw' + productidlist);
                    }

            }

            $.ajax({
                type: 'POST',
                url: 'deliverynotemake',

                data: {
                'customerordernumber' : $('#customerordernumber').text(),
                'productidlist': JSON.stringify(productidlist),

                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                },

                success: function(url){
//                window.location.href = url;

                },
                error: function(){
                    alert('failure');
                },
                datatype: 'html'

            });

            console.log('stringified' + JSON.stringify(productidlist));

    });
});