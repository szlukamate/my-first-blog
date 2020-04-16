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

    $('a[href="/aid/aorderprocess/"]').parent().addClass('active');
//    var itemlistincart = [];
    cartrefresh();

    var currentstep = 0;
    var maxstep = 2; //only this parameter is needed to adjust if the number of tabs would change
    //initialize tabs
    $( "#tabs" ).tabs({ //first tab let be active
        active: 0,
    });
    $( "#tabs" ).tabs({ disabled: true }); //all tabs are disable
    $( "#tabs" ).tabs("enable", 0); //but first
    $('#previousbutton').prop("disabled", true) //default previousbutton is disabled
    $('#finishbutton').prop("disabled", true) //default finishbutton is disabled

    //addtocartbutton eventlistener script
    $('#addtocartbutton').click(function() {
        addtocartdoc();
    });

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
    $('body').on("click", ".productincreasebutton", function() {
        var docdetalsid = $(this).attr( "docdetalsid" );
        acustomercartincreasingqty(docdetalsid);
    });
    $('body').on("click", ".productdecreasebutton", function() {
        var docdetalsid = $(this).attr( "docdetalsid" );
        acustomercartdecreasingqty(docdetalsid);
    });
    $('body').on("click", ".productremovebutton", function() {
        var docdetalsid = $(this).attr( "docdetalsid" );
        acustomercartproductremove(docdetalsid);
    });

//    function addtocart_main(){

//        var numberofrowsincart = itemlistincart.length/7;
//        var linenumberforrow = numberofrowsincart + 1;
//        var linenumberforrow = 22;

//        var productidvar = $('#addtocartselect').find(":selected").attr('productid');
//        var purchasepricevar = $('#addtocartselect').find(":selected").attr('purchaseprice');
//        var customerdescriptionvar = $('#addtocartselect').find(":selected").attr('customerdescription');
//        var marginvar = $('#addtocartselect').find(":selected").attr('margin');
//        var unitvar = $('#addtocartselect').find(":selected").attr('unit');
//        var currencyisocodevar = $('#addtocartselect').find(":selected").attr('currencyisocode');
//            var customerpricevar=Math.round(purchasepricevar/(1-marginvar/100));

//        itemlistincart.push(linenumberforrow, productidvar, customerpricevar, customerdescriptionvar, marginvar, unitvar, currencyisocodevar );
//                    console.log(linenumberforrow);
//                    console.log(itemlistincart);

//                    addtocart_cartupdate(itemlistincart);
//    }
    function acustomercartincreasingqty(docdetalsid){
                $.ajax({
                    type: 'POST',
                    url: 'acustomercartincreasingqty/',

                    data: {
                    'docdetailsid' : docdetalsid,

                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                    },

                    success: function(){
                      cartrefresh();

                    },
                    error: function(){
                        alert('failure');
                    },
                    datatype: 'html'

                });

    }
    function acustomercartdecreasingqty(docdetalsid){
                $.ajax({
                    type: 'POST',
                    url: 'acustomercartdecreasingqty/',

                    data: {
                    'docdetailsid' : docdetalsid,

                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                    },

                    success: function(){
                      cartrefresh();

                    },
                    error: function(){
                        alert('failure');
                    },
                    datatype: 'html'

                });

    }
    function acustomercartproductremove(docdetalsid){
                $.ajax({
                    type: 'POST',
                    url: 'acustomercartproductremove/',

                    data: {
                    'docdetailsid' : docdetalsid,

                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                    },

                    success: function(){
                      cartrefresh();

                    },
                    error: function(){
                        alert('failure');
                    },
                    datatype: 'html'

                });

    }
    function cartrefresh(){
                $.ajax({
                    type: 'POST',
                    url: 'acustomercartrefresh/',

                    data: {
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                    },

                    success: function(cartcontent){
                      $('#cartitemstemplate').html(cartcontent)

                    },
                    error: function(){
                        alert('failure');
                    },
                    datatype: 'html'

                });

    }
    function addtocartdoc(){
                $.ajax({
                    type: 'POST',
                    url: 'acustomercartadditemtocart/',

                    data: {
                    'productid' : $('#addtocartselect').find(":selected").attr('productid'),
                    'qty' : 3,

                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                    },

                    success: function(url){
                      cartrefresh();

                    },
                    error: function(){
                        alert('failure');
                    },
                    datatype: 'html'

                });

    }
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
        $('input[name="qty2"]').val(ui.value)

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
//    function cartupdate(){

//        var cartitemlinenumber = 1
//        var cartitemproductid = 2
//        var cartitemdescription = 'Escort to Doctor'
//        var cartitemunitprice = 2300
//        var cartitemiso = 'HUF'
//        var cartitemunit = 'hrs'

        //var cartitemlist = []
        //cartitemlist.push(cartitemlinenumber,cartitemproductid,cartitemdescription,cartitemunitprice,cartitemunit,cartitemquantity,cartitemiso)
        //console.log(cartitemlist);

        //cart filling begin
//        $('#cartitemstemplate').text(cartitemlinenumber + '. ' + cartitemdescription + ' ' + window.cartitemquantity + ' ' + cartitemunit + ' ' + cartitemquantity*cartitemunitprice + ' ' + cartitemiso)
        //cart filling end
//    }
//    function addtocart_cartupdate(itemlistincart){
//        var carthtmlphrase = ''
//        var rowsincart = itemlistincart.length/7-1
//         for (j = 0; j < rowsincart+1; j++) {
//            var cartitemlinenumber = itemlistincart[j*7+0]
//            var cartitemproductid = 2
//            var cartitemdescription = itemlistincart[j*7+3]
//            var cartitemunitprice = 2300
//            var cartitemiso = 'HUF'
//            var cartitemunit = 'hrs'
//            var cartitemquantity = 4

//            carthtmlphrase = carthtmlphrase + '<p>' + cartitemlinenumber + '. ' + cartitemdescription + ' ' + cartitemquantity + ' ' + cartitemunit + ' ' + cartitemquantity*cartitemunitprice + ' ' + cartitemiso + '</p><br>'
//            }
//        $('#cartitemstemplate').text(cartitemlinenumber + '. ' + cartitemdescription + ' ' + cartitemquantity + ' ' + cartitemunit + ' ' + cartitemquantity*cartitemunitprice + ' ' + cartitemiso)
//        $('#cartitemstemplate').html(carthtmlphrase)

//    }
//Cart scrpt end
});