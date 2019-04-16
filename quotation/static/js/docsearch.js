/*
quotation.js
*/

            var msg="Hello Javascript2";
                    console.log(msg);

$(function () {

$('a[href="/quotation/docsearch/"]').parent().addClass('active'); //activate products tab on navbar
    setTimeout(
      function()
      {
            $('#searchbutton').trigger('click');

      }, 500);

    $('#searchbutton').click(function() {

            $.ajax({
                type: 'POST',
                url: 'docsearchcontent',

                data: {
                'docnumber': $('#docnumber').val(),
                'dockindname': $('#dockindname').val(),
                'fromdate': $('#fromdate').val(),
                'todate': $('#todate').val(),
                'company': $('#company').val(),

                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                },

                success: function(data){

                    $('#docsearchtemplate').html(data);
                    //console.log(data);
                },
                error: function(){
                    alert('failure');
                },
                datatype: 'html'

            });
                setTimeout(
                  function()
                  {
                    var companyvalueaccumulator=$('select#company').val();
                    var companyswap=$('select#companyswap').html();
                    $('select#company').html(companyswap);
                    $('select#company').val(companyvalueaccumulator);

                    var dockindnamevalueaccumulator=$('select#dockindname').val();
                    var dockindnameswap=$('select#dockindnameswap').html();
                    $('select#dockindname').html(dockindnameswap);
                    $('select#dockindname').val(dockindnamevalueaccumulator);

                  }, 500);

    });
    $('#searchoutbutton').click(function() {
        $('#docnumber').val("");
        $('#dockindname').val("");
        $('#company').val("");

        $('#searchbutton').trigger('click');
    });

});