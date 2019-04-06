/*
quotation.js
*/

            var msg="Hello Javascript2";
                    console.log(msg);

$(window).on("load", function(){

});

$(function () {



                var title_tblcontacts_ctbldoc= $('#title_tblcontacts_ctbldoc').text();
                var lastname_tblcontacts_ctbldoc= $('#lastname_tblcontacts_ctbldoc').text();


                $("#emailbodytext").html(function () {
                    return $(this).html().replace("data1", "Dear " + title_tblcontacts_ctbldoc + " " + lastname_tblcontacts_ctbldoc + ",");
                });


sessionStorage.lastname = "Smith2";
// Retrieve
 console.log(sessionStorage.lastname)
});



