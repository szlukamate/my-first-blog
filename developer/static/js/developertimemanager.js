/*
developertimemanager.js
*/

            var msg="Hello Javascript2";
                    console.log(msg);
$(function () {
    var filteritemmaxrowid=0;


    $('#title').click(function() {
        $('#title').hide();
    });

    setTimeout(
      function()
      {

            $("#addfilterselect option[value=timeentryid]").attr('selected', 'selected'); // open and autofocus for this filter field
            $('#addfilterselect').trigger('change');

            $("#addfilterselect option[value=rowenabledformanager]").attr('selected', 'selected'); // open and autofocus for this filter field
            $('#addfilterselect').trigger('change');
            setTimeout(
              function()
              {

                                    $('#auxfunctionfordatespentondefaultfill').trigger('click');
                                    $('#filterbutton').trigger('click');

              }, 1000);

      }, 500);

   $('body').on("change", ".updateable", function() {


        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        var fieldvalue = $(this).val();
        var rowid = $(this).attr( "timedoneid" );
        var fieldname = $(this).attr( "name" );



                   $.ajax({
                        type: 'POST',
                        url: 'timemanagerdevfieldupdate',

                        data: {
                        'fieldvalue': fieldvalue,
                        'rowid' : rowid,
                        'fieldname': fieldname,
                        'csrfmiddlewaretoken': CSRFtoken
                        },
                        success: updatesuccess,
                        error: updateerror,




                        datatype: 'html'


                   });
                            function updatesuccess (data, textStatus, jqXHR){
                                console.log('datafromsql:' + data);
                                $('input[name="' + fieldname + '"][timedoneid="' + rowid + '"').css("background-color", "white").val(data);
                                $('#sqlsavingfeedbackproduct').html('<span  class="glyphicon glyphicon-hdd"></span>');

                                setTimeout(
                                  function()
                                  {
                                    $('#sqlsavingfeedbackproduct').html("");

                                  }, 500);
                                console.log(fieldvalue);
                            };
                            function updateerror (){
                                alert('Failure in saving');
                            };

   });
    $('#filterbutton').click(function() {
    var filteritemlist = []
    main();

        function main(){
            $( "#dialog-message-requesting" ).dialog( "open" ); // Requesting...

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
                url: 'timemanagerdevsearchcontent',

                data: {

                'filteritemlist': filteritemliststringified,

                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                },

                success: function(data){

                    $( "#dialog-message-requesting" ).dialog( "close" ); // Requesting... close

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

        console.log('addfilterselect invoke event');

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
                    url: 'filtertemplatehtmlontimemanagerdevform',

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

//console.log('searchphraseformainresults_var: '+ searchphraseformainresults_var);

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
                       console.log('filteritemselect event invoked');

        var filteritemrowid = $(this).attr( "filteritemrowid" );
        var filteritemname = $(this).attr( "filteritemname" );

        searchphraseformainresults_var = $('#searchphraseformainresults').text()
                if ( searchphraseformainresults_var == "") {
                    searchphraseformainresults_var = 'a'
                }


                    $.ajax({
                    type: 'POST',
                    url: 'filtertemplatehtmlontimemanagerdevform',

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
//                       console.log('filteritemname: ' + $('.filteritemtemplate[filteritemrowid="' + filteritemrowid + '"]').attr('filteritemname'));
                    if ($('.filteritemtemplate[filteritemrowid="' + filteritemrowid + '"]').attr('filteritemname') == 'datespenton') {
                                    $('#auxfunctionfordatespentondefaultfill').trigger('click');
                    }
                    $('.firstinputbox').focus();

                    }



    });
    $('body').on("click", ".enabledfiltercheckbox", function() {

        var filteritemrowid = $(this).attr( "filteritemrowid" );
        $('.filteritemtemplate[filteritemrowid="' + filteritemrowid + '"]').toggle();
        $('.filteritemselect[filteritemrowid="' + filteritemrowid + '"]').toggle();



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
    $('body').on("change", ".projectselection", function() {
            timedoneid = $(this).attr( "timedoneid" )
                    $.ajax({
                    type: 'POST',
                    url: 'timemanagerdevupdateprojectselect',

                    data: {

                    'projectidinjs' : $(this).val(),
                    'projectnameinjs' : $( ".projectselection[timedoneid='" + timedoneid + "'] option:selected" ).text(),
                    'timedoneidinjs' : timedoneid,
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                    },

                    success: UpdateSuccess,
                    error: function(){
                       console.log('ajax failure');
                    },
                    complete: function(){

                        console.log('ajax done');
                    },

                    datatype: 'json'

                    });

                    function UpdateSuccess(data, textStatus, jqXHR)
                    {
                    console.log(data);
                    var projectidsql= data[0][0];
                    var projectnamesql= data[0][1];

                    $('select[class="projectselection"][timedoneid="' + timedoneid + '"] option:selected').html(projectnamesql);
                    $('input[class="projectid"][timedoneid="' + timedoneid + '"]').val(projectidsql)

                    $('#auxfunctionforissueselectoptions').trigger('click', ["" + timedoneid + "" , "" + projectidsql + ""]); // relevant issue select options for project

                    }

    });
    $('body').on("change", ".userselection", function() {
            timedoneid = $(this).attr( "timedoneid" )
                    $.ajax({
                    type: 'POST',
                    url: 'timemanagerdevupdateuserselect',

                    data: {

                    'useridinjs' : $(this).val(),
                    'usernameinjs' : $( ".userselection[timedoneid='" + timedoneid + "'] option:selected" ).text(),
                    'timedoneidinjs' : timedoneid,
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                    },

                    success: UpdateSuccess,
                    error: function(){
                       console.log('ajax failure');
                    },
                    complete: function(){

                        console.log('ajax done');
                    },

                    datatype: 'json'

                    });

                    function UpdateSuccess(data, textStatus, jqXHR)
                    {
                    console.log(data);
                    var useridsql= data[0][0];
                    var usernamesql= data[0][1];

                    $('select[class="userselection"][timedoneid="' + timedoneid + '"] option:selected').html(usernamesql);
                    $('input[class="userid"][timedoneid="' + timedoneid + '"]').val(useridsql)

                    }

    });
    $('body').on("change", ".issueselection", function() {
            timedoneid = $(this).attr( "timedoneid" )
                    $.ajax({
                    type: 'POST',
                    url: 'timemanagerdevupdateissueselect',

                    data: {

                    'issueidinjs' : $(this).val(),
                    'issuesubjectinjs' : $( ".issueselection[timedoneid='" + timedoneid + "'] option:selected" ).text(),
                    'timedoneidinjs' : timedoneid,
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                    },

                    success: UpdateSuccess,
                    error: function(){
                       console.log('ajax failure');
                    },
                    complete: function(){

                        console.log('ajax done');
                    },

                    datatype: 'json'

                    });

                    function UpdateSuccess(data, textStatus, jqXHR)
                    {
                    console.log(data);
                    var issueidsql= data[0][0];
                    var issuesubjectsql= data[0][1];

                    $('select[class="issueselection"][timedoneid="' + timedoneid + '"] option:selected').html(issuesubjectsql);
                    $('input[class="issueid"][timedoneid="' + timedoneid + '"]').val(issueidsql)

                    $('input[class="issueid"][timedoneid="' + timedoneid + '"]').css("background-color", ""); //remove red background

                    }

    });
    $('#auxfunctionforissueselectoptions').click(function(event, timedoneid, projectid) {
                    console.log('projectid in aux: ' + projectid);
                    console.log('timedoneid in aux: ' + timedoneid);


                    $.ajax({
                    type: 'POST',
                    url: 'timemanagerdevupdateissueselectafterchangeprojectselect',

                    data: {

                    'timedoneidinjs' : timedoneid,
                    'projectidinjs' : projectid,
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                    },

                    success: UpdateSuccess,
                    error: function(){
                       console.log('ajax failure');
                    },
                    complete: function(){

                        console.log('ajax done');
                    },

                    datatype: 'json'

                    });

                    function UpdateSuccess(data, textStatus, jqXHR)
                    {
                    console.log(data);
                    $('select[class="issueselection"][timedoneid="' + timedoneid + '"]').html(data);
                    $('input[class="issueid"][timedoneid="' + timedoneid + '"]').css("background-color", "red");
                    $('select[class="issueselection"][timedoneid="' + timedoneid + '"]').val('');

                    }

    });
    $( "#dialog" ).dialog({
      autoOpen:false,
      modal: true,
      buttons: {
        Ok: function() {
          $( this ).dialog( "close" );

        }
      },
      open: function() {
          var useridemptyintimedoneid = $(this).data('useridemptyintimedoneid');
          $('#useridemptyintimedoneid').text(useridemptyintimedoneid);

      }

    });

// Dialog "Uploading..."  begin
    $( "#dialog-message" ).dialog({
      autoOpen: false,
      modal: true
    });
// Dialog "Uploading..." end

// Dialog "Requesting..."  begin
    $( "#dialog-message-requesting" ).dialog({
      autoOpen: false,
      modal: true
    });
// Dialog "Requesting..." end

    $('body').on("click", "#auxfunctionfordatespentondefaultfill", function() {

                                    var d = new Date();

                                    var fromyear = d.getFullYear()-1; //-1 cause one year diff between fromdate and todate
                                    var frommonth = d.getMonth()+1; // +1 cause 0-11 the javascript months
                                    var fromday = d.getDate();

                                    var fromoutput = fromyear + '-' +
                                        (frommonth<10 ? '0' : '') + frommonth + '-' +
                                        (fromday<10 ? '0' : '') + fromday;
                                    $('.firstinputbox[filteritemname="datespenton"]').val(fromoutput);

                                    var d = new Date();

                                    var toyear = d.getFullYear();
                                    var tomonth = d.getMonth()+1; // +1 cause 0-11 the javascript months
                                    var today = d.getDate();

                                    var tooutput = toyear + '-' +
                                        (tomonth<10 ? '0' : '') + tomonth + '-' +
                                        (today<10 ? '0' : '') + today;
                                    $('.secondinputbox[filteritemname="datespenton"]').val(tooutput);



    });
    $('body').on("change", ".rowenabledformanager", function() {

        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        var timedoneid = $(this).attr( "timedoneid" );
        var checkedvalue = $(this).prop( "checked" );

           $.ajax({
            type: 'POST',
            url: 'timemanagerdevrowenabledformanager',

            data: {
           'timedoneid' : timedoneid,
           'checkedvalue' : checkedvalue,
           'csrfmiddlewaretoken': CSRFtoken,
           },
           success: updatesuccess,
           error: updateerror,
           datatype: 'html'
          });
        function updatesuccess (data, textStatus, jqXHR){
            console.log('datafromsql:' + data);
        };

        function updateerror (){
            console.log('Failure in saving');
        };

    });

});