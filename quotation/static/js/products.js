/*
quotation.js
*/

            var msg="Hello Javascript2";
                    console.log(msg);
$(function () {

$('#title').click(function() {
    $('#title').hide();

});
   $('.updateable').focusout(function() {

        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        var fieldvalue = $(this).val();
        var rowid = $(this).attr( "rowid" );
        var fieldname = $(this).attr( "name" );



           $.ajax({
                type: 'POST',
                url: '',

                data: {
                'fieldvalue': fieldvalue,
                'rowid' : rowid,
                'fieldname': fieldname,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                },
                success:function(){
                    $('input[name="' + fieldname + '"][rowid="' + rowid + '"').css("background-color", "white");
                    $('#sqlsavingfeedbackproduct').html('<span  class="glyphicon glyphicon-hdd"></span>');

/*
                    setTimeout(
                      function()
                      {
                        $('#sqlsavingfeedbackproduct').unhide();

                      }, 400);
*/
                    setTimeout(
                      function()
                      {
                        $('#sqlsavingfeedbackproduct').html("");

                      }, 500);
                    console.log(fieldvalue);
                            },
                error: function(){
                    alert('failure');
                },


                datatype: 'html'


                });
                console.log(fieldname, fieldvalue, rowid);
           });

   $('.updateable').click(function() {
        $(this).css("background-color", "yellow");

//          console.log(data);
            console.log('click event');

           });

   $('#search').keyup(function() {
            $.ajax({
                type: 'POST',
                url: 'searchquotationcontacts/',

                data: {
                'search_text' : $('#search').val(),
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                },

                success: SearchSuccess,
                error: function(){
                    alert('failure');
                },
                datatype: 'html'

            });

            console.log('Works')
            function SearchSuccess(data, textStatus, jqXHR)
            {

            $('#search-results').html(data);
            console.log(data);

            }
    });
   $('.currencychoiceselect').change(function() {

        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        var fieldvalue = $(this).val();
        var rowid = $(this).attr( "productid" );
        var fieldname = $(this).attr( "name" );
        console.log('fieldvalue:' + fieldvalue, 'rowid:' + rowid, 'fieldname:' + fieldname );


           $.ajax({
                type: 'POST',
                url: '',

                data: {
                'fieldvalue': fieldvalue,
                'rowid' : rowid,
                'fieldname': fieldname,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                },
                success:function(){
                    $('input[name="' + fieldname + '"][rowid="' + rowid + '"').css("background-color", "white");
                    $('#sqlsavingfeedbackproduct').html('<span  class="glyphicon glyphicon-hdd"></span>');

                    setTimeout(
                      function()
                      {
                        $('#sqlsavingfeedbackproduct').html("");

                      }, 500);
                },

                error: function(){
                    alert('failure');
                },


                datatype: 'html'


                });


    });
});