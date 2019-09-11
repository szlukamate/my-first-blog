/*
customerinvoiceprint.js
*/

            var msg="Hello Javascript2";
                    console.log(msg);

$(window).on("load", function(){

});

$(function () {
// remarks frame height begin
var text = $("#remarkstextarea").text();
var div = $('<div id="temp" style="width:85mm;  white-space:pre-line; "></div>');
div.text(text);
$('body').append(div);
var divHeight = $('#temp').height();
div.remove();

$("#remarkstextarea").height( divHeight );
$("#frameremarks").height( divHeight + 20 );
// remarks frame height end

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
var wrapfirstpagedone=0;
var total=0;
var vattotal=0;
var totalflag="Total_Off"
var currencycode=$('#currencycodeinreport_tbldoc').text();
main();

    function main(){

//        backpagehandling();
        for (i = 0; i <= itemnumbers; i++) {
            measureitemcontainer();
            totalcount(i);

            if (sumheight > 400  && pagenumber == 1 && wrapfirstpagedone == 0 ) { // some items to first page if there is enough room

                wrapfirstpage();
            }
            if (sumheight > 600  ) { // remain items to more pages, sumheight: sum height of items inspected via cycle

                wrap();
            }
                            console.log(wrapfirstpagedone);

            if (i == itemnumbers) { //last page
            towrap.push(i); //last record to wrap we put to array and wrap
  //                  console.log(wrapfirstpagedone);

            if (wrapfirstpagedone == 0) {
            wrapfirstpage();
            }
            wrap();

            pagenumberer();
            totalprint();

            return;
            }
            towrap.push(i); //if there is room on page only goes to wrap array
 //                   console.log(sumheight);

        }

    }
    function backpagehandling(){

            var customerinvoiceid = $('#customerinvoiceid').text();

            $.ajax({
                type: 'POST',
                url: 'customerinvoicebackpage/',

                data: {
                'customerinvoiceid' : customerinvoiceid,
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
        var totalflag=$('#total').text();


//        var totalunfixed = Number(totalunfixed);
        var totalfixed = total.toFixed(2);
        var vattotalfixed = vattotal.toFixed(2);
//                    console.log(vattotalfixed);


        if (totalflag == "Total_On") {
         $('span[name="totalhtmlinsertspan"][rowid="' + itemnumbers + '"').html('<hr class=\"totalhr\" ><div ><span class="totallabel" >Gross Price Total: ' + totalfixed + ' ' + currencycode + '<br></span><span class="totallabel" >VAT Value Total: ' + vattotalfixed + ' ' + currencycode + '</span></div>');
        }
    }
    function totalcount(i){
        var val=$('p[name="grosspricediv"][rowid="' + i + '"').text();
        var vatval=$('p[name="vatvaluediv"][rowid="' + i + '"').text();
        total=total + Number(val);
        vattotal=vattotal + Number(vatval);
//                            console.log(val);

    }

    function wrapfirstpage(){
//        pagenumber++;
        wrapfirstpagedone = 1;
                            console.log('wrapfirstpagedoneloop');

        minitemwrapped=towrap[0];
        maxitemwrapped=towrap[towrap.length-1];
          for (j = 0; j < towrap.length; j++) {

            wrapphrase= wrapphrase + "div[id=\"invoicehead\"], div[class=\"item-container-for-measure\"][rowid=\"" + towrap[j] + "\"], "
            }
        wrapphrase = wrapphrase.slice(0, -2); // remove comma from end (-2 cause there is an adding space)

        jQuery.globalEval( "$('" + wrapphrase + "').wrapAll('<div class=\"page\"> </div>');" );
        sumheight=0;
        towrap.length=0;
        wrapphrase="";
        headerinsert(minitemwrapped); // which item insertbefore
        footerinsert(maxitemwrapped, pagenumber);

    }
    function wrap(){
                            console.log('wraploop');

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

    $('span[name="htmlinsertbefore"][rowid="' + rowid + '"').html('<div id="frameheader"><div id="positionnumberlabel"><span >Pos.</span></div><div id="descriptionlabel"><span >Description</span></div><div id="unitlabel"><span >Unit</span></div><div id="quantitylabel"><span >Qty.</span></div><div id="unitpricelabel"><span >Unit Price</span></div><div id="netpricelabel"><span >Net Price</span></div><div id="vatpercentlabel"><span >VAT%</span></div><div id="vatvaluelabel"><span >VAT Value</span></div><div id="grosspricelabel"><span >Gross Price</span></div></div>');
    }
    function footerinsert(rowid, pagenumber){

    $('span[name="htmlinsertafter"][rowid="' + rowid + '"').html('<div class="middlepagesfooterdiv" ><hr><span class="middlepagesfooterspan1"><br></span><span pagenumber=\"' + pagenumber + '\" class="middlepagesfooterspan2">Description2</span><span class="middlepagesfooterspan3">Description3</span></div>');
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
//            $('#pages').text((pagenumber+1)); // pagenumbers on firstpage
//            $('span[class="firstpagefooterspan2"]').text( "page 1/" + (pagenumber+1)); // firstpage footer filling
//            $('span[class="firstpagefooterspan3"]').text( "Number of Invoice: " + $('#numberofcustomerinvoice').text()); // firstpage footer filling

            for (k = 1; k != (pagenumber+1); k++) { // for cycle for middlepage numbers
            $('span[class="middlepagesfooterspan2"][pagenumber="' + k + '"').text( "page " + k + "/" + (pagenumber));

            }
            $('span[class="middlepagesfooterspan3"]').text( "Number of Invoice: " + $('#numberofcustomerinvoice').text()); // middlepages number of customerinvoice filling

//            $('span[class="backpagefooterspan2"]').text( "page " + (pagenumber+1) + "/" + (pagenumber+1)); // backpage footer filling
//            $('span[class="backpagefooterspan3"]').text( "Number of Invoice: " + $('#numberofcustomerinvoice').text()); // backpage footer filling

    }
    $('#dispatchinvoicebutton').click(function() {
                var customerinvoiceid= $('#customerinvoiceid').text();
                var dateofinvoicevalue= $('#dateofinvoicevalue').text();
                var dateofcompletionvalue= $('#dateofcompletionvalue').text();
                var deadlineforpaymentvalue= $('#deadlineforpaymentvalue').text();
                var methodofpaymentvalue= $('#methodofpaymentvalue').text();
                var currencyvalue= $('#currencyvalue').text();
                var remarkstextarea= $('#remarkstextarea').text();
                var numberofordervalue= $('#numberofordervalue').text();
                var companynameandcontactname= $('#companyname').text() + "- " + $('#contactname').text();
                var pcd= $('#pcd').text();
                var town= $('#town').text();
                var address= $('#address').text();
                var itemnumber= $('#itemnumberp').attr( "itemnumber" );
                var description;
                var unit;
                var unitsalesprice;
                var itemdataliststringified;
                var itemdataliststringifiedescaped;
                var itemdatalist=[];



        main();

            function main(){


                for (i = 1; i <= itemnumber; i++) {
                    itemdatacollect(i);

                }
                itemdataliststringified = JSON.stringify(itemdatalist);

                datatransmit();

            }
            function itemdatacollect(i){
              description=$('.descriptiondiv[rowid="' + (i - 1) + '"]').text();
              unit=$('p[name="unit_tblDoc_details"][rowid="' + (i - 1) + '"]').text();
              unitsalesprice=$('p[name="unitsalesprice"][rowid="' + (i - 1) + '"]').text();
              vatpercent=$('p[name="vatpercentdiv"][rowid="' + (i - 1) + '"]').text();
              netprice=$('p[name="netpricediv"][rowid="' + (i - 1) + '"]').text();
              vatvalue=$('p[name="vatvaluediv"][rowid="' + (i - 1) + '"]').text();
              grossprice=$('p[name="grosspricediv"][rowid="' + (i - 1) + '"]').text();
              qty=$('p[name="qty"][rowid="' + (i - 1) + '"]').text();
              itemdatalist.push(description, unit, unitsalesprice, vatpercent, netprice, vatvalue, grossprice, qty);

            }

            function datatransmit(){
            itemdataliststringifiedescaped = itemdataliststringified.replace(/\\n/g, "\\n")
                                                                  .replace(/\\'/g, "\\'")
                                                                  .replace(/\\"/g, '\\"')
                                                                  .replace(/\\&/g, "\\&")
                                                                  .replace(/\\r/g, "\\r")
                                                                  .replace(/\\t/g, "\\t")
                                                                  .replace(/\\b/g, "\\b")
                                                                  .replace(/\\f/g, "\\f");
            console.log('itemdataliststringified: ' + itemdataliststringified);
            console.log('itemdataliststringifiedescaped: ' + itemdataliststringifiedescaped);

                $.ajax({
                    type: 'POST',
                    url: 'customerinvoicedispatch',

                    data: {
                    'customerinvoiceid' : customerinvoiceid,
                    'dateofinvoicevalue' : dateofinvoicevalue,
                    'dateofcompletionvalue' : dateofcompletionvalue,
                    'deadlineforpaymentvalue' : deadlineforpaymentvalue,
                    'methodofpaymentvalue' : methodofpaymentvalue,
                    'currencyvalue' : currencyvalue,
                    'remarkstextarea' : remarkstextarea,
                    'numberofordervalue' : numberofordervalue,
                    'companynameandcontactname' : companynameandcontactname,
                    'pcd' : pcd,
                    'town' : town,
                    'address' : address,
                    'itemnumber' : itemnumber,
                    'itemdatalist': itemdataliststringifiedescaped,

                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                    },

                    success: function(url){
                    window.location.href = url;

                    },
                    error: function(){
                        alert('failure');
                    },
                    datatype: 'html'

                });
            }

    });

});



