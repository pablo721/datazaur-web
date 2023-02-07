
function changeTopNCoins(){

    let dropdown = document.getElementById('top_n_coins_dropdown');
    let top_n_coins = dropdown.selectedOptions[0].text;
    let url = 'http://127.0.0.1:8000/crypto/dominance/?top_n_coins=' + top_n_coins;
    window.open(url, '_self');
    };

