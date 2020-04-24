$(document).on('submit', '.comment-input-block', function(event){
    event.preventDefault();
    // ВЫВОДИМ В КОНСОЛЬ ЛОГ ОТЧЕТА ПО ЗАПРОСУ
    console.log($(this).serialize());
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: $(this).serialize(),
        dataType: 'json',
        success: function(response) {
            // ПРИ УСПЕШНОЙ ОТПРАВКИ, ОБНОВЛЯЕМ ДАННЫЕ СТРАНИЦЫ
            $('.comment-section').html(response['forms']);
        },
        error: function(rs, e) {
            console.log(rs.responseText);
            // ВЫВОДИМ В КОНСОЛЬ ЛОГ ОТЧЕТА ПО ЗАПРОСУ
        },
    });
});
