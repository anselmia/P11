/*!
 * Start Bootstrap - Creative v6.0.0 (https://startbootstrap.com/themes/creative)
 * Copyright 2013-2020 Start Bootstrap
 * Licensed under MIT (https://github.com/BlackrockDigital/startbootstrap-creative/blob/master/LICENSE)
 */
(function ($) {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 72)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  $(document).ready(function () {
    if ($("input[name='GoToProduct']").length > 0) {
      $('body, html').animate({
        scrollTop: $("#product").offset().top - 82
      }, 600);
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function () {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 75
  });

  // Collapse Navbar
  var navbarCollapse = function () {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-scrolled");
    } else {
      $("#mainNav").removeClass("navbar-scrolled");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

  // Magnific popup calls
  $('#portfolio').magnificPopup({
    delegate: 'a',
    type: 'image',
    tLoading: 'Loading image #%curr%...',
    mainClass: 'mfp-img-mobile',
    gallery: {
      enabled: true,
      navigateByImgClick: true,
      preload: [0, 1]
    },
    image: {
      tError: '<a href="%url%">The image #%curr%</a> could not be loaded.'
    }
  });


  $('select.family').on('change', function (e) {
    var optionSelected = $("option:selected", this);
    var valueSelected = this.value;
    var url = window.location.origin + "/favorites/" + parseInt(valueSelected) + '/'
    window.location.href = url;
  });

  $('select.favori').on('change', function (e) {
    var optionSelected = $("option:selected", this);
    var valueSelected = this.value.split("/");
    var id_favori = valueSelected[0]
    var id_family = valueSelected[1]
    $.get('/save_favorites/' + parseInt(id_favori) + '/' + parseInt(id_family) + '/')
  });


})(jQuery); // End of use strict

$('input[name="email"], input[name="username"]').keyup(function () {
  if ($(this).val()) {
    $("button[name='confirm_change']").removeAttr('disabled').removeClass("disabled");
  }
});

function PopupCentrer(page, largeur, hauteur, options) {
  // ouvre une fenetre sans barre d'etat, ni d'ascenceur
  w = open(page, "", "top=" + top + ",left=" + left + ",width=" + largeur + ",height=" + hauteur + "," + options);
  w.document.write("<title> Ajouter une famille de favoris</title>");
  w.document.write("<body> Bonjour " + document.forms["f_popup"].elements["nom"].value + "<br><br>");
  w.document.write("Ce popup n'est pas un fichier HTML, ");
  w.document.write("il est écrit directement par la fenêtre appelante");
  w.document.write("</body>");
  w.document.close();
  var top = (screen.height - hauteur) / 2;
  var left = (screen.width - largeur) / 2;
  window.open(page, "", "top=" + top + ",left=" + left + ",width=" + largeur + ",height=" + hauteur + "," + options);
}

function openAlert(largeur, hauteur) {
  var popup = document.getElementById('popup'),
    bouton = document.createElement('button'),
    bouton2 = document.createElement('button');;

  popup.innerHTML = "";

  popup.appendChild(document.createTextNode('Nom de la famille à ajouter :'));
  popup.appendChild(document.createElement('br'));
  var input = document.createElement("input");
  input.type = "text";
  popup.appendChild(input);
  $('input[type="text"]').addClass("name");
  popup.appendChild(document.createElement('br'));
  popup.appendChild(bouton);
  bouton.appendChild(document.createTextNode('Valider'));
  popup.style.display = "";
  popup.appendChild(document.createElement('br'));
  popup.appendChild(bouton2);
  bouton2.appendChild(document.createTextNode('Annuler'));

  popup.style.left = (screen.height - hauteur) / 2;
  popup.style.top = (screen.width - largeur) / 2;

  $(function () {
    $('.name').keypress(function (e) {
      var keyCode = e.which;
      if (((keyCode >= 48 && keyCode <= 57) ||
          (keyCode >= 65 && keyCode <= 90) ||
          (keyCode >= 97 && keyCode <= 122)) &&
        keyCode != 8 && keyCode != 32) {} else {
        return false;
      }
    });
  });

  bouton.onclick = function () {
    popup.style.display = "none";
    var family = input.value
    var url = window.location.origin + "/save_family/" + family + '/'
    window.location.href = url;
  };
  bouton2.onclick = function () {
    popup.style.display = "none";
  };
}