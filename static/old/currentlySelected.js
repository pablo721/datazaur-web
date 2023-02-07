


$('select').change(function(){
    let selectedValue = this.selectedOptions[0].value;
    if (this.id == 'change_currency_dropdown') {
        $('#selected_currency').val(selectedValue);
        console.log('currency');
        console.log(selectedValue);
        }
    else {
        $('#selected_coin').val(selectedValue);
        console.log('coin');
        console.log(selectedValue);
        };
    });






