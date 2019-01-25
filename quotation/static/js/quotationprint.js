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
var itemnumbers=$('#itemnumberp').attr( "itemnumber" );
itemnumbers--;
var towrap = [];
var i;
var wrapphrase="";
for (i = 0; i <= itemnumbers; i++) {

    height=$('div[class="item-container"][rowid="' + i + '"').outerHeight();
    sumheight=sumheight+height;

console.log(i + " " + height + " " + sumheight);

    if (sumheight > 600 || i == itemnumbers) {
                   if (i == itemnumbers) {towrap.push(i);} //last record to wrap we put to array
      //$('span[name="htmlinsert"][rowid="' + i + '"').html('<p>TEXTT</p>');
            for (j = 0; j < towrap.length; j++) {

            wrapphrase= wrapphrase + "div[class=\"item-container\"][rowid=\"" + towrap[j] + "\"], "
            }
        wrapphrase = wrapphrase.slice(0, -2); // remove comma from end (-2 cause there is an adding space)
        jQuery.globalEval( "$('" + wrapphrase + "').wrapAll('<div class=\"page\"> </div>');" );
        sumheight=0;
        towrap.length=0;
        wrapphrase="";
    }
    towrap.push(i);


    //if sumheight > 1400 then
    //    insert footer/break/header/page closing div/page opening div before this item
    // the page number = number of insert



 }



 //$('div[class="item-container"][rowid="' + 0 + '"], div[class="item-container"][rowid="' + 1 + '"]' ).wrapAll('<div class="page"> </div>');
              //div[class="item-container"][rowid="7"], div[class="item-container"][rowid="8"], div[class="item-container"][rowid="9"] //from console
 //    put page number to footer

});