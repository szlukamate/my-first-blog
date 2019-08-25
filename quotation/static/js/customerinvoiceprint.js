/*
deliverynoteprint.js
*/

            var msg="Hello Javascript2";
                    console.log(msg);

$(window).on("load", function(){

});

$(function () {

var height;
var sumheight=0;
var itemnumbers;
itemnumbers();
var towrap = [];
var i;
var wrapphrase="";
var minitemwrapped;
var maxitemwrapped;
var pagenumber=1;
var total=0;
var totalflag="Total_Off"
var currencycode=$('#currencycodeinreport_tbldoc').text();
main();

    function main(){
        backpagehandling();
        for (i = 0; i <= itemnumbers; i++) {
            measureitemcontainer();
            totalcount(i);
            if (sumheight > 600 ) { // sumheight: sum height of items inspected via cycle
                wrap();
            }
            if (i == itemnumbers) { //last page
            towrap.push(i); //last record to wrap we put to array and wrap
            wrap();
            pagenumberer();
            totalprint();

            return;
            }
            towrap.push(i); //if there is room on page only goes to wrap array

        }

    }
    function backpagehandling(){

            var deliverynoteid = $('#deliverynoteid').text();
            $.ajax({
                type: 'POST',
                url: 'deliverynotebackpage/',

                data: {
                'deliverynoteid' : deliverynoteid,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                },

                success: SearchSuccess,
                error: function(){
                    alert('failure');
                },
                datatype: 'html'

            });

            function SearchSuccess(data, textStatus, jqXHR)
            {
                var deliverydays= $('#deliverydays').text();
                var payment= $('#payment').text();


                $(".backpagetextcontainer").html(function () {
                    return $(this).html().replace("data1", deliverydays);
                });
                $(".backpagetextcontainer").html(function () {
                    return $(this).html().replace("data2", payment);
                });

            }
    }

    function totalprint(){
        totalflag=$('#total').text();
        if (totalflag == "Total_On") {
         $('span[name="totalhtmlinsertspan"][rowid="' + itemnumbers + '"').html('<hr class=\"totalhr\" ><div ><span class="totallabel" >Total: ' + total + ' ' + currencycode + '+VAT</span></div>');
        }
        console.log(totalflag);
    }
    function totalcount(i){
        var val=$('p[name="salesprice"][rowid="' + i + '"').text();
        total=total + Number(val);
    }

    function wrap(){
        pagenumber++;
        minitemwrapped=towrap[0];
        maxitemwrapped=towrap[towrap.length-1];
          for (j = 0; j < towrap.length; j++) {

            wrapphrase= wrapphrase + "div[class=\"item-container-for-measure\"][rowid=\"" + towrap[j] + "\"], "
            }
        wrapphrase = wrapphrase.slice(0, -2); // remove comma from end (-2 cause there is an adding space)
        jQuery.globalEval( "$('" + wrapphrase + "').wrapAll('<div class=\"page\"> </div>');" );
        sumheight=0;
        towrap.length=0;
        wrapphrase="";
        headerinsert(minitemwrapped); // which item insertbefore
        footerinsert(maxitemwrapped, pagenumber);

    }
    function headerinsert(rowid){

    $('span[name="htmlinsertbefore"][rowid="' + rowid + '"').html('<div class="header" ><div class="headerlabels" ><span style="margin-left: 35mm" >Description</span><span style="margin-left: 44mm" >Qty</span><span class="headerlabelunitprice" >Unit Price</span><span class="headerlabelscurrencycodespanforunitprice">in ' + currencycode + '</span><span class="headerlabelsalesprice" >Sales Price</span><span class="headerlabelscurrencycodespanforsalesprice">in ' + currencycode + '</span></div></div>');
    }
    function footerinsert(rowid, pagenumber){
    $('span[name="htmlinsertafter"][rowid="' + rowid + '"').html('<div class="middlepagesfooterdiv" ><hr><span class="middlepagesfooterspan1">Please see the conditions in details on the last page<br></span><span pagenumber=\"' + pagenumber + '\" class="middlepagesfooterspan2">Description2</span><span class="middlepagesfooterspan3">Description3</span></div>');
    }
    function measureitemcontainer(){
    height=$('div[class="item-container-for-measure"][rowid="' + i + '"').outerHeight();
    sumheight=sumheight+height;
    }
    function itemnumbers(){
    itemnumbers=$('#itemnumberp').attr( "itemnumber" ); //number of products
    itemnumbers--; // convert 1-x -> 0-(x-1)
    }
    function pagenumberer(){
            $('#pages').text((pagenumber+1)); // pagenumbers on firstpage
            $('span[class="firstpagefooterspan2"]').text( "page 1/" + (pagenumber+1)); // firstpage footer filling
            $('span[class="firstpagefooterspan3"]').text( "Number of Delivery Note: " + $('#numberofdeliverynote').text()); // firstpage footer filling

            for (k = 1; k != (pagenumber+1); k++) { // for cycle for middlepage numbers
            $('span[class="middlepagesfooterspan2"][pagenumber="' + k + '"').text( "page " + k + "/" + (pagenumber+1));

            }
            $('span[class="middlepagesfooterspan3"]').text( "Number of Delivery Note: " + $('#numberofdeliverynote').text()); // middlepages number of deliverynote filling

            $('span[class="backpagefooterspan2"]').text( "page " + (pagenumber+1) + "/" + (pagenumber+1)); // backpage footer filling
            $('span[class="backpagefooterspan3"]').text( "Number of Delivery Note: " + $('#numberofdeliverynote').text()); // backpage footer filling

    }
});



