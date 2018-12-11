/*
quotation.js
*/

            var msg="Hello Javascript2";
                    console.log(msg);
/*
$(window).on("unload", function(){
  alert('Bye.');
});
*/
$(function () {
$('#drag').draggable();

$('#title').click(function() {
    $('#title').hide();

});
   $('.updateablequotation').focusout(function() {

        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        var fieldvalue = $(this).val();
        var rowid = $(this).attr( "rowid" );
        var fieldname = $(this).attr( "name" );



           $.post("", {
           'fieldvalue': fieldvalue,
           'rowid' : rowid,
           'fieldname': fieldname,
           'csrfmiddlewaretoken': CSRFtoken,
           });

//          console.log(data);
            console.log(fieldname, fieldvalue, rowid);

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

});