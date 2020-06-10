/*
aorderprocessmidiordercheckout.js
*/

            var msg="Hello Javascript2";
                    console.log(msg);

$(function () {
                  var msg="Hello Javascript2";
                    console.log('aa: ' + msg);
                  var csrftoken = $('input[name=csrfmiddlewaretoken]').val();
                  var midifileid = $('input[name=midifileid]').val();
                  var emailtosend = $('input[name=emailtosend]').val();
                    console.log('csrftoken: ' + csrftoken);
                    console.log('midifileid in paypal javascript: ' + midifileid);

         paypal.Buttons({
            createOrder: function() {
                var formDataoncreateorder = new FormData();

                formDataoncreateorder.append("midifileid", midifileid);
                formDataoncreateorder.append("emailtosend", emailtosend);


              return fetch('aorderprocessmidiorderpaypalpayment/', {
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
                  // This function captures the funds from the transaction.
                    for (const property in data) {
                      console.log(`${property}: ${data[property]}`);
                    }

                  return actions.order.capture().then(function(details)
                        {
                                    // This function shows a transaction success message to your buyer.
                                    for (const property in details) {
                                      console.log(`${property}: ${details[property]}`);
                                    }

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
                            fetch('aorderprocessmidiorderthankyouredirecturl/',
                                    {
                                        method: 'post',
                                        headers:
                                        {
                                          'X-CSRFToken' : csrftoken,
                                        }
                                    })
//                            alert('Transaction completed by ' + details.payer.name.given_name);
                        });
            }
          }).render('#paypal-button-container');
          //This function displays Smart Payment Buttons on your web page.

});

