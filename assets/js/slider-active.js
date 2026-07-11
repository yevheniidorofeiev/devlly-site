/***************************************************
==================== JS INDEX ======================
****************************************************

01. marquee left slide Js
02. marquee right slide Js

Swiper sliders (.work-active, .testimonial-active, .testimonial-two-active)
were removed: none of those elements exist in the markup.

****************************************************/

(function ($) {
	"use strict";

	////////////////////////////////////////////////////
	// 01. marquee left slide Js
	if ($(".marquee_left").length) {
		$(".marquee_left").marquee({
			speed: 50,
			gap: 0,
			delayBeforeStart: 0,
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
			duplicated: true,
			pauseOnHover: true,
			startVisible: true,
			direction: "right",
			loop: -1,
		});
	}

})(jQuery);
