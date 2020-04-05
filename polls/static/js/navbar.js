// СКРИПТ ДЛЯ ВЫПАДАЮЩЕГО мЕнЮ ПУНКТА "ЕЩЕ"
function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(e) {
  if (!e.target.matches('.dropbtn')) {
  var myDropdown = document.getElementById("myDropdown");
    if (myDropdown.classList.contains('show')) {
      myDropdown.classList.remove('show');
    }
  }
}

// СКРИПТ ДЛЯ АДАПТИВНОГО ПУНКТА МЕНЮ
function myFunctionToggle(x) {
    x.classList.toggle("change");

    var y = document.getElementById("myLinks");
    if (y.style.display === "block") {
        y.style.display = "none";
    } else {
        y.style.display = "block";
    }
}

// СКРИПТ ДЛЯ ОТОБРАЖЕНИЕ НАВБАРА ПРИ СКРОЛЛИНГЕ
var scrollTop = $(window).scrollTop();
var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
    var currentScrollPos = window.pageYOffset;
    if (prevScrollpos > currentScrollPos) {
        document.getElementById("navbar").style.top = "0";
    }
    else {
        document.getElementById("navbar").style.top = "-70px";
    }
    prevScrollpos = currentScrollPos;
    if (scrollTop == currentScrollPos) {
        document.getElementById("navbar").style.top = "0";
    }
}
