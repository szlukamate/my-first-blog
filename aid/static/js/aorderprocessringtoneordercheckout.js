/*
aorderprocessringtoneordercheckout.js
*/

            var msg="Hello Javascript2";
                    console.log(msg);

$(function () {
                  var msg="Hello Javascript2";
                    console.log('aa: ' + msg);
                  var csrftoken = $('input[name=csrfmiddlewaretoken]').val();
                  var ringtonemasterfileid = $('input[name=ringtonemasterfileid]').val();
                  var emailtosend = $('input[name=emailtosend]').val();
                    console.log('csrftoken: ' + csrftoken);
                    //console.log('ringtonemasterfileid in paypal javascript: ' + ringtonemasterfileid);

// Dialog "Sending email..." begin
    $( "#dialog-message" ).dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        Ok: function() {
          $( this ).dialog( "close" );
        }
      }
    });

                $( "#dialog-message" ).dialog("option", "buttons", {}); //remove OK button
// Dialog "Sending email..." end


         paypal.Buttons({
            createOrder: function() {
                var formDataoncreateorder = new FormData();

                formDataoncreateorder.append("ringtonemasterfileid", ringtonemasterfileid);
                formDataoncreateorder.append("emailtosend", emailtosend);


              return fetch('aorderprocessringtoneorderpaypalpayment/', {
                method: 'post',
                headers: {
                  'X-CSRFToken' : csrftoken
                },
                body: formDataoncreateorder,

              }).then(function(res) {
                return res.json();
              }).then(function(res) {
                console.log('res: ' + res);

                return res; // Use the same key name for order ID on the client and server
              });
            },
            onApprove: function(data, actions) {
                   $( "#dialog-message" ).dialog( "open" );

                  // This function captures the funds from the transaction.
                    for (const property in data) {
                      console.log(`${property}: ${data[property]}`);
                    }

                  return actions.order.capture().then(function(details)
                        {
                                    // This function shows a transaction success message to your buyer.
//                                    for (const property in details) {
//                                      console.log(`${property}: ${details[property]}`);
//                                    }
/*
                                var formDataonapprove = new FormData();

                                formDataonapprove.append("ectoken", details.id);

                            fetch('aorderprocessmidiorderpaymentcheck/',
                                    {
                                        method: 'post',
                                        headers:
                                        {
                                          'X-CSRFToken' : csrftoken,
                                        },
                                        body: formDataonapprove,
                                    })
                                    .then(data => console.log(data)); //log the data;
*/

                                    $.ajax({
                                        type: 'POST',
                                        url: 'aorderprocessringtoneorderpaymentcheck/',

                                        data: {
                                        'ectoken' : details.id,
                                        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                                        },
                                        success: function(url){
                                        console.log(url);

                                        window.location.href = url;

                                        },
                                        error: function(){
                                            alert('failure');
                                        },
                                        datatype: 'html'
                                    });


//                            alert('Transaction completed by ' + details.payer.name.given_name);
                        });
            }
          }).render('#paypal-button-container');
          //This function displays Smart Payment Buttons on your web page.

});

