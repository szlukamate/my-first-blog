/*
purchaseorderpre.js
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
    var filteritemmaxrowid=0;

    setTimeout(
      function()
      {


            //$("#addfilterselect option[value=dateofcorcreation]").attr('selected', 'selected'); // open and autofocus for this filter field
            //$('#addfilterselect').trigger('change');
            $("#addfilterselect option[value=docnumber]").attr('selected', 'selected'); // open and autofocus for this filter field
            $('#addfilterselect').trigger('change');
                setTimeout(
              function()
              {
                    $('.firstinputbox[filteritemname="docnumber"]').val(176);

              },200);

            setTimeout(
              function()
              {

                    var d = new Date();
                    d.setDate(d.getDate()-14); // -14 days for fromdate

                    var fromyear = d.getFullYear();
                    var frommonth = d.getMonth()+1; // +1 cause 0-11 the javascript months
                    var fromday = d.getDate();

                    var fromoutput = fromyear + '-' +
                        (frommonth<10 ? '0' : '') + frommonth + '-' +
                        (fromday<10 ? '0' : '') + fromday;
                    $('.firstinputbox[filteritemname="dateofcorcreation"]').val(fromoutput);

                    var d = new Date();

                    var toyear = d.getFullYear();
                    var tomonth = d.getMonth()+1; // +1 cause 0-11 the javascript months
                    var today = d.getDate();

                    var tooutput = toyear + '-' +
                        (tomonth<10 ? '0' : '') + tomonth + '-' +
                        (today<10 ? '0' : '') + today;
                    $('.secondinputbox[filteritemname="dateofcorcreation"]').val(tooutput);


                    $('#filterbutton').trigger('click');
              }, 1000);

      }, 500);

//    $('#purchaseordermakebutton').click(function() {
    $('body').on("click", "#purchaseordermakebutton", function() {

        var customerordersnumber=0;
        var i;
        var docdetailslist=[];
        var docdetailslistmember;
        var tosorqtymember;

        customerordersnumberfunc();

        main();

            function main(){
                customerordersnumberfunc();

                for (i = 1; i <= customerordersnumber; i++) {
                    getifchecked();

                }


            }

            function customerordersnumberfunc(){
            customerordersnumber=$('#customerordersnumber').attr( "customerordersnumber" ); //Number of Customer Order Items
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
    $('#filterbutton').click(function() {
    var filteritemlist = []
    main();

        function main(){
            addfilterselectalloptionsenable();
            $("#filteritemlistelementvaluesaccumulatortemplate").html('<!--Empty-->') // emptying filteritems accumulator

            for (i = 1; i <= filteritemmaxrowid; ++i) {
            getfilteritemparamaters(i);
            }

            filteritemliststringified = JSON.stringify(filteritemlist);

            filteritemlisttransmit();
        }
        function addfilterselectthisoptiondisable(filteritemnamevar){
            $('#addfilterselect option').each(function() {
                if ($(this).val() == filteritemnamevar) {
                   $(this).prop('disabled', true);
                }
            });

        }
        function addfilterselectalloptionsenable(){
            $('#addfilterselect option').each(function() {
                $(this).prop('disabled', false);
            });

        }
        function getfilteritemparamaters(i){
            if ($('.enabledfiltercheckbox[filteritemrowid="' + i + '"]').is(":checked")) {

                filteritemnamevar = $('.enabledfiltercheckbox[filteritemrowid="' + i + '"]').attr( "filteritemname" );
                filteritemselectedvaluevar = $('.filteritemselect[filteritemrowid="' + i + '"]').val();
                firstinputbox = $('.firstinputbox[filteritemrowid="' + i + '"]').val();
                if (typeof firstinputbox === "undefined") {
                    firstinputbox = ''
                }
                secondinputbox = $('.secondinputbox[filteritemrowid="' + i + '"]').val();
                if (typeof secondinputbox === "undefined") {
                    secondinputbox = ''
                }

                 //filteritems to temporary store /to accumulator/ (because the filteritem values are vanished after adding a new filteritems ...cont...
                 // therefore put out to site and copy this values to the already existing filter items)
                $("#filteritemlistelementvaluesaccumulatortemplate").append('<input type="text" class="filteritemlistelementvaluesaccumulator_name" value="' + filteritemnamevar + '" filteritemrowid="' + i + '">');
                $("#filteritemlistelementvaluesaccumulatortemplate").append('<input type="text" class="filteritemlistelementvaluesaccumulator_selectedvalue" value="' + filteritemselectedvaluevar + '" filteritemrowid="' + i + '">');
                $("#filteritemlistelementvaluesaccumulatortemplate").append('<input type="text" class="filteritemlistelementvaluesaccumulator_firstinputbox" value="' + firstinputbox + '" filteritemrowid="' + i + '">');
                $("#filteritemlistelementvaluesaccumulatortemplate").append('<input type="text" class="filteritemlistelementvaluesaccumulator_secondinputbox" value="' + secondinputbox + '" filteritemrowid="' + i + '">');
                $("#filteritemlistelementvaluesaccumulatortemplate").append('<br>');

                filteritemlist.push(filteritemnamevar, filteritemselectedvaluevar, firstinputbox, secondinputbox);

                addfilterselectthisoptiondisable(filteritemnamevar);

            }
            if ($('.enabledfiltercheckbox[filteritemrowid="' + i + '"]').is(":checked") == false) { //checked out filteritems remove
                $('.enabledfiltercheckbox[filteritemrowid="' + i + '"]').prev().prev().remove(); //line before previos (<br>) remove
                $('.enabledfiltercheckbox[filteritemrowid="' + i + '"]').prev().remove(); //line previous (csrfmiddlewaretoken) remove
                $('.enabledfiltercheckbox[filteritemrowid="' + i + '"]').remove();
                $('.selectedoption[filteritemrowid="' + i + '"]').remove();
                $('.filteritemselect[filteritemrowid="' + i + '"]').remove();
                $('span[class="filteritemtemplate"][filteritemrowid="' + i + '"]').remove();
            }


        }
        function filteritemlisttransmit(){
                    console.log(filteritemliststringified);

            $.ajax({
                type: 'POST',
                url: 'purchaseorderpre/',

                data: {

                'filteritemlist': filteritemliststringified,

                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                },

                success: function(data){

                    $('#productsearchtemplate').html(data);
                },
                error: function(){
                    alert('failure');
                },
                datatype: 'html'

            });
        }
    });
    $('#addfilterselect').change(function() {
        filteritemmaxrowid++;
        var optionValues = [];

        $('#addfilterselect option').each(function() {
            optionValues.push($(this).attr( "value" ));
        });
        var selectedvalue = $('#addfilterselect').val()
        var selectedoption = $('#addfilterselect option:selected').text()
        $("#addfilterselect option:selected").attr('disabled','disabled')
        $('#addfilterselect').val("");

        searchphraseformainresults_var = $('#searchphraseformainresults').text()
                if ( searchphraseformainresults_var == "") {
                    searchphraseformainresults_var = 'a'
                }

                    $.ajax({
                    type: 'POST',
                    url: 'filtertemplatehtmlonpurchaseorderpreform',

                    data: {
                    'searchphraseformainresults': searchphraseformainresults_var,
                    'invokedfrom': 'addfilterselectchanged',
                    'filteritemmaxrowid': filteritemmaxrowid,
                    'selectedvalue': selectedvalue,
                    'selectedoption': selectedoption,
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                    },

                    success: UpdateSuccess3,
                    error: function(){
                       console.log('ajax failure');
                    },
                    complete: function(){

                    },

                    datatype: 'json'

                    });

                    function UpdateSuccess3(data, textStatus, jqXHR)
                    {

                    $("#filtertemplate").append(data);
                            setTimeout(
                              function()
                              {

                                  filteritemvaluesfromaccumulator(); // filteritem values from accumulator to eliminate vanish effect after new addfilter (see above - keyword: accumulator)
                              }, 250);

console.log('searchphraseformainresults_var: '+ searchphraseformainresults_var);

                    $('.filteritemselect').trigger('change');
                    }
                    function filteritemvaluesfromaccumulator(){
                        for (i = 1; i <= (filteritemmaxrowid-1); ++i) { // filteritemmaxrowid already contains new filteritem which has not accumulated value
                        copyfilteritemvaluesfromaccumulator(i);
                        }

                    }
                    function copyfilteritemvaluesfromaccumulator(){
                    temp_firstinputbox = $('input[class="filteritemlistelementvaluesaccumulator_firstinputbox"][filteritemrowid="' + i + '"]').val()
                    $('input[class="firstinputbox"][filteritemrowid="' + i + '"]').val(temp_firstinputbox)

                    temp_secondinputbox = $('input[class="filteritemlistelementvaluesaccumulator_secondinputbox"][filteritemrowid="' + i + '"]').val()
                    $('input[class="secondinputbox"][filteritemrowid="' + i + '"]').val(temp_secondinputbox)


                    }




    });
    $('body').on("change", ".filteritemselect", function() {

        var filteritemrowid = $(this).attr( "filteritemrowid" );
        var filteritemname = $(this).attr( "filteritemname" );

        searchphraseformainresults_var = $('#searchphraseformainresults').text()
                if ( searchphraseformainresults_var == "") {
                    searchphraseformainresults_var = 'a'
                }


                    $.ajax({
                    type: 'POST',
                    url: 'filtertemplatehtmlonpurchaseorderpreform',

                    data: {
                    'searchphraseformainresults': searchphraseformainresults_var,
                    'invokedfrom': 'filteritemselectchanged',
                    'filteritemrowid': filteritemrowid,
                    'filteritemname': filteritemname,
                    'filteritemselectedvalue': $('.filteritemselect[filteritemrowid="' + filteritemrowid + '"]').val(),

                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                    },

                    success: UpdateSuccess3,
                    error: function(){
                       console.log('ajax failure');
                    },
                    complete: function(){

                    },

                    datatype: 'json'

                    });

                    function UpdateSuccess3(data, textStatus, jqXHR)
                    {
                    $('.filteritemtemplate[filteritemrowid="' + filteritemrowid + '"]').html(data);
                    $('.firstinputbox').focus();

                    }



    });
    $('#filteroutbutton').click(function() {

        $('#filtertemplate').html('<!-- Empty -->');

        $('#filterbutton').trigger('click');


    });
    $('body').on("keypress", ".firstinputbox", function(event) {
        if (event.keyCode == 13) {
            $('#filterbutton').trigger('click');
        }
    });
    $('body').on("click", ".enabledfiltercheckbox", function() {

        var filteritemrowid = $(this).attr( "filteritemrowid" );
        $('.filteritemtemplate[filteritemrowid="' + filteritemrowid + '"]').toggle();
        $('.filteritemselect[filteritemrowid="' + filteritemrowid + '"]').toggle();



    });
    $('#checkallbutton').click(function() {

        var customerordersnumber=0;
        var i;
        var docdetailslist=[];
        var docdetailslistmember;
        var tosorqtymember;

        customerordersnumberfunc();

        main();

            function main(){
                customerordersnumberfunc();

                for (i = 1; i <= customerordersnumber; i++) {

                            setchecked(i);

                }

            }

            function customerordersnumberfunc(){
            customerordersnumber=$('#customerordersnumber').attr( "customerordersnumber" ); //Number of Customer Order Items
            }
            function setchecked(i){
                    setTimeout(
                      function()
                      {
                        $('input[type="checkbox"][rowid="' + i + '"').prop('checked', true);

                      },200*i);

            }

    });
    $('#uncheckallbutton').click(function() {

        var customerordersnumber=0;
        var i;
        var docdetailslist=[];
        var docdetailslistmember;
        var tosorqtymember;

        customerordersnumberfunc();

        main();

            function main(){
                customerordersnumberfunc();

                for (i = 1; i <= customerordersnumber; i++) {

                            setchecked(i);

                }

            }

            function customerordersnumberfunc(){
            customerordersnumber=$('#customerordersnumber').attr( "customerordersnumber" ); //Number of Customer Order Items
            }
            function setchecked(i){
                    setTimeout(
                      function()
                      {
                        $('input[type="checkbox"][rowid="' + i + '"').prop('checked', false);

                      },200*i);

            }

    });

});