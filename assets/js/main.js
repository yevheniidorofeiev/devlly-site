/***************************************************
==================== JS INDEX ======================
****************************************************

01. PreLoader Js
02.Header Sticky Js
03. Menu Controls JS
04. Sidebar Js
05. Search Bar Js
06. AOS Js
07. Backtotop Js
08. magnific Popup  Js
09. counter Js
10. Bg Image For Attribute  Js
11. Ripples  Js
12. Image Cliping Effect
13. Hover Reveal
14. Mouse Custom Cursor
15. About Images Hover Animation Js
16. Mouse active Js











****************************************************/



(function ($) {
	"use strict";


      ////////////////////////////////////////////////////
      // 01. PreLoader Js
      $(window).on('load', function () {
        var body = $('body');
        body.addClass('loaded');

        setTimeout(function () {
          body.removeClass('loaded');
        }, 1500);
      });
      document.addEventListener("DOMContentLoaded", () => {
        const svg = document.getElementById("svg");
        if (!svg) return;

        const tls = gsap.timeline();
        const curve = "M0 502S175 272 500 272s500 230 500 230V0H0Z";
        const flat = "M0 2S175 1 500 1s500 1 500 1V0H0Z";

        // Loader heading text
        if (document.querySelector(".loader-wrap-heading")) {
          tls.to(".loader-wrap-heading .load-text , .loader-wrap-heading .cont", {
            delay: 0.5,
            y: -100,
            opacity: 0,
          });
        }

        // SVG animation
        tls.to(svg, {
          duration: 0.5,
          attr: { d: curve },
          ease: "power2.in",
        }).to(svg, {
          duration: 0.5,
          attr: { d: flat },
          ease: "power2.out",
        });

        // Loader wrap
        if (document.querySelector(".loader-wrap")) {
        tls.to(".loader-wrap", { y: -1500 })
          .to(".loader-wrap", { zIndex: -1, display: "none" });
        }

        // Pre-header animation (safe check)
        const preHeader = document.querySelector(".pre-header");
        if (preHeader) {
        tls.from(preHeader, { y: 200 }, "-=1.5");

        const preHeaderCont = preHeader.querySelector(".containers");
          if (preHeaderCont) {
            tls.from(preHeaderCont, {
              y: 40,
              opacity: 0,
              delay: 0.1,
            }, "-=1.5");
          }
        }
      });


      ////////////////////////////////////////////////////
      // 02.Header Sticky Js
      // =========================  Start ==============
      $(window).on("scroll", function () {
        if ($(window).scrollTop() >= 260) {
          $(".header").addClass("fixed-header");
        } else {
          $(".header").removeClass("fixed-header");
        }
      });


      

      ////////////////////////////////////////////////////
      // 03. Menu Controls JS
      $('.tw-hamburger-toggle').on('click', function(){
        $('.tw-header-side-menu').slideToggle('tw-header-side-menu');
      });
      if($('.tw-main-menu-content').length && $('.tw-main-menu-mobile').length){
        let navContent = document.querySelector(".tw-main-menu-content").outerHTML;
        let mobileNavContainer = document.querySelector(".tw-main-menu-mobile");
        mobileNavContainer.innerHTML = navContent;
        let arrow = $(".tw-main-menu-mobile .has-dropdown > a");
        arrow.each(function () {
          let self = $(this);
          let arrowBtn = document.createElement("BUTTON");
          arrowBtn.classList.add("dropdown-toggle-btn");
          arrowBtn.innerHTML = "<i class='ph ph-caret-right'></i>";
          self.append(function () {
            return arrowBtn;
          });
          self.find("button").on("click", function (e) {
            e.preventDefault();
            let self = $(this);
            self.toggleClass("dropdown-opened");
            self.parent().toggleClass("expanded");
            self.parent().parent().addClass("dropdown-opened").siblings().removeClass("dropdown-opened");
            self.parent().parent().children(".tw-submenu").slideToggle();
          });
          });
      }




      ////////////////////////////////////////////////////
      // 04. Sidebar Js
      $(".tw-menu-bar").on("click", function () {
        $(".tpoffcanvas").addClass("opened");
        $(".body-overlay").addClass("apply");
      });
      $(".close-btn").on("click", function () {
        $(".tpoffcanvas").removeClass("opened");
        $(".body-overlay").removeClass("apply");
      });
      $(".body-overlay").on("click", function () {
        $(".tpoffcanvas").removeClass("opened");
        $(".body-overlay").removeClass("apply");
      });




      ////////////////////////////////////////////////////
      // 05. Search Bar Js
      $(".open-search").on("click", function () {
          $(".search_popup").addClass("search-opened");
          $(".search-popup-overlay").addClass("search-popup-overlay-open");
      });
      $(".search_close_btn").on("click", function () {
          $(".search_popup").removeClass("search-opened");
          $(".search-popup-overlay").removeClass("search-popup-overlay-open");
      });
      $(".search-popup-overlay").on("click", function () {
          $(".search_popup").removeClass("search-opened");
          $(this).removeClass("search-popup-overlay-open");
      });



      ////////////////////////////////////////////////////
      // 06. AOS Js
      AOS.init({
        once: false, // animation will happen every time you scroll
        offset: 0, // start animation when element enters the viewport
        anchorPlacement: "top-bottom", // when the bottom of the element hits the bottom of the screen
      });



      ////////////////////////////////////////////////////
      // 07. Backtotop Js
      function back_to_top() {
        var btn = $('#back_to_top');
        var btn_wrapper = $('.back-to-top-wrapper');
        $(window).on('scroll', function () {
          if ($(this).scrollTop() > 300) {
            btn_wrapper.addClass('back-to-top-btn-show');
          } else {
            btn_wrapper.removeClass('back-to-top-btn-show');
          }
        });
        btn.on('click', function (e) {
          e.preventDefault();
          $('html, body').animate({ scrollTop: 0 }, 300);
        });
      }
      back_to_top();






      
      ////////////////////////////////////////////////////
      // 09. counter Js
      new PureCounter();
      new PureCounter({
          filesizing: true,
          selector: ".filesizecount",
          pulse: 2,
      });


      ////////////////////////////////////////////////////
      // 10. Bg Image For Attribute  Js
      $(".bg-img").each(function () {
          var img = $(this).data("background-image");
          if (img) {
              $(this).css("background-image", "url('" + img + "')");
          }
      });
      $("[data-bg-color]").each(function () {
        $(this).css("background-color", $(this).attr("data-bg-color"));
      });



      ///////////////////////
      // 12. Image Cliping Effect
      document.addEventListener("DOMContentLoaded", () => {
        const initialClipPaths = [
          "polygon(0% 0%, 0% 0%, 0% 0%, 0% 0%)",
          "polygon(33.33% 0%, 33.33% 0%, 33.33% 0%, 33.33% 0%)",
          "polygon(65.66% 0%, 66.66% 0%, 66.66% 0%, 66.66% 0%)",
          "polygon(0% 33.33%, 0% 33.33%, 0% 33.33%, 0% 33.33%)",
          "polygon(33.33% 33.33%, 33.33% 33.33%, 33.33% 33.33%, 33.33% 33.33%)",
          "polygon(65.66% 33.33%, 66.66% 33.33%, 66.66% 33.33%, 66.66% 33.33%)",
          "polygon(0% 66.66%, 0% 66.66%, 0% 66.66%, 0% 66.66%)",
          "polygon(33.33% 66.66%, 33.33% 66.66%, 33.33% 66.66%, 33.33% 66.66%)",
          "polygon(65.66% 66.66%, 66.66% 66.66%, 66.66% 66.66%, 66.66% 66.66%)"
        ];
        const finalClipPaths = [
          "polygon(0% 0%, 34.33% 0%, 34.33% 34.33%, 0% 34.33%)",
          "polygon(32.33% 0%, 66.66% 0%, 66.66% 33.33%, 33.33% 34.33%)",
          "polygon(65.66% 0%, 100% 0%, 100% 33.33%, 65.66% 34.33%)",
          "polygon(0% 33.33%, 33.33% 33.33%, 33.33% 66.66%, 0% 66.66%)",
          "polygon(30.33% 33.33%, 66.66% 33.33%, 66.66% 66.66%, 33.33% 66.66%)",
          "polygon(65.66% 33.33%, 100% 32.33%, 100% 66.66%, 65.66% 66.66%)",
          "polygon(0% 65.66%, 33.33% 66.66%, 33.33% 100%, 0% 100%)",
          "polygon(30.33% 66.66%, 66.66% 65.66%, 66.66% 100%, 33.33% 100%)",
          "polygon(65.66% 66.66%, 100% 65.66%, 100% 100%, 65.66% 100%)"
        ];
        // Create mask divs for each wrapper
        document.querySelectorAll(".tw-clip-anim").forEach(wrapper => {
          const img = wrapper.querySelector(".tw-anim-img[data-animate='true']");
          if (!img) return;
          const url = img.src;
          // Remove old masks if any (reuse safe)
          wrapper.querySelectorAll(".mask").forEach(m => m.remove());
          for (let i = 0; i < 9; i++) {
            const mask = document.createElement("div");
            mask.className = `mask mask-${i + 1}`;
            Object.assign(mask.style, {
              backgroundImage: `url(${url})`,
              backgroundSize: "cover",
              backgroundPosition: "center",
              position: "absolute",
              inset: "0"
            });
            wrapper.appendChild(mask);
          }
        });
        // Animate masks
        gsap.utils.toArray(".tw-clip-anim").forEach(wrapper => {
          const masks = wrapper.querySelectorAll(".mask");
          if (!masks.length) return;
          gsap.set(masks, { clipPath: (i) => initialClipPaths[i] });
          const order = [
            [".mask-1"],
            [".mask-2", ".mask-4"],
            [".mask-3", ".mask-5", ".mask-7"],
            [".mask-6", ".mask-8"],
            [".mask-9"]
          ];
          const tl = gsap.timeline({
            scrollTrigger: { trigger: wrapper, start: "top 75%" }
          });
          order.forEach((targets, i) => {
            const validTargets = targets
              .map(c => wrapper.querySelector(c))
              .filter(el => el); // filter out nulls

            if (validTargets.length) {
              tl.to(validTargets, {
                clipPath: (j, el) => finalClipPaths[Array.from(masks).indexOf(el)],
                duration: 1,
                ease: "power4.out",
                stagger: 0.1
              }, i * 0.125);
            }
          });
        });
      })



      ///////////////////////
      // 13. Hover Reveal
        const hoverItem = document.querySelectorAll(".hover__reveal-item");
        function moveImage(e, hoverItem, index) {
            const item = hoverItem.getBoundingClientRect();
            const x = e.clientX - item.x;
            const y = e.clientY - item.y;
            if (hoverItem.children[index]) {
                hoverItem.children[index].style.transform = `translate(${x}px, ${y}px)`;
            }
        }
        hoverItem.forEach((item, i) => {
            item.addEventListener("mousemove", (e) => {
                setInterval(moveImage(e, item, 1), 50);
            });
        });




        // 14. Mouse Custom Cursor 
        function itCursor() {
          var myCursor = jQuery(".mouseCursor");
          if (myCursor.length) {
            if ($("body")) {
              const e = document.querySelector(".cursor-inner"),
                t = document.querySelector(".cursor-outer");
              let n,
                i = 0,
                o = !1;
              (window.onmousemove = function (s) {
                o ||
                  (t.style.transform =
                    "translate(" + s.clientX + "px, " + s.clientY + "px)"),
                  (e.style.transform =
                    "translate(" + s.clientX + "px, " + s.clientY + "px)"),
                  (n = s.clientY),
                  (i = s.clientX);
              }),
                $("body").on("mouseenter", "button, a, .cursor-pointer", function () {
                  e.classList.add("active"), t.classList.add("active");
                }),
                $("body").on("mouseleave", "button, a, .cursor-pointer", function () {
                  ($(this).is("a", "button") &&
                    $(this).closest(".cursor-pointer").length) ||
                    (e.classList.remove("active"),
                      t.classList.remove("active"));
                }),
                (e.style.visibility = "visible"),
                (t.style.visibility = "visible");
            }
          }
        }
        itCursor();
        $(".tw-cursor-point-area").on("mouseenter", function () {
          $(".mouseCursor").addClass("cursor-big");
        });

        $(".tw-cursor-point-area").on("mouseleave", function () {
          $(".mouseCursor").removeClass("cursor-big");
        });

      



      ////////////////////////////////////////////////////
      // 15. About Images Hover Animation Js
      $('.about-three-list-wrap .about-three-list-item').on("mouseenter", function () {
          $('#about-three-thumb').removeClass().addClass($(this).attr('rel'));
          $(this).addClass('active').siblings().removeClass('active');
      });




      ////////////////////////////////////////////////////
      // 16. Mouse active Js
      $(document).ready(function () {
          $(
          ".chooseus-two-item, .about-ip-three-wrap, .service-four-wrapper, .counter-four-item"
          ).on("mouseenter", function () {
          $(this).addClass("active").siblings().removeClass("active");
          });
          $(
          ".chooseus-two-item, .about-ip-three-wrap, .service-four-wrapper, .counter-four-item"
          ).on("mouseenter", function () {
          $(this).addClass("active");
          $(this)
              .parent()
              .siblings()
              .find(
              ".chooseus-two-item, .about-ip-three-wrap, .service-four-wrapper, .counter-four-item"
              )
              .removeClass("active");
          });
      });



      ////////////////////////////////////////////////////
      // 17. knob progess  Js
      if (typeof ($.fn.knob) != 'undefined') {
        $('.knob').each(function () {
        var $this = $(this),
        knobVal = $this.attr('data-rel');

        $this.knob({
        'draw': function () {
          $(this.i).val(this.cv + '%')
        }
        });

        $this.appear(function () {
        $({
          value: 0
        }).animate({
          value: knobVal
        }, {
          duration: 2000,
          easing: 'swing',
          step: function () {
          $this.val(Math.ceil(this.value)).trigger('change');
          }
        });
        }, {
        accX: 0,
        accY: -150,
        });
      });
    }
        
        

})(jQuery);
