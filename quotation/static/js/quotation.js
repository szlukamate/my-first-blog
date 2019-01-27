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
$("#tabs").tabs();

$('#title').click(function() {
    $('#title').hide();

});
   $('.updateablequotation').focusout(function() {

        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        var fieldvalue = $(this).val();
        var rowid = $(this).attr( "rowid" );
        var fieldname = $(this).attr( "name" );
        var tbl="tblDoc_details";

           $.post("", {
           'tbl' : tbl,
           'fieldvalue': fieldvalue,
           'rowid' : rowid,
           'fieldname': fieldname,
           'csrfmiddlewaretoken': CSRFtoken,
           });

            console.log("tbldocdetails" + fieldname, fieldvalue, rowid);

   });
   $('.updateabletbldoc').focusout(function() {

        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        var fieldvalue = $(this).val();
        var docid = $('#quotationdocid').text();
        var fieldname = $(this).attr( "name" );
        var tbl="tblDoc";


           $.post("", {
           'tbl' : tbl,
           'fieldvalue': fieldvalue,
           'docid' : docid,
           'fieldname': fieldname,
           'csrfmiddlewaretoken': CSRFtoken,
           });

            console.log("tbldoc" + fieldname, fieldvalue, docid);

   });

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
        var productid=$('input[name="Productid_tblDoc_details_id"][rowid="' + docdetailsid + '"').val()
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

});