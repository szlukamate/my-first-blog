/*
timemanager.js
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

            $('#filterbutton').trigger('click');

            $("#addfilterselect option[value=projectid]").attr('selected', 'selected'); // open and autofocus for this filter field
            $('#addfilterselect').trigger('change');

      }, 500);

   $('body').on("focusout", ".updateable", function() {


        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        var fieldvalue = $(this).val();
        var rowid = $(this).attr( "timedoneid" );
        var fieldname = $(this).attr( "name" );



                   $.ajax({
                        type: 'POST',
                        url: 'timemanagerfieldupdate',

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
    $('body').on("click", ".updateable", function() {

        $(this).css("background-color", "yellow");


   });
    $('#filterbutton').click(function() {
    var filteritemlist = []
    main();

        function main(){
            addfilterselectalloptionsenable();
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
                secondinputbox = $('.secondinputbox[filteritemrowid="' + i + '"]').val();
                if (typeof secondinputbox === "undefined") {
                    secondinputbox = ''
                }
                filteritemlist.push(filteritemnamevar, filteritemselectedvaluevar, firstinputbox, secondinputbox);

                addfilterselectthisoptiondisable(filteritemnamevar);

            }
            if ($('.enabledfiltercheckbox[filteritemrowid="' + i + '"]').is(":checked") == false) { //checked out filteritems remove
                $('.enabledfiltercheckbox[filteritemrowid="' + i + '"]').remove();
                $('.selectedoption[filteritemrowid="' + i + '"]').remove();
            }
        }
        function filteritemlisttransmit(){
                    console.log(filteritemliststringified);

            $.ajax({
                type: 'POST',
                url: 'timemanagersearchcontent',

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
                    url: 'filtertemplatehtmlontimemanagerform',

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
                    $('.filteritemselect').trigger('change');

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
                    url: 'filtertemplatehtmlontimemanagerform',

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
                    url: 'timemanagerupdateprojectselect',

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

                    $('#auxfunctionforissueselectoptions').trigger('click', projectidsql); // relevant issue select options for project

                    }

    });
    $('body').on("change", ".userselection", function() {
            timedoneid = $(this).attr( "timedoneid" )
                    $.ajax({
                    type: 'POST',
                    url: 'timemanagerupdateuserselect',

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
                    url: 'timemanagerupdateissueselect',

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

                    }

    });
    $('body').on("click", "#timedonesuploadtoitsbutton", function() {
                var timedonesnumberofitems= $('#timedonesnumberofitems').text();
                var itemdatalist=[];
                var itemdataliststringified;
                //var quotationdocid = $('#quotationdocid').text();
                //var quotationdocnumber = $('#quotationdocnumber').text();

        main();

            function main(){


                for (i = 1; i <= timedonesnumberofitems; i++) {
                    itemdatacollect(i);

                }
                itemdataliststringified = JSON.stringify(itemdatalist);
                    console.log(timedonesnumberofitems);
                    console.log(itemdataliststringified);

                datatransmit();

            }
            function itemdatacollect(i){
              //timedoneid=$('input[class="timedoneid"][rowid="' + (i - 1) + '"]').val();
              //      console.log(i);
              //      console.log('timedoneid: ' + timedoneid);

              timedoneid=$('input[class="timedoneid"][rowid="' + (i - 1) + '"]').val();
              projectid=$('input[class="projectid"][rowid="' + (i - 1) + '"]').val();
              userid=$('input[class="userid"][rowid="' + (i - 1) + '"]').val();
              issueid=$('input[class="issueid"][rowid="' + (i - 1) + '"]').val();
              hours=$('input[name="hours_tbltimedone"][rowid="' + (i - 1) + '"]').val();
              comments=$('input[name="comments_tbltimedone"][rowid="' + (i - 1) + '"]').val();
              spenton=$('input[name="spenton_tbltimedone"][rowid="' + (i - 1) + '"]').val();

              projectname=$('td[class="projectname"][rowid="' + (i - 1) + '"]').text();
              username=$('td[class="username"][rowid="' + (i - 1) + '"]').text();
              activityname=$('td[class="activityname"][rowid="' + (i - 1) + '"]').text();
              //hours=$('td[class="hours"][rowid="' + (i - 1) + '"]').text();
              //comments=$('td[class="comments"][rowid="' + (i - 1) + '"]').text();
              //spenton=$('td[class="spenton"][rowid="' + (i - 1) + '"]').text();
              itemdatalist.push(timedoneid, projectid, userid, issueid, hours, comments, spenton );

                    console.log('itemdatalist: ' + itemdatalist);

            }

            function datatransmit(){

                $.ajax({
                    type: 'POST',
                    url: 'timemanageruploadtoits',

                    data: {
                    //'quotationdocid' : quotationdocid,
                    //'quotationdocnumber' : quotationdocnumber,
                    'timedonesnumberofitems' : timedonesnumberofitems,
                    'itemdatalist': itemdataliststringified,

                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                    },

                    success: function(url){
                    console.log('success');

                    //window.location.href = url;

                    },
                    error: function(){
                        alert('failure');
                    },
                    datatype: 'html'

                });
            }

    });
    $('#auxfunctionforissueselectoptions').click(function(event, projectid) {
                    //console.log('auxfunctionforissueselectoptions ' + timedoneid);


                    $.ajax({
                    type: 'POST',
                    url: 'timemanagerupdateissueselectafterchangeprojectselect',

                    data: {

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
/*
                    var projectidsql= data[0][0];
                    var projectnamesql= data[0][1];

                    $('select[class="projectselection"][timedoneid="' + timedoneid + '"] option:selected').html(projectnamesql);
                    $('input[class="projectid"][timedoneid="' + timedoneid + '"]').val(projectidsql)

                    $('#auxfunctionforissueselectoptions').trigger('click'); // relevant issue select options for project
*/
                    }

    });

});