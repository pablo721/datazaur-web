
document.getElementById('info_change').onchange(function(){
    let info_type = this.selectedOptions[0];
    let table = document.getElementById('fund_baseinfo').children[0];
    let base_table = "{{ info |safe }}";
    let esg_table = "{{ esg |safe }}";
    if (info_type == 'base'){
        table = base_table;
    }
    else if (info_type == 'esg'){
        table = esg_table;
    }
});


