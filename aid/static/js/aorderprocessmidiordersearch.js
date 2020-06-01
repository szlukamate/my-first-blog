/*
aorderprocessmidiordersearch.js
*/

            var msg="Hello Javascript2";
                    console.log(msg);

$(function () {

$('a[href="/aid/aorderprocessmidiordersearch/"]').parent().addClass('active');

    setTimeout(
      function()
      {
            $('#docnumber').val(sessionStorage.docnumber);
            $('#dockindname').val(sessionStorage.dockindname);

            if (typeof sessionStorage.fromdate === 'undefined') {

                var d = new Date();

                var fromyear = d.getFullYear()-1; //-1 cause one year diff between fromdate and todate
                var frommonth = d.getMonth()+1; // +1 cause 0-11 the javascript months
                var fromday = d.getDate();

                var fromoutput = fromyear + '-' +
                    (frommonth<10 ? '0' : '') + frommonth + '-' +
                    (fromday<10 ? '0' : '') + fromday;
                sessionStorage.fromdate = fromoutput;
                $('#fromdate').val(fromoutput);
                //console.log(sessionStorage.fromdate);

            } else {
            $('#fromdate').val(sessionStorage.fromdate);

            }

            if (typeof sessionStorage.todate === 'undefined') {

                var d = new Date();

                var toyear = d.getFullYear();
                var tomonth = d.getMonth()+1; // +1 cause 0-11 the javascript months
                var today = d.getDate();

                var tooutput = toyear + '-' +
                    (tomonth<10 ? '0' : '') + tomonth + '-' +
                    (today<10 ? '0' : '') + today;
                sessionStorage.todate = tooutput;
                $('#todate').val(tooutput);
                //console.log(sessionStorage.todate);

            } else {
            $('#todate').val(sessionStorage.todate);

            }


            $('#company').val(sessionStorage.company);

            $('#searchbutton').trigger('click');

      }, 500);

    $('#searchbutton').click(function() {

            $.ajax({
                type: 'POST',
                url: 'adocsearchcontent/',

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
                    var companyvalueaccumulator=$('select#company').val(); // swap options of select element after html template refresh
                    var companyswap=$('select#companyswap').html();
                    $('select#company').html(companyswap);
                    $('select#company').val(companyvalueaccumulator);

                    var dockindnamevalueaccumulator=$('select#dockindname').val();
                    var dockindnameswap=$('select#dockindnameswap').html();
                    $('select#dockindname').html(dockindnameswap);
                    $('select#dockindname').val(dockindnamevalueaccumulator);

                  }, 500);
        sessionStorage.docnumber = $('#docnumber').val();
        sessionStorage.dockindname = $('#dockindname').val();
        sessionStorage.fromdate = $('#fromdate').val();
        sessionStorage.todate = $('#todate').val();
        sessionStorage.company = $('#company').val();

    });
    $('#searchoutbutton').click(function() {
        $('#docnumber').val("");
        sessionStorage.docnumber = ""

        $('#dockindname').val("");
        sessionStorage.dockindname = ""

        $('#company').val("");
        sessionStorage.company = ""

        $('#searchbutton').trigger('click');

        //console.log(rowid);

    });
    $('body').on("click", ".linkable", function() { //save search conditions before jump
        var djangourl = $(this).attr('hrefdjango');
        sessionStorage.docnumber = $('#docnumber').val();
        sessionStorage.dockindname = $('#dockindname').val();
        sessionStorage.fromdate = $('#fromdate').val();
        sessionStorage.todate = $('#todate').val();
        sessionStorage.company = $('#company').val();

        //console.log(sessionStorage.docnumber);

       window.location.href = djangourl;
    });
    $('#docnumber').keypress(function(event) {
        if (event.keyCode == 13) {
            $('#searchbutton').trigger('click');
        }
    });


});

