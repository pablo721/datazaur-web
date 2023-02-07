
console.log('yo crypto js');
$('#crypto_curr_select').change(
    function changeCurrencyCrypto(){

            console.log('changing curr js');
            let code = this.value;
            console.log(code);
            if (code){
                $.ajax({
                type: 'POST',
                url: '/crypto/change_currency/',
                data: {
                    currency_code: code,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                },
                success: function(){
                    window.location.reload(true);
                },
                error: function(){
                    console.log('change curr js error');
                }
            }
        )};
    }
);




