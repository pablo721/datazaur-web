

var amount = 0;

function addToPortfolio(){
	let amount = prompt('Please enter amount to add.');
	if (amount > 0){
		$('amount').val(amount);
		console.log('portf amount:');
		console.log(amount);
		}
	else{
		return
		};
	};
