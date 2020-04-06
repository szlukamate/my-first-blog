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
    var maxstep = 3; //only this parameter is needed to adjust if the number of tabs would change
    //initialize tabs
    $( "#tabs" ).tabs({ //first tab let be active
        active: 0,
    });
    $( "#tabs" ).tabs({ disabled: true }); //all tabs are disable
    $( "#tabs" ).tabs("enable", 0); //but first
    $('#previousbutton').prop("disabled", true) //default previousbutton is disabled
    $('#finishbutton').prop("disabled", true) //default finishbutton is disabled

    //nextbutton eventlistener script
    $('#nextbutton').click(function() {
        setactivetabtextfilled('next'); //add ' - OK' to the end of tab
        currentstep++;
        tabactivator(); //set appropriate tab to active
    });
    //previousbutton eventlistener script
    $('#previousbutton').click(function() {
        setactivetabtextfilled('previous'); //remove ' - OK' from previous tab
        currentstep--;
        tabactivator(); //set appropriate tab to active
    });
    //finishbutton eventlistener script
    $('#finishbutton').click(function() {
        location.reload();
    });

    function tabactivator(){
            if (currentstep == 0 ) {
                setactivetab(currentstep);
                $('#previousbutton').prop("disabled", true)
            }
            if ((currentstep !== 0) && (currentstep !== maxstep )) {
                setactivetab(currentstep);
                $('#previousbutton').prop("disabled", false)
                $('#finishbutton').prop("disabled", true)
                $('#nextbutton').prop("disabled", false)
            }
            if (currentstep == maxstep ) {
                setactivetab(currentstep);
                $('#nextbutton').prop("disabled", true)
                $('#finishbutton').prop("disabled", false)
            }
    }
    function getactivetabtext(){
        return $("#tabs .ui-tabs-active").text();
    }
    function setactivetabtextfilled(nextorprevious){
            if (nextorprevious === 'next') {
                $('#tabs ul:first li:eq(' + (currentstep) + ') a').text(getactivetabtext() + ' - OK'); //add ' - OK' to the end of tab
            }
            if (nextorprevious === 'previous') {
                //set active the currentstep-1 tab to replace OK
                setactivetab(currentstep-1);
                //previous tab is active thus the 'OK' can be removed from active tab
                $('#tabs ul:first li:eq(' + (currentstep-1) + ') a').text(getactivetabtext().replace(' - OK',''));
            }
    }
    function setactivetab(xstep){
        $( "#tabs" ).tabs({ disabled: false }); //set all tabs to enabled
        $( "#tabs" ).tabs({
            active: '' + (xstep) + '', //set tab active
        });
        $( "#tabs" ).tabs({ disabled: true }); //set all tab to disabled
        $( "#tabs" ).tabs("enable", '' + (xstep + 1) + ''); //except this (this parameter is not 0 indexed so +1)
    }

//Cart scrpt begin
    //aidkind script begin
    var handleaidkind = $( "#custom-handle-aidkind" );
    $( "#slideraidkind" ).slider({
      min: 2,
      max: 20,
      value: 2.5,
      step: 0.50,
      create: function() {
        handleaidkind.text( $( this ).slider( "value" ) );
      },
      slide: function( event, ui ) {
        handleaidkind.text( ui.value );
        window.cartitemquantity = ui.value
        cartupdate();

      }
    });
    //aidkind script end
    //car usage script begin
    var handlecarusage = $( "#custom-handle-carusage" );
    $( "#slidercarusage" ).slider({
      min: 2,
      max: 20,
      value: 2.5,
      step: 0.50,
      create: function() {
        handlecarusage.text( $( this ).slider( "value" ) );
      },
      slide: function( event, ui ) {
        handlecarusage.text( ui.value );
      }
    });
    //car usage script end
    function cartupdate(){

        var cartitemlinenumber = 1
        var cartitemproductid = 2
        var cartitemdescription = 'Escort to Doctor'
        var cartitemunitprice = 2300
        var cartitemiso = 'HUF'
        var cartitemunit = 'hrs'

        //var cartitemlist = []
        //cartitemlist.push(cartitemlinenumber,cartitemproductid,cartitemdescription,cartitemunitprice,cartitemunit,cartitemquantity,cartitemiso)
        //console.log(cartitemlist);

        //cart filling begin
        $('#cartitemstemplate').text(cartitemlinenumber + '. ' + cartitemdescription + ' ' + window.cartitemquantity + ' ' + cartitemunit + ' ' + cartitemquantity*cartitemunitprice + ' ' + cartitemiso)
        //cart filling end
    }
//Cart scrpt end
});