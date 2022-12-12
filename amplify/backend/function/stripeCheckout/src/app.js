const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY)

var express = require('express')
var bodyParser = require('body-parser')
var awsServerlessExpressMiddleware = require('aws-serverless-express/middleware')

// declare a new express app
var app = express()
app.use(bodyParser.json())
app.use(awsServerlessExpressMiddleware.eventContext())

// Enable CORS for all methods
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*")
  res.header("Access-Control-Allow-Headers", "*")
  next()
});


app.post('/checkout', async function(req, res) {
  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [
        {
          price: req.body.priceId,
          quantity: 1,
        },
      ],
      mode: 'payment',
      client_reference_id: req.body.client_reference_id,
      success_url: 'https://ihcappointments.uk/success?session_id={CHECKOUT_SESSION_ID}',
      cancel_url: 'https://ihcappointments.uk',
    })
    res.json(session)
  } catch (err) {
    res.json(err)
  }
})

app.listen(3000, function() {
    console.log("App started")
});

// Export the app object. When executing the application local this does nothing. However,
// to port it to AWS Lambda we will create a wrapper around that will load the app from
// this file
module.exports = app
