
$('#invert_fx').click(function(){
    let table = document.getElementById('fx_column');
    for (row of table.tBodies[0].rows){
        row.cells[1].innerHTML = Math.round((1000 / row.cells[1].innerHTML)) / 1000;
    }
})

