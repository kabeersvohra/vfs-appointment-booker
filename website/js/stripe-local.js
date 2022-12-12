// import { API } from "aws-amplify"
// import { loadStripe } from "@stripe/stripe-js"

const stripePromise = Stripe(
	'pk_test_51Ij84jEpmt8X7qxvCy2iNNTvfo5HFaP7r62WEycE6cbabSrIKKaOi9bZ8y4dzaROUVU4yspyLoMNrDs6uamPQpjW00PkhPpSnI'
);

var checkoutButton = document.getElementById('passport-renewal-button');

checkoutButton.addEventListener('click', async function() {
	const fetchSession = async() => {
		const apiName = "stripeAPI"
		// const apiEndpoint = "/checkout"
		const apiEndpoint = "https://afykk8twq3.execute-api.eu-west-1.amazonaws.com/dev/checkout"
		const body = {
			client_reference_id: "UniqueString",
			line_items: [{
				priceId: "price_1IstJLEpmt8X7qxvs8lUvRKy",
				quantity: 1,
			}],
			mode: "payment",
		}
		// const session = await API.post(apiName, apiEndpoint, {body})
		const session = await $.post(apiEndpoint, body).promise()  
		return session
	}

	const session = await fetchSession()
	const sessionId = session.id
	const stripe = await stripePromise
	stripe.redirectToCheckout({sessionId})
});
