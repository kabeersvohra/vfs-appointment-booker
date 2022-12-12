// Create an instance of the Stripe object with your publishable API key
var stripe = Stripe(
	'pk_test_51Ij84jEpmt8X7qxvCy2iNNTvfo5HFaP7r62WEycE6cbabSrIKKaOi9bZ8y4dzaROUVU4yspyLoMNrDs6uamPQpjW00PkhPpSnI'
);
var checkoutButton = document.getElementById('passport-renewal-button');

checkoutButton.addEventListener('click', function() {
	// Create a new Checkout Session using the server-side endpoint you
	// created in step 3.
	fetch('https://zv3xlrogmd.execute-api.eu-west-1.amazonaws.com/prod', {
		method: 'POST',
	})
	.then(function(response) {
		return response.json();
	})
	.then(function(session) {
		return stripe.redirectToCheckout({ sessionId: session.id });
	})
	.then(function(result) {
		// If `redirectToCheckout` fails due to a browser or network
		// error, you should display the localized error message to your
		// customer using `error.message`.
		if (result.error) {
			alert(result.error.message);
		}
	})
	.catch(function(error) {
		console.error('Error:', error);
	});
});
