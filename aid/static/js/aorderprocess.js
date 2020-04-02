/*
aorderprocess.js
*/

            var msg="Hello Javascript2";
                    console.log(msg);

                    // Store
localStorage.lastname = "Smith";
// Retrieve
 console.log(localStorage.lastname);
$(function () {
    $( "#tabs" ).tabs({
        active: 0,  //run when initialized
        activate: function(event, ui) {  //run when clicked
            //  Get future value
            var newIndex1 = ui.newTab.parent().children().index(ui.newTab);
             console.log(newIndex1);

            //  Set future value
            //try {
            //    dataStore1.setItem( index1, newIndex1 );
            //} catch(e) {}
        }
    });

//    $( "#tabs" ).tabs( { disabled: [0, 1] } );
    $('#nextbutton').click(function() {
             console.log('newIndex1');
        $( "#tabs" ).tabs({
            active: 1,  //run when initialized
        });

    });
});