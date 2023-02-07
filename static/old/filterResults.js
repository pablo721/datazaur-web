
var search_box = document.getElementById('search_box');

search_box.addEventListener('keyup', function(){
    let table = document.getElementsByTagName('table')[0];
    let tables = document.getElementsByTagName('table');


	let filtered_table = table;
	let text = this.value;
	console.log(text);
	for (table of tables){
        if (!text){
            for (row of table.rows){
                $(row).show();
            }
        }
         else {
            for (row of table.rows){
                if ($(row).parent().is('thead')){
                    continue;
                }
                else if (row.innerHTML.toLowerCase().includes(text.toLowerCase())){
                    $(row).show();
                    }
                else {
                    $(row).hide();
                    }
            }
         }
    }
});


