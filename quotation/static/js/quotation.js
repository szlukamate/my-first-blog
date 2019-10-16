/*
quotation.js
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

// Dialog "Connecting..." begin
    $( "#dialog-message-connecting" ).dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        Ok: function() {
          $( this ).dialog( "close" );
        }
      }
    });

// Dialog "Connecting..." end


    var index1 = 'qpsstats-active-tab1';
    //  Define friendly data store name
    var dataStore1 = window.sessionStorage;
    var oldIndex1 = 0;
    //  Start magic!
    try {
        // getter: Fetch previous value
        oldIndex1 = dataStore1.getItem(index1);
    } catch(e) {}

    $( "#tabs1" ).tabs({
        active: oldIndex1,
        activate: function(event, ui) {
            //  Get future value
            var newIndex1 = ui.newTab.parent().children().index(ui.newTab);
            //  Set future value
            try {
                dataStore1.setItem( index1, newIndex1 );
            } catch(e) {}
        }
    });


    var index2 = 'qpsstats-active-tab2';
    //  Define friendly data store name
    var dataStore2 = window.sessionStorage;
    var oldIndex2 = 0;
    //  Start magic!
    try {
        // getter: Fetch previous value
        oldIndex2 = dataStore2.getItem(index2);
    } catch(e) {}

    $( "#tabs2" ).tabs({
        active: oldIndex2,
        activate: function(event, ui) {
            //  Get future value
            var newIndex2 = ui.newTab.parent().children().index(ui.newTab);
            //  Set future value
            try {
                dataStore2.setItem( index2, newIndex2 );
            } catch(e) {}
        }
    });

$('#title').click(function() {
    $('#title').hide();

});
   $('.updateabletbldocdetails').change(function() {

        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        var fieldvalue = $(this).val();
        var rowid = $(this).attr( "rowid" );
        var fieldname = $(this).attr( "name" );
        var tbl="tblDoc_details";

           $.ajax({
            type: 'POST',
            url: '',

            data: {
           'tbl' : tbl,
           'fieldvalue': fieldvalue,
           'rowid' : rowid,
           'docid' : 0,
           'fieldname': fieldname,
           'csrfmiddlewaretoken': CSRFtoken,
           },
           success: updatesuccess,
           error: updateerror,
           datatype: 'html'
          });

        function updatesuccess (data, textStatus, jqXHR){
            console.log('datafromsql:' + data);
            $('input[name="' + fieldname + '"][rowid="' + rowid + '"').val(data);
            $('#sqlsaving').html('<span  class="glyphicon glyphicon-hdd"></span>');

            setTimeout(
              function()
              {
                $('#sqlsaving').html("");

              }, 500);
            console.log(fieldvalue);
        };
        function updateerror (){
            console.log('Failure in saving');
        };

   });
   $('.updateabletbldoc').change(function() {

        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        var fieldvalue = $(this).val();
        var docid = $('#quotationdocid').text();
        var fieldname = $(this).attr( "name" );
        var tbl="tblDoc";

          $.ajax({
            type: 'POST',
            url: '',

            data: {
           'tbl' : tbl,
           'fieldvalue': fieldvalue,
           'rowid' : 0,
           'docid' : docid,
           'fieldname': fieldname,
           'csrfmiddlewaretoken': CSRFtoken,
           },
           success: updatesuccess,
           error: updateerror,
           datatype: 'html'
          });

        function updatesuccess (data, textStatus, jqXHR){
            console.log('datafromsql:' + data);
            $('input[name="' + fieldname + '"][docid="' + docid + '"').val(data);
            $('#sqlsaving').html('<span  class="glyphicon glyphicon-hdd"></span>');

            setTimeout(
              function()
              {
                $('#sqlsaving').html("");

              }, 500);
            console.log(fieldvalue);
        };
        function updateerror (){
            console.log('Failure in saving');
        };


   });
    /*
    $('.updateabletbldocdetails').click(function() {
        $(this).css("background-color", "yellow");
    });
    $('.updateabletbldocdetails').focusout(function() {
        $(this).css("background-color", "white");
    });
    */



   $('#search').keyup(function() {
            var docidinquotationjs = $('#quotationdocid').text();
            $.ajax({
                type: 'POST',
                url: 'searchquotationcontacts/',

                data: {
                'search_text' : $('#search').val(),
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'docidinquotationjs' : docidinquotationjs
                },

                success: SearchSuccess,
                error: function(){
                    alert('failure');
                },
                datatype: 'html'

            });

            console.log(docidinquotationjs)
            function SearchSuccess(data, textStatus, jqXHR)
            {

            $('#search-results').html(data);

            }
   });
    $('#newquotationrowsignonhtml').click(function() {
        var quotationid=$('#quotationdocid').text();

            $.ajax({
                type: 'POST',
                url: 'quotationnewrowadd',

                data: {
                'quotationid' : quotationid,
                'docdetailsid' : 0, // New row in docdetails the 0 shows it (the quotationnewrowadd def in vw_quotation.py recognizes it)
                'nextfirstnumonhtml' : $('#nextfirstnumonhtml').val(),
                'nextsecondnumonhtml' : $('#nextsecondnumonhtml').val(),
                'nextthirdnumonhtml' : $('#nextthirdnumonhtml').val(),
                'nextfourthnumonhtml' : $('#nextfourthnumonhtml').val(),

                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                },

                success: function(data){

                    $('#quotationtemplate').html(data);
                    console.log(data);
                },
                error: function(){
                    alert('failure');
                },
                datatype: 'html'

            });



    });

    $('[name="quotationproductforrow"]').click(function() {
        var quotationid=$('#quotationdocid').text();
        var docdetailsid=$(this).attr( "rowid" );
        var productid=$('input[name="Productid_tblDoc_details_id"][rowid="' + docdetailsid + '"]').val();
        console.log('in');
            $.ajax({
                type: 'POST',
                url: 'quotationnewrowadd',

                data: {
                'quotationid' : quotationid,
                'docdetailsid' : docdetailsid, // Only product update the !0 shows it (the quotationnewrowadd def in vw_quotation.py recognizes it)
                'nextfirstnumonhtml' :    $('input[name="firstnum_tblDoc_details"][rowid="' + docdetailsid + '"').val(),
                'nextsecondnumonhtml' : $('input[name="secondnum_tblDoc_details"][rowid="' + docdetailsid + '"').val(),
                'nextthirdnumonhtml' : $('input[name="thirdnum_tblDoc_details"][rowid="' + docdetailsid + '"').val(),
                'nextfourthnumonhtml' : $('input[name="fourthnum_tblDoc_details"][rowid="' + docdetailsid + '"').val(),

                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                },

                success: function(data){

                    $('#quotationtemplate').html(data);
                    console.log(data);
                    location.href = "#" + productid;
                },
                error: function(){
                    alert('failure');
                },
                datatype: 'html'

            });



    });
    $('.selection').change(function() {

        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        var fieldvalue = $(this).val();
        var quotationdocid = $('#quotationdocid').text();
        var fieldname = $(this).attr( "fieldname" );
        console.log('quotationdocid:' + quotationdocid);
            $.ajax({
            type: 'POST',
            url: 'quotationuniversalselections/',

            data: {
           'fieldvalue': fieldvalue,
           'quotationdocid' : quotationdocid,
           'fieldname': fieldname,
           'csrfmiddlewaretoken': CSRFtoken,
           },
           success: updatesuccess,
           error: updateerror,
           datatype: 'html'
          });

        function updatesuccess (data, textStatus, jqXHR){
            console.log('datafromsql:' + data);
            var fromsql= data[0]

            $('select[class="selection"][fieldname="' + fieldname + '"] option:selected').html(fromsql);


            $('#sqlsaving').html('<span  class="glyphicon glyphicon-hdd"></span>');

            setTimeout(
              function()
              {
                $('#sqlsaving').html("");

              }, 500);

        };
        function updateerror (){
            console.log('Failure in saving');
        };

   });

    $('#itsbutton').click(function() {
        var quotationid=$('#quotationdocid').text();
/*
                  // send it out
                  let xhr = new XMLHttpRequest();
//                  xhr.open("GET","https://cors-anywhere.herokuapp.com/http://13.58.18.245:3000//time_entries.xml?key=6a722899382b3495828b3f2d6c41f93d19adb5f6&project_id=4"); // https://cors-anywhere.herokuapp.com the header exchanger proxy server
                  xhr.open("GET","https://ancient-sierra-24943.herokuapp.com/http://13.58.18.245:3000//time_entries.xml?key=6a722899382b3495828b3f2d6c41f93d19adb5f6&status_id=1"); // https://cors-anywhere.herokuapp.com the header exchanger proxy server
                  xhr.send();
                  $( "#dialog-message-connecting" ).dialog("option", "buttons", {}); //remove OK button
                  $( "#dialog-message-connecting" ).dialog( "open" );

                  xhr.onload = function (){
                                    console.log(xhr.response);
                  $( "#dialog-message-connecting" ).dialog( "close" );
*/
                  $( "#dialog-message-connecting" ).dialog( "open" );

                    $.ajax({
                        type: 'POST',
                        url: 'quotationissuetrackingsystem',

                        data: {
                        'quotationid': quotationid,
                        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                        },

                        success: function(data){
                        $( "#dialog-message-connecting" ).dialog( "close" );
                        $('#quotationtemplate').html(data);
                        //template dates setting begin
                        setTimeout(
                          function()
                          {

                            $('#onlyforopenprojects').prop('checked', true);
                            $('#unquotedcheckbox').prop('checked', true);

                            $("#addfilterselect option[value=projectstatus]").attr('selected', 'selected'); // open this filter field
                            $('#addfilterselect').trigger('change');

                            $("#addfilterselect option[value=quoteddocdetailsid]").attr('selected', 'selected'); // open this filter field
                            $('#addfilterselect').trigger('change');

                            $("#addfilterselect option[value=datespenton]").attr('selected', 'selected'); // open this filter field
                            $('#addfilterselect').trigger('change');

                            setTimeout(
                              function()
                              {

                                    var d = new Date();

                                    var fromyear = d.getFullYear()-1; //-1 cause one year diff between fromdate and todate
                                    var frommonth = d.getMonth()+1; // +1 cause 0-11 the javascript months
                                    var fromday = d.getDate();

                                    var fromoutput = fromyear + '-' +
                                        (frommonth<10 ? '0' : '') + frommonth + '-' +
                                        (fromday<10 ? '0' : '') + fromday;
//                                    $('#fromdate').val(fromoutput);
                                    $('.firstinputbox[filteritemname="datespenton"]').val(fromoutput);

                                    var d = new Date();

                                    var toyear = d.getFullYear();
                                    var tomonth = d.getMonth()+1; // +1 cause 0-11 the javascript months
                                    var today = d.getDate();

                                    var tooutput = toyear + '-' +
                                        (tomonth<10 ? '0' : '') + tomonth + '-' +
                                        (today<10 ? '0' : '') + today;
//                                    $('#todate').val(tooutput);
                                    $('.secondinputbox[filteritemname="datespenton"]').val(tooutput);


                                    $('#filterbutton').trigger('click');
                              }, 1000);


                          }, 250);

                        //template dates setting end


                        },
                        error: function(){

                            alert('failure');
                        },
                        datatype: 'html'

//                    });

                    });


    });

    $('body').on("click", "#timeentriestoquotationbutton", function() {
                var issuetrackingsystemnumberofitems= $('#issuetrackingsystemnumberofitems').text();
                var itemdatalist=[];
                var itemdataliststringified;
                var quotationdocid = $('#quotationdocid').text();
                var quotationdocnumber = $('#quotationdocnumber').text();

        main();

            function main(){


                for (i = 1; i <= issuetrackingsystemnumberofitems; i++) {
                    itemdatacollect(i);

                }
                itemdataliststringified = JSON.stringify(itemdatalist);
                    console.log(issuetrackingsystemnumberofitems);
                    console.log(itemdataliststringified);

                datatransmit();

            }
            function itemdatacollect(i){
              timeentryid=$('p[class="timeentryid"][rowid="' + (i - 1) + '"]').text();
                    console.log('timeentryid: ' + timeentryid);

              timeentryandissueid=$('td[class="timeentryandissueid"][rowid="' + (i - 1) + '"]').text();
              projectname=$('td[class="projectname"][rowid="' + (i - 1) + '"]').text();
              username=$('td[class="username"][rowid="' + (i - 1) + '"]').text();
              activityname=$('td[class="activityname"][rowid="' + (i - 1) + '"]').text();
              hours=$('td[class="hours"][rowid="' + (i - 1) + '"]').text();
              comments=$('td[class="comments"][rowid="' + (i - 1) + '"]').text();
              spenton=$('td[class="spenton"][rowid="' + (i - 1) + '"]').text();
              itemdatalist.push(timeentryid, timeentryandissueid, projectname, username, activityname, hours, comments, spenton);

                    console.log('itemdatalist: ' + itemdatalist);

            }

            function datatransmit(){

                $.ajax({
                    type: 'POST',
                    url: 'quotationissuetrackingsystemitemstoquotation',

                    data: {
                    'quotationdocid' : quotationdocid,
                    'quotationdocnumber' : quotationdocnumber,
                    'issuetrackingsystemnumberofitems' : issuetrackingsystemnumberofitems,
                    'itemdatalist': itemdataliststringified,

                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                    },

                    success: function(url){
                    console.log('success');

                    window.location.href = url;

                    },
                    error: function(){
                        alert('failure');
                    },
                    datatype: 'html'

                });
            }

    });
    $('#updateitsbutton').click(function() {
        var quotationid=$('#quotationdocid').text();

                  // send it out
                  let xhr = new XMLHttpRequest();
//                  xhr.open("GET","https://cors-anywhere.herokuapp.com/http://13.58.18.245:3000//time_entries.xml?key=6a722899382b3495828b3f2d6c41f93d19adb5f6"); // https://cors-anywhere.herokuapp.com the header exchanger proxy server
//                  xhr.open("POST","https://ancient-sierra-24943.herokuapp.com/http://13.58.18.245:3000//time_entries.xml?key=6a722899382b3495828b3f2d6c41f93d19adb5f6&project_id=4&activity_id=8"); // https://xxxxxxxx.herokuapp.com the header exchanger proxy server (own)
                  xhr.open("POST","https://ancient-sierra-24943.herokuapp.com/http://13.58.18.245:3000//projects.xml?key=6a722899382b3495828b3f2d6c41f93d19adb5f6&name=%20na"); // https://xxxxxxxx.herokuapp.com the header exchanger proxy server (own)
                  xhr.send();
                  $( "#dialog-message-connecting" ).dialog("option", "buttons", {}); //remove OK button
                  $( "#dialog-message-connecting" ).dialog( "open" );

                  xhr.onload = function (){
                                    console.log(xhr.response);
                  $( "#dialog-message-connecting" ).dialog( "close" );

                    $.ajax({
                        type: 'POST',
                        url: 'quotationissuetrackingsystempostitems',

                        data: {
                        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                        },

                        success: function(data){
//                    $('#quotationtemplate').html(data);
                                    console.log('success');

                        },
                        error: function(){

                            alert('failure');
                        },
                        datatype: 'html'

                    });

                  };


    });
    $('body').on("click", "#filterbutton", function() {

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
                url: 'quotationissuetrackingsystemsearchcontent',

                data: {

                'filteritemlist': filteritemliststringified,

                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                },

                success: function(data){

                    $('#timeentrysearchtemplate').html(data);
console.log('searchphraseformainresults: '+ $('#searchphraseformainresults').text());

                },
                error: function(){
                    alert('failure');
                },
                datatype: 'html'

            });
        }


/*
            $.ajax({
                type: 'POST',
                url: 'quotationissuetrackingsystemsearchcontent',

                data: {
                'quoteddocnumber': $('#quoteddocnumber').val(),
                'timeentryid': $('#timeentryid').val(),
                'fromdate': $('#fromdate').val(),
                'todate': $('#todate').val(),
                'projectname': $('#projectname').val(),
                'userid': $('#username').val(),
                'activityid': $('#activityname').val(),
                'onlyforopenprojects': $('#onlyforopenprojects').prop('checked'),
                'unquotedcheckbox': $('#unquotedcheckbox').prop('checked'),

                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                },

                success: function(data){

                    $('#timeentrysearchtemplate').html(data);
                    //console.log(data);

                    setTimeout(
                      function()
                      {

                        var projectnamevalueaccumulator=$('select#projectname').val(); // swap options of select element after html template refresh
                        var projectnameswap=$('select#projectnameswap').html();
                        $('select#projectname').html(projectnameswap);
                        $('select#projectname').val(projectnamevalueaccumulator);

                        var usernamevalueaccumulator=$('select#username').val();
                        var usernameswap=$('select#usernameswap').html();
                        $('select#username').html(usernameswap);
                        $('select#username').val(usernamevalueaccumulator);

                        var activitynamevalueaccumulator=$('select#activityname').val();
                        var activitynameswap=$('select#activitynameswap').html();
                        $('select#activityname').html(activitynameswap);
                        $('select#activityname').val(activitynamevalueaccumulator);

                      }, 500);


                },
                error: function(){
                    alert('failure');
                },
                datatype: 'html'

            });
*/
    });
    $('body').on("click", "#filteroutbutton", function() {


        $('#filtertemplate').html('<!-- Empty -->');

        $('#filterbutton').trigger('click');


    });
    $('body').on("keypress", "#timeentryid", function(event) {
        if (event.keyCode == 13) {
            $('#searchbutton').trigger('click');
        }
    });

    $('body').on("keypress", "#quoteddocnumber", function(event) {
        if (event.keyCode == 13) {
            $('#searchbutton').trigger('click');
        }
    });
    $('body').on("change", "#addfilterselect", function(event) {
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
                    url: 'filtertemplatehtmlonquotationtimeentryform',

                    data: {

                    'searchphraseformainresults': $('#searchphraseformainresults').text(),
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
    $('body').on("click", ".enabledfiltercheckbox", function() {

        var filteritemrowid = $(this).attr( "filteritemrowid" );
        $('.filteritemtemplate[filteritemrowid="' + filteritemrowid + '"]').toggle();
        $('.filteritemselect[filteritemrowid="' + filteritemrowid + '"]').toggle();



    });
    $('body').on("change", ".filteritemselect", function() {

        var filteritemrowid = $(this).attr( "filteritemrowid" );
        var filteritemname = $(this).attr( "filteritemname" );

                    $.ajax({
                    type: 'POST',
                    url: 'filtertemplatehtmlonquotationtimeentryform',

                    data: {

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

});