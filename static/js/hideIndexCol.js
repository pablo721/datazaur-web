
let tables = document.getElementsByTagName('table');

for (let table of tables){
    for (let row of table.rows){
        row.deleteCell(0);
    }
}