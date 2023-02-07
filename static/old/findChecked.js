
var checked_symbols = Array();


function findChecked(){
    let checkboxes = document.getElementsByClassName("star");
    let checked = Array();
    for (item of checkboxes) {
        if (item.checked) {
        checked.push(item.id);
        };
    };
    console.log(checked);
    checked_symbols = checked;
    $('#checked_symbols').val(checked_symbols);
};