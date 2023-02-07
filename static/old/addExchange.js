
var checkboxes = document.getElementsByClassName('star');

$(document).on('click', '.star', function(e){
//    e.preventDefault();
    $.ajax({
    type: 'POST',
    url: '/crypto/addExchange/',
    data: {
        exchange_id: this.value,
        value: this.checked ? 1 : 0,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    },
    success: function(data){
        alert(data);
    }
    });
});

