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
    initMap();
// Dialog "Sending Your Order..." begin
    $( "#dialog-message-sendingyourorder" ).dialog({
      autoOpen: false,
      modal: true
    });
// Dialog "Sending Your Order..." end
    $('a[href="/aid/aorderprocess/"]').parent().addClass('active');
    var sessionidforanonymoususer = window.sessionStorage;
//    var anonymoususerid=sessionidforanonymoususer.setItem("anonymoususerid", 0);
    var loadervisibilitydelaydoneflag = 0;
    var loadervisibilitydatadoneflag = 0;
    var sendingyourordervisibilitydelaydoneflag = 0;
    var sendingyourordervisibilitydatadoneflag = 0;
    var currentstep = 0;
    var maxstep = 1; //only this parameter is needed to adjust if the number of tabs would change
    var pricetagtocarttopvalue = 0;
    loaderstartingandsetting('Starting');
    cartrefresh();
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
        acustomercartsaveasorder();
//        location.reload();
    });
    $('body').on("click", ".productincreasebutton", function() {
        var docdetailsid = $(this).attr( "docdetailsid" );
        acustomercartincreasingordecreasing(docdetailsid, 'increasing');
    });
    $('body').on("click", ".productdecreasebutton", function() {
        var docdetailsid = $(this).attr( "docdetailsid" );
        acustomercartincreasingordecreasing(docdetailsid, 'decreasing');
    });
    $('body').on("click", ".productremovebutton", function() {
        var docdetailsid = $(this).attr( "docdetailsid" );
        acustomercartproductremove(docdetailsid);
    });
    function acustomercartincreasingordecreasing(docdetailsid, upordownflag){
        var maxqty = $('span[name="maxqtyincart"][docdetailsid="' + docdetailsid + '"]').html();
        var currentqty = $('span[class="qtynumber"][docdetailsid="' + docdetailsid + '"]').html();
        var unitsalespriceACU = Number($('span[class="unitsalespriceACU"][docdetailsid="' + docdetailsid + '"]').html()).toFixed(0);
        //var lisprice = $('span[class="listprice"][docdetailsid="' + docdetailsid + '"]').html();
        var incrementedqty = Number(currentqty) + 1;
        var decrementedqty = Number(currentqty) - 1;
        incrementedqty = incrementedqty.toFixed(2);
        decrementedqty = decrementedqty.toFixed(2);
        maxqty = Number(maxqty);
        if (upordownflag === 'increasing' ) {
                    $('span[class="qtynumber"][docdetailsid="' + docdetailsid + '"]').html(incrementedqty);
                    $('span[class="salesprice"][docdetailsid="' + docdetailsid + '"]').html(unitsalespriceACU*incrementedqty);
                    acustomercartincreasingqty(docdetailsid);
            if (incrementedqty >= maxqty ) {
                    $('[class="productincreasebutton"][docdetailsid="' + docdetailsid + '"]').prop('disabled', true);
                    $('[class="maxtag"][docdetailsid="' + docdetailsid + '"]').prop('hidden', false);
            }
        }
        if (upordownflag === 'decreasing' ) {
                    $('span[class="qtynumber"][docdetailsid="' + docdetailsid + '"]').html(decrementedqty);
                    $('span[class="salesprice"][docdetailsid="' + docdetailsid + '"]').html(unitsalespriceACU*decrementedqty);
            if (decrementedqty <= maxqty ) {
                    $('[class="productincreasebutton"][docdetailsid="' + docdetailsid + '"]').prop('disabled', false);
                    $('[class="maxtag"][docdetailsid="' + docdetailsid + '"]').prop('hidden', true);
            }
            if (decrementedqty <= 0 ) {
                    acustomercartproductremove(docdetailsid);
            }
            else
            {
                    acustomercartdecreasingqty(docdetailsid);
            }
        }
    }
    function acustomercartincreasingqty(docdetailsid){
                loaderstartingandsetting('Adding');
                $.ajax({
                    type: 'POST',
                    url: 'acustomercartincreasingqty/',

                    data: {
                    'docdetailsid' : docdetailsid,

                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                    },

                    success: function(){
                        pricetagtocarttop();
                    },
                    error: function(){
                        alert('failure');
                    },
                    datatype: 'html'
                });
    }
    function acustomercartdecreasingqty(docdetailsid){
                loaderstartingandsetting('Removing');
                $.ajax({
                    type: 'POST',
                    url: 'acustomercartdecreasingqty/',

                    data: {
                    'docdetailsid' : docdetailsid,

                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                    },

                    success: function(){
                        pricetagtocarttop();
                    },
                    error: function(){
                        alert('failure');
                    },
                    datatype: 'html'
                });
    }
    function acustomercartproductremove(docdetailsid){
                loaderstartingandsetting('Removing');
                $.ajax({
                    type: 'POST',
                    url: 'acustomercartproductremove/',

                    data: {
                    'docdetailsid' : docdetailsid,

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
                anonymoususerid = anonymoususer();
                $.ajax({
                    type: 'POST',
                    url: 'acustomercartrefresh/',

                    data: {
                    'anonymoususerid' : anonymoususerid,
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                    },

                    success: function(cartcontent){
                      $('#cartitemstemplate').html(cartcontent)
                      pricetagtocarttop();
                    },
                    error: function(){
                        alert('failure');
                    },
                    datatype: 'html'
                });
                    console.log('in cartrefresh:' + anonymoususerid);

    }
    function loaderstartingandsetting(messagetag){
                loadervisibilitydelaydoneflag = 0;
                loadervisibilitydatadoneflag = 0;
                showloader(messagetag);
                setTimeout(
                  function()
                  {
                  loadervisibilitydelaydoneflag = 1;
                  hideloader();
                  }, 3000);
    }
    function addtocartdoc(){
                loaderstartingandsetting('Adding');
                    console.log('in addtocart anonymousid: ' + anonymoususer());

                $.ajax({
                    type: 'POST',
                    url: 'acustomercartadditemtocart/',

                    data: {
                    'anonymoususerid' : anonymoususer(),
                    'productid' : $('#addtocartselect').find(":selected").attr('productid'),
                    'qty' : 3,

                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                    },
                    success: function(x){
                      cartrefresh();
                    },
                    error: function(){
                        alert('failure');
                    },
                    datatype: 'html'
                });

    }
    function anonymoususer(){
                anonymoususerid = sessionidforanonymoususer.getItem('anonymoususerid');
                $.ajax({
                    type: 'POST',
                    url: 'acustomercartaddinganonymoususerid/',

                    data: {
                    'anonymoususerid' : anonymoususerid,
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                    },
                    success: function(x){
                    sessionidforanonymoususer.setItem( 'anonymoususerid', x );

                    },
                    error: function(){
                        alert('failure');
                    },
                    datatype: 'html',
                    async: false
                });
                    anonymoususerid = sessionidforanonymoususer.getItem('anonymoususerid');
                    console.log(anonymoususerid);

                    return anonymoususerid
    }
    function showloader(messagetag){
                $('#carttoptemplate').html('<div class="loader"></div><div class="messagetagincarttop">' + messagetag + '</div>');
    }
    function hideloader(){
            if ((loadervisibilitydelaydoneflag === 1) && (loadervisibilitydatadoneflag === 1 )) {
                $('#carttoptemplate').html('<div class="glyphicon glyphicon-shopping-cart"></div><div class="messagetagincarttop">' + 'Guide Price' + '</div><div class="pricetagincarttop">' + pricetagtocarttopvalue + ' HUF</div>').fadeOut(1);
                $('#carttoptemplate').html('<div class="glyphicon glyphicon-shopping-cart"></div><div class="messagetagincarttop">' + 'Guide Price' + '</div><div class="pricetagincarttop">' + pricetagtocarttopvalue + ' HUF</div>').fadeIn(500);
                loadervisibilitydatadoneflag = 0; // to prevent flashing the pricetagincarttop template because of multi invoke this function
            }
    }
    function pricetagtocarttop(){
                anonymoususerid = sessionidforanonymoususer.getItem('anonymoususerid');

                $.ajax({
                    type: 'POST',
                    url: 'acustomercartpricetagtocarttop/',

                    data: {

                    'anonymoususerid': anonymoususerid,
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                    },
                    success: function(pricetag){
                    pricetagtocarttopvalue = pricetag;
                    loadervisibilitydatadoneflag = 1;
                    hideloader();
                    },
                    error: function(){
                        alert('failure');
                    },
                    datatype: 'html'
                });
    }
    function acustomercartsaveasorder(){
                $.ajax({
                    type: 'POST',
                    url: 'acustomercartsaveasorder/',

                    data: {
                    'aidstartdate' : $('#aidstartdate').val(),
                    'aidstarttime' : $('#aidstarttime').val(),
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                    },
                    success: function(url){
                    console.log(url);

                    window.location.href = url;

                    },
                    error: function(){
                        alert('failure');
                    },
                    datatype: 'html'
                });
    }
    function showsendingyourorder(){
                $( "#dialog-message-sendingyourorder" ).dialog( "open" );
    }
    function hidesendingyourorder(){
            if ((sendingyourordervisibilitydelaydoneflag === 1) && (sendingyourordervisibilitydatadoneflag === 1 )) {
                    $( "#dialog-message-sendingyourorder" ).dialog( "close" );
            }
    }
    function sendingyourorderstartingandsetting(){
                sendingyourordervisibilitydelaydoneflag = 0;
                sendingyourordervisibilitydatadoneflag = 0;
                showsendingyourorder();
                setTimeout(
                  function()
                  {
                  sendingyourordervisibilitydelaydoneflag = 1;
                  hidesendingyourorder();
                    console.log('q');

                  }, 3000);
    }
    function tabactivator(){
            if (currentstep == 0 ) {
                setactivetab(currentstep);
                $('#previousbutton').prop("disabled", true)
                $('#nextbutton').prop("disabled", false)
                $('#finishbutton').prop("disabled", true)
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
                $('#previousbutton').prop("disabled", false)
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
    $( "#aidstartdate" ).datepicker({ dateFormat: 'yy-mm-dd', minDate: -20, maxDate: "+10D" });
    $( "#aidstartdate" ).datepicker( "setDate", new Date ); //set today
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

     function initMap() {
            var myLatlng = {lat: 46.26873280379492, lng: 20.13837369751033};
            var map = new google.maps.Map(
                document.getElementById('map'), {zoom: 14, center: myLatlng, mapTypeId: 'hybrid'});

            // Create the initial InfoWindow.
            var infoWindow = new google.maps.InfoWindow(
                {content: 'Click the map to get Lat/Lng!', position: myLatlng});
            infoWindow.open(map);

            // Configure the click listener.
            map.addListener('click', function(mapsMouseEvent) {
              // Close the current InfoWindow.
              infoWindow.close();

              // Create a new InfoWindow.
              infoWindow = new google.maps.InfoWindow({position: mapsMouseEvent.latLng});
              infoWindow.setContent(mapsMouseEvent.latLng.toString());
              infoWindow.open(map);
              console.log('raw: ' + mapsMouseEvent.latLng.toString());
              var coordinates = mapsMouseEvent.latLng.toString().split(",")
              var clickedlat = coordinates[0];
              clickedlat = clickedlat.tostring();
              console.log('clickedlat: ' + clickedlat);
              var clickedlng = coordinates[1];
              console.log('clickedlng: ' + clickedlng);
              var coordinates2 = coordinates.toString().substring(1,5);
              console.log('processed: ' + coordinates2);

            });
     }
    calculateDistance();

/*
      function calculateDistance(origin, destination) {
        var service = new google.maps.DistanceMatrixService();
        service.getDistanceMatrix(
        {
          origins: ['46.252103811613274,20.146751170256003'],
          destinations: ['46.253103811613274,20.146751170256003'],
          travelMode: google.maps.TravelMode.WALKING,
          unitSystem: google.maps.UnitSystem.IMPERIAL,
          avoidHighways: false,
          avoidTolls: false
        }, callback());
      }

      function callback(response, status) {
        console.log(distance.value);

        if (status != google.maps.DistanceMatrixStatus.OK) {
          $('#result').html(err);
        } else {
          var origin = response.originAddresses[0];
          var destination = response.destinationAddresses[0];
          if (response.rows[0].elements[0].status === "ZERO_RESULTS") {
            $('#result').html("Better get on a plane. There are no roads between "
                              + origin + " and " + destination);
          } else {
            var distance = response.rows[0].elements[0].distance;
            var distance_value = distance.value;
            var distance_text = distance.text;
            var miles = distance_text.substring(0, distance_text.length - 3);
            $('#result').html("It is " + miles + " miles from " + origin + " to " + destination);
          }
        }
      }

      $('#distance_form').submit(function(e){
          event.preventDefault();
          var origin = $('#origin').val();
          var destination = $('#destination').val();
          var distance_text = calculateDistance(origin, destination);
      });
*/
      function calculateDistance() {
        var service = new google.maps.DistanceMatrixService();
        service.getDistanceMatrix(
            {
              origins: ['46.252103811613274,20.146751170256003'],
              destinations: ['46.466103812613274,20.146751170256003'],
              travelMode: google.maps.TravelMode.WALKING,
              unitSystem: google.maps.UnitSystem.METRIC,
              avoidHighways: false,
              avoidTolls: false
            }, function (response, status)
            {
            console.log('st:' + status);
                if (status != google.maps.DistanceMatrixStatus.OK)
                    {
                      $('#result').html(err);
                    } else
                    {
                      var origin = response.originAddresses[0];
                      var destination = response.destinationAddresses[0];
                      if (response.rows[0].elements[0].status === "ZERO_RESULTS")
                          {
                            $('#result').html("Better get on a plane. There are no roads between "
                                              + origin + " and " + destination);
                          } else
                          {
                            var distance = response.rows[0].elements[0].distance;
                            var duration = response.rows[0].elements[0].duration;
                            var distance_value = distance.value;
                            var duration_value = duration.value;
                            var distance_text = distance.text;
                            var duration_text = duration.text;
                            var miles = distance_text.substring(0, distance_text.length - 3);
                            var seconds = duration_text.substring(0, duration_text.length - 3);
                            $('#result').html('<p>It is ' + miles + ' miles from ' + origin + ' to ' + destination + '</p><p>It is ' + seconds + ' seconds</p>' );
                          }
                    }



            }
        )
      };


});