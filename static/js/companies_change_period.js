
$('#companies_market_data_period_select').change(function(){
    var period = $('#companies_market_data_period_select').val();
    var symbol2 = symbol;
    var url = '/companies/' + symbol2 + '/market_data?period=' + period;
    console.log(symbol2);

    window.location.replace(url);
})