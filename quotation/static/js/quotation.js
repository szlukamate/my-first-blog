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



<<<<<<< HEAD


=======
>>>>>>> aab59635ca3ec79857281d64a90704dcd3b4576f
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
<<<<<<< HEAD
            var docidinquotationjs = $('#quotationdocidspan').text();
=======
>>>>>>> aab59635ca3ec79857281d64a90704dcd3b4576f
            $.ajax({
                type: 'POST',
                url: 'searchquotationcontacts/',

                data: {
                'search_text' : $('#search').val(),
<<<<<<< HEAD
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'docidinquotationjs' : docidinquotationjs
=======
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
>>>>>>> aab59635ca3ec79857281d64a90704dcd3b4576f
                },

                success: SearchSuccess,
                error: function(){
                    alert('failure');
                },
                datatype: 'html'

            });

<<<<<<< HEAD
            console.log(docidinquotationjs)
=======
            console.log('Works')
>>>>>>> aab59635ca3ec79857281d64a90704dcd3b4576f
            function SearchSuccess(data, textStatus, jqXHR)
            {

            $('#search-results').html(data);
<<<<<<< HEAD

=======
            console.log(data);
>>>>>>> aab59635ca3ec79857281d64a90704dcd3b4576f

            }
        });

});