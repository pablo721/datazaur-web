
$('select').change(function(){
    let new_curr = this.selectedOptions[0].text;
    let url = 'http://127.0.0.1:8000/markets/forex/?currency=' + new_curr;
    window.open(url, '_self');
})


