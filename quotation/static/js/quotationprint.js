/*
quotation.js
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
main();




    function main(){
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
            return;
            }
            towrap.push(i); //if there is room on page only goes to wrap array

        }

    }
    function totalprint(){
         $('span[name="totalhtmlinsertspan"][rowid="' + itemnumbers + '"').html('<div >totalprobe</div>');
    }
    function totalcount(i){
        var val=$('p[name="salesprice_tblDoc_details"][rowid="' + i + '"').text();
        total=total + Number(val);
        console.log(total);

    }

    function wrap(){
        pagenumber++;
        minitemwrapped=towrap[0];
        maxitemwrapped=towrap[towrap.length-1];
          for (j = 0; j < towrap.length; j++) {

            wrapphrase= wrapphrase + "div[class=\"item-container-for-measure\"][rowid=\"" + towrap[j] + "\"], " //"div[class=\"item-container-withhtmlinserts\"][rowid=\"" + towrap[j] + "\"], " //span[name=\"htmlinsertbefore\"][rowid=\"" + towrap[j] + "\"], div[class=\"item-container\"][rowid=\"" + towrap[j] + "\"], span[name=\"htmlinsertafter\"][rowid=\"" + towrap[j] + "\"], " //span[name=\"totalhtmlinsert\"][rowid=\"" + towrap[j] + "\"], "
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
    $('span[name="htmlinsertbefore"][rowid="' + rowid + '"').html('<div class="header" ><div class="headerlabels" ><span style="margin-left: 40mm" >Description</span><span style="margin-left: 60mm" >Qty</span></div></div>');
    }
    function footerinsert(rowid, pagenumber){
    $('span[name="htmlinsertafter"][rowid="' + rowid + '"').html('<div class="footerdiv" ><hr><span class="footerspan1">Please see the conditions in details on the last page<br></span><span pagenumber=\"' + pagenumber + '\" class="footerspan1">Description2</span></div>');
    }
    function measureitemcontainer(){
    height=$('div[class="item-container-for-measure"][rowid="' + i + '"').outerHeight();
    sumheight=sumheight+height;
    }
    function itemnumbers(){
    itemnumbers=$('#itemnumberp').attr( "itemnumber" ); //number of products
    itemnumbers--;
    }
    function pagenumberer(){
            for (k = 1; k != pagenumber+1; k++) {
            $('span[class="footerspan1"][pagenumber="' + k + '"').text( "page " + k + "/" + pagenumber);


            }

    }
});