function showHide(element_id) {
    //Если элемент с id-шником element_id существует
    if (document.getElementById(element_id)) {
        //Записываем ссылку на элемент в переменную obj
        var obj = document.getElementById(element_id);
        //Если css-свойство display не block, то:
        if (obj.style.display != "flex") {
            obj.style.display = "flex"; //Показываем элемент
        }
        else obj.style.display = "none"; //Скрываем элемент
    }
}

$('.nav1').on('click', 'a', function(){
  let wy = $(window).height() / 2,
      id = $(this).attr('href'),
      ey = $(id).offset().top,
      eh = $(id).outerHeight() / 2,
      top = ey - (wy - eh);

  top = top < 0 ? 0 : top;

  $('body,html').animate({
    scrollTop: top
  }, 1500);
  return false;
});
