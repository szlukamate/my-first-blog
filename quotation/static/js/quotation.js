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
            var docidinquotationjs = $('#quotationdocidspan').text();
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

    $('.quotationproductforrow').click(function() {
        var quotationid=$('#quotationdocid').text();
        var docdetailsid=$(this).attr( "rowid" );
        console.log('in');
            $.ajax({
                type: 'POST',
                url: 'quotationnewrowadd',

                data: {
                'quotationid' : quotationid,
                'docdetailsid' : docdetailsid, // Only product update the !0 shows it (the quotationnewrowadd def in vw_quotation.py recognizes it)
                'nextfirstnumonhtml' :    $('input[name="firstnum_tblDoc_details"][rowid="' + docdetailsid + '"').val(),
                'nextsecondnumonhtml' : 111,
                'nextthirdnumonhtml' : 111,
                'nextfourthnumonhtml' : 111,

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

});