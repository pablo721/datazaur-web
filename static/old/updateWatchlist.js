
//import Cookies from '/static/js.cookie.mjs'

var checked_symbols = Array();

function findChecked(){
    let checkboxes = document.getElementsByTagName("input");
    let checked = Array();
    for (item of checkboxes) {
        if (item.checked) {
        checked.push(item.id);
        };
    };
    console.log(checked);
    checked_ids = checked;
    $('#checked_symbols').val(checked_symbols);
};

function updateWatchlist(){
    let checked_ids = findChecked();
    console.log(document.cookie)
    let csrftoken = document.cookie.split('=')[1]
    $('#checked_symbols').val(checked_symbols);
    $.ajax({
        type: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        url: '../watchlist/',
        data: checked_symbols});
    console.log(checked_symbols);
    };


document.addEventListener('click', updateWatchlist);




