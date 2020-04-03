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
    var currentstep = 0;
    var maxstep = 3;
    var othertexttotab = 2;

    $( "#tabs" ).tabs({
        active: 0,  //run when initialized
        //disabled:  disabledstep
    });
    $( "#tabs" ).tabs({ disabled: true });
    $( "#tabs" ).tabs("enable", 0);
//    $('#tabs ul:first li:eq(' & othertexttotab & ') a').text("Other text");
    $('#tabs ul:first li:eq(' + othertexttotab + ') a').text("Other text");

    $('#previousbutton').prop("disabled", true)
    $('#finishbutton').prop("disabled", true)

    $('#nextbutton').click(function() {
        console.log('nextbuttonclick');
        currentstep++;
        tabactivator();
    });
    $('#previousbutton').click(function() {
        console.log('previousbuttonclick');
        currentstep--;
        tabactivator();

    });
    $('#finishbutton').click(function() {
        console.log('finishbuttonclick');
        location.reload();
    });
    function tabactivator(){
            if (currentstep == 0 ) {
                $( "#tabs" ).tabs( "option", "disabled", [ 1, 2, 3 ] )

                $( "#tabs" ).tabs({
                    active: 0,
                });
                $('#previousbutton').prop("disabled", true)

            }

            if ((currentstep !== 0) && (currentstep !== maxstep )) {
                $( "#tabs" ).tabs( "option", "disabled", [ 0, 2 ] )

                $( "#tabs" ).tabs({
                    active: 1,
                });
                $('#previousbutton').prop("disabled", false)
                $('#finishbutton').prop("disabled", true)
                $('#nextbutton').prop("disabled", false)

            }

            if (currentstep == maxstep ) {
                $( "#tabs" ).tabs( "option", "disabled", [ 0, 1 ] )

                $( "#tabs" ).tabs({
                    active: 2,
                });
                $('#nextbutton').prop("disabled", true)
                $('#finishbutton').prop("disabled", false)

            }

    }

});