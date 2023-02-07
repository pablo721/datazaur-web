
$(document).ready(function(){
    let table = document.getElementsByTagName('table')[0];
    for (row of table.tBodies[0].rows){
        let checkbox = document.createElement('input');
        checkbox.setAttribute('id', row.cells[1].innerText);
        checkbox.setAttribute('type', 'checkbox');
        checkbox.setAttribute('class', 'star');
        checkbox.setAttribute('style', 'position:relative; top:-2px; left:-8px');
        let cell = row.cells[5];
        cell.appendChild(checkbox);
        };
    });


