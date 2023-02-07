
function sendCoinId() {
//    console.log(coin_id);
    let coin_id = this.srcElement['id'];
    console.log(coin_id);
    csrf = document.cookie.split('=')[1];
    console.log(csrf);
    $.post('#', {
    type: 'JSON',
    headers: {'X-CSRFToken': csrf},
    data: {id: coin_id},
    success: function() {alert('success')},
    error: function() {alert('error')},
    });
    };