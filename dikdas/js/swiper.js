      $(document).ready(function () {
        var swiper = app.swiper.get(".swiper-container");
        var swiperMusic = app.swiper.get(".swiper-container-music");

        swiper.slideNext();

        swiper.on("slideChange", function () {
          var theslide = swiper.activeIndex; //this is working the first time I load the page, but not if I load the same page again, using stacked pages.
          if (theslide == 0) {
            $(".bg-header").css("background-color", "#e8a885");
            $(".header-title").text("WHERE THE CRAWDADS SING");
            $(".header-desc").text(
              "'Beautifully written at times, and with an interesting, plausible story. '"
            );
          } else if (theslide == 1) {
            $(".bg-header").css("background-color", "#e6e367");
            $(".header-title").text("My Thoughts Exactly");
            $(".header-desc").text("'An unflicing, unputdownable book'");
          } else if (theslide == 2) {
            $(".bg-header").css("background-color", "#82cdca");
            $(".header-title").text("Next Level Basic");
            $(".header-desc").text(
              "'Basic is not just a next level of this story'"
            );
          }
        });

        swiperMusic.on("slideChange", function () {
          var theslides = swiperMusic.activeIndex; //this is working the first time I load the page, but not if I load the same page again, using stacked pages.
          if (theslides == 0) {
            $(".bg-header-music").css("background-color", "#222222");
            $(".header-title-music").text("HONNE");
          } else if (theslides == 1) {
            $(".bg-header-music").css("background-color", "#ec3c62");
            $(".header-title-music").text("LANY");
          } else if (theslides == 2) {
            $(".bg-header-music").css("background-color", "#f2a0b7");
            $(".header-title-music").text("Taylor Swift");
          }
        });
      });