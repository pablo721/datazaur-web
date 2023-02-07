

function changeTimeframe(){
    let dropdown = document.getElementById('trends_timeframes');
    let timeframe = dropdown.selectedOptions[0].text;
    let url = 'http://127.0.0.1:8000/crypto/trends/?timeframe=' + timeframe;
    window.open(url, '_self');
    };

