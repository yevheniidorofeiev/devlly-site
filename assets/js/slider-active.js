/***************************************************
==================== JS INDEX ======================
****************************************************

01. marquee left slide Js


****************************************************/



(function ($) {
	"use strict";

    


    ////////////////////////////////////////////////////
    // 01. Work Js
	var slider = new Swiper('.work-active', {
		slidesPerView: 'auto',
		spaceBetween: 120,
		speed: 700,
		loop: true,
		centeredSlides: true,
		breakpoints: {
			1200: {
				 slidesPerView: 1.8,
				 spaceBetween: 80,
				},
			992: {
				 slidesPerView: 1.5,
				 spaceBetween: 60, 
				},
			768: {
				 slidesPerView: 1.2, 
				 spaceBetween: 60, 
				},
			576: {
				  slidesPerView: 1.1,
				},
			425: {
				  slidesPerView: 1.1,
				},
			375: {
				  slidesPerView: 1.1,
				},
			0: { 
				slidesPerView: 1 
			},
		},
		on: {
			init: function () {
				rotateSlides(this);
			},
			slideChangeTransitionStart: function () {
				rotateSlides(this);
			}
		}
	});
	function rotateSlides(swiper) {
		swiper.slides.forEach((slide) => {
			slide.style.transform = 'rotate(0deg) scale(0.9)';
			slide.style.transition = '0.5s';
		});
		let activeIndex = swiper.activeIndex;
		let prev = swiper.slides[activeIndex - 1];
		let next = swiper.slides[activeIndex + 1];
		let active = swiper.slides[activeIndex];
		if (active) {
			active.style.transform = 'rotate(0deg) scale(1)';
			active.style.zIndex = 3;
		}
		if (prev) {
			prev.style.transform = 'rotate(-20deg) scale(0.9)';
			prev.style.zIndex = 2;
		}
		if (next) {
			next.style.transform = 'rotate(20deg) scale(0.9)';
			next.style.zIndex = 2;
		}
	}




	////////////////////////////////////////////////////
	// 01. Home Four Project Js
	var slider = new Swiper('.testimonial-active', {
		slidesPerView: 2,
		spaceBetween: 30,
		loop: true,
		breakpoints: {
			'1600': {
				slidesPerView: 2,
			},
			'1400': {
				slidesPerView: 2,
			},
			'1200': {
				slidesPerView: 2,
			},
			'992': {
				slidesPerView: 1,
			},
			'768': {
				slidesPerView: 1,
			},
			'576': {
				slidesPerView: 1,
			},
			'0': {
				slidesPerView: 1,
			},
		},
		// Navigation arrows
		navigation: {
			nextEl: '.slider-next',
			prevEl: '.slider-prev',
		},
	});



	////////////////////////////////////////////////////
	// 01. marquee left slide Js
    if ($(".marquee_left").length) {
      $(".marquee_left").marquee({
        speed: 50,
        gap: 0,
        delayBeforeStart: 0,
        direction: $("html").attr("dir") === "rtl" ? "right" : "left",
        duplicated: true,
        pauseOnHover: true,
        startVisible: true,
        direction: "left",
        loop: -1,
      });
    }


    ////////////////////////////////////////////////////
	// 02. marquee right slide Js
    if ($(".marquee_right").length) {
      $(".marquee_right").marquee({
        speed: 50,
        gap: 0,
        delayBeforeStart: 0,
        direction: $("html").attr("dir") === "rtl" ? "right" : "left",
        duplicated: true,
        pauseOnHover: true,
        startVisible: true,
        direction: "right",
        loop: -1,
      });
    }






	////////////////////////////////////////////////////
	// 10. Home Two Testimonial  Js
	var slider = new Swiper('.testimonial-two-active', {
		slidesPerView: 3,
		spaceBetween: 30,
		loop: true,
		breakpoints: {
			'1600': {
				slidesPerView: 3,
			},
			'1400': {
				slidesPerView: 3,
			},
			'1200': {
				slidesPerView: 3,
			},
			'992': {
				slidesPerView: 2,
			},
			'768': {
				slidesPerView: 1,
			},
			'576': {
				slidesPerView: 1,
			},
			'0': {
				slidesPerView: 1,
			},
		},
        pagination: {
			el: ".testimonial-two-dot",
			clickable: true,
			renderBullet: function (index, className) {
			  return '<span class="' + className + '">' + '<button>'+(index + 1)+'</button>' + "</span>";
			},
		},
	});



	














})(jQuery);
