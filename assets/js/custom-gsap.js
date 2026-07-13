/***************************************************
==================== JS INDEX ======================
****************************************************
0. Custom Cursor Js
01. Smooth Scroll Js
02. char splitText Js
03. Ttile Animation js
04. button hover animation JS
05. Blog Panel Js
06. text-scale-anim
07. Work Panel Js
08. Sticky Js
09. Thumbnail Menu Js
10. Video Js
11. Counter Card Animation  J
12. Team Panel
13. team inner page Sticky Js
14. Branch Js
****************************************************/



function initCustomGsap($) {
	"use strict";

    // На тачі кастомний курсор безглуздий (миші немає), а коштує дорого:
    // 183 .cursor-small х 2 слухачі + GSAP-твін на кожен mousemove.
    // ScrollSmoother і SplitText теж вимикаємо - це головні пожирачі
    // головного потоку на мобільному.
    var IS_TOUCH = window.matchMedia('(pointer: coarse)').matches || window.innerWidth < 992;

    ////////////////////////////////////////////////////
    // 0. Custom Cursor Js
    var body = document.body;
    var cursor = document.querySelector('.cursor');
    var dot = document.querySelector('.dot');
    var cursorSmalls = IS_TOUCH ? [] : document.querySelectorAll('.cursor-small');
    var cursorBigs = IS_TOUCH ? [] : document.querySelectorAll('.cursor-big');
    if (!IS_TOUCH) {
    body.addEventListener('mousemove', function (event) {
        gsap.to(cursor, {
            x: event.x,
            y: event.y,
            duration: 2, 
            delay: 0.1,
            visibility: 'visible',
            ease: "expo.out",
        });
    });
    body.addEventListener('mousemove', function (event) {
        gsap.to(dot, {
            x: event.x,
            y: event.y,
            duration: 1.5,
            visibility: 'visible',
            ease: "expo.out",
        });
    });
    // Small Cursor
    cursorSmalls.forEach(cursorSmall => {
    cursorSmall.addEventListener('mouseenter', function () {
        gsap.to(dot, {
            scale: 6,
            backgroundColor: '#fff',
        });
        gsap.to(cursor, {
            visibility: 'hidden',
            opacity: 0
        });
    });
    cursorSmall.addEventListener('mouseleave', function () {
        gsap.to(dot, {
            scale: 1,
            backgroundColor: '#fff',
        });
        gsap.to(cursor, {
            visibility: 'visible',
            opacity: 1
        });
    });
    });
    // Big Cursor
    cursorBigs.forEach(cursorBig => {
    cursorBig.addEventListener('mouseenter', function () {
        gsap.to(dot, {
            scale: 12,
            backgroundColor: '#fff',
        });
        gsap.to(cursor, {
            visibility: 'hidden',
            opacity: 0
        });
    });
    cursorBig.addEventListener('mouseleave', function () {
        gsap.to(dot, {
            scale: 1,
            backgroundColor: '#fff',
        });
        gsap.to(cursor, {
            visibility: 'visible',
            opacity: 1
        });
    });
    });
    }   // !IS_TOUCH


    ////////////////////////////////////////////////////
    // 01. Smooth Scroll Js
	function smoothSctoll() {
		$('.smooth a').on('click', function (event) {
			var target = $(this.getAttribute('href'));
			if (target.length) {
				event.preventDefault();
				$('html, body').stop().animate({
					scrollTop: target.offset().top - 120
				}, 1500);
			}
		});
	}
	smoothSctoll();
	if($('#smooth-wrapper').length && $('#smooth-content').length){
		gsap.registerPlugin(ScrollTrigger, ScrollSmoother, TweenMax, ScrollToPlugin);

		gsap.config({
			nullTargetWarn: false,
		});

		// На мобільному ScrollSmoother не створюємо: він тримає весь контент
		// у трансформі й перераховує його щокадру. Нативний скрол там і швидший,
		// і плавніший. Увесь код, що звертається до смузера, має фолбек
		// (ScrollSmoother.get() поверне null -> window.scrollTo).
		// effects вимкнено: data-speed у розмітці немає жодного, тобто анімувати нічого.
		if (!IS_TOUCH) {
			ScrollSmoother.create({
				smooth: 2,
				effects: false,
				smoothTouch: 0,
				normalizeScroll: false,
				ignoreMobileResize: true,
			});
		}
	}


    ////////////////////////////////////////////////////
    // 02. char splitText Js
    if (!IS_TOUCH && $(".tw-char-animation").length > 0) {   // SplitText ріже заголовок на сотні span'ів
        let char_come = gsap.utils.toArray(".tw-char-animation");
        char_come.forEach(splitTextLine => {
            const tl = gsap.timeline({
                scrollTrigger: {
                    trigger: splitTextLine,
                    start: "top 90%",
                    end: "bottom 60%",
                    scrub: false,
                    markers: false,
                    toggleActions: "play none none none",
                },
            });
            const itemSplitted = new SplitText(splitTextLine, {
                type: "chars, words",
            });
            gsap.set(splitTextLine, {
                perspective: 300
            });
            itemSplitted.split({
                type: "chars, words"
            });
            tl.from(itemSplitted.chars, {
                duration: 1,
                delay: 0.5,
                x: 100,
                autoAlpha: 0,
                stagger: 0.05,
            });
        });
    }


    ////////////////////////////////////////////////////
    // 03. Ttile Animation js
    if ($(".tw-itm-title tw-itm-anim").length) {
        let staggerAmount = 0.03,
            translateXValue = 20,
            delayValue = 0.1,
            easeType = "power2.out",
            animatedTextElements = document.querySelectorAll(".tw-itm-title tw-itm-anim");

        animatedTextElements.forEach(element => {
            let animationSplitText = new SplitText(element, { type: "chars, words" });

            ScrollTrigger.create({
                trigger: element,
                start: "top 85%",
                onEnter: () => {
                    gsap.from(animationSplitText.chars, {
                        duration: 1,
                        delay: delayValue,
                        x: translateXValue,
                        autoAlpha: 0,
                        stagger: staggerAmount,
                        ease: easeType,
                    });
                },
            });
        });
    }
    if($('.tw-sub-tilte').length) {
      var agtsub = $(".tw-sub-tilte");

      if(agtsub.length == 0) return; gsap.registerPlugin(SplitText); agtsub.each(function(index, el) {

        el.split = new SplitText(el, {
          type: "lines,words,chars",
          linesClass: "split-line"
        });

        if( $(el).hasClass('tw-sub-anim') ){
          gsap.set(el.split.chars, {
            opacity: 0,
            x: "7",
          });
        }

        el.anim = gsap.to(el.split.chars, {
          scrollTrigger: {
            trigger: el,
            start: "top 90%",
            end: "top 60%",
            markers: false,
            scrub: 1,
          },

          x: "0",
          y: "0",
          opacity: 1,
          duration: .7,
          stagger: 0.2,
        });

      });
    }
    if(!IS_TOUCH && $('.tw-itm-title').length) {
		var txtheading = $(".tw-itm-title");

    if(txtheading.length == 0) return; gsap.registerPlugin(SplitText); txtheading.each(function(index, el) {

        el.split = new SplitText(el, {
          type: "lines,words,chars",
          linesClass: "split-line"
        });

        if( $(el).hasClass('tw-itm-anim') ){
          gsap.set(el.split.chars, {
            opacity: .3,
            x: "-7",
          });
        }
        el.anim = gsap.to(el.split.chars, {
          scrollTrigger: {
            trigger: el,
            start: "top 92%",
            end: "top 60%",
            markers: false,
            scrub: 1,
          },

          x: "0",
          y: "0",
          opacity: 1,
          duration: .7,
          stagger: 0.2,
        });

      });
    }



    ////////////////////////////////////////////////////
    // 04. button hover animation JS
	$(".tw-hover-btn").on("mouseenter", function (e) {
		var x = e.pageX - $(this).offset().left;
		var y = e.pageY - $(this).offset().top;
		$(this).find(".tw-hover-btn-circle-dot").css({
			top: y,
			left: x,
		});
	});
	$(".tw-hover-btn").on("mouseout", function (e) {
		var x = e.pageX - $(this).offset().left;
		var y = e.pageY - $(this).offset().top;
		$(this).find(".tw-hover-btn-circle-dot").css({
			top: y,
			left: x,
		});
	});
    $('.tw-hover-btn').on('mouseenter', function (e) {
        var x = e.pageX - $(this).offset().left;
        var y = e.pageY - $(this).offset().top;
        $(this).find('.tw-btn-circle-dot').css({
            top: y,
            left: x
        });
    });
    $('.tw-hover-btn').on('mouseout', function (e) {
        var x = e.pageX - $(this).offset().left;
        var y = e.pageY - $(this).offset().top;
        $(this).find('.tw-btn-circle-dot').css({
            top: y,
            left: x
        });
    });
    var hoverBtns = gsap.utils.toArray(".tw-hover-btn-wrapper");
    const hoverBtnItem = gsap.utils.toArray(".tw-hover-btn-item");
    hoverBtns.forEach((btn, i) => {
        $(btn).mousemove(function (e) {
            callParallax(e);
        });
        function callParallax(e) {
            parallaxIt(e, hoverBtnItem[i], 60);
        }
        function parallaxIt(e, target, movement) {
            var $this = $(btn);
            var relX = e.pageX - $this.offset().left;
            var relY = e.pageY - $this.offset().top;
            gsap.to(target, 1, {
                x: ((relX - $this.width() / 2) / $this.width()) * movement,
                y: ((relY - $this.height() / 2) / $this.height()) * movement,
                ease: Power2.easeOut,
            });
        }
        $(btn).mouseleave(function (e) {
            gsap.to(hoverBtnItem[i], 1, {
                x: 0,
                y: 0,
                ease: Power2.easeOut,
            });
        });
    });




    ////////////////////////////////////////////////////
    // 05. Blog Panel Js
    let pr = gsap.matchMedia();
    pr.add("(min-width: 1199px)", () => {
        let tl = gsap.timeline();
        let projectpanels = document.querySelectorAll('.blog-panel')
        projectpanels.forEach((section, index) => {
            tl.to(section, {
                scrollTrigger: {
                    trigger: section,
                    pin: section,
                    scrub: 1,
                    start: 'center center',
                    end: "bottom 60%",
                    endTrigger: '.blog-panel-area',
                    pinSpacing: false,
                    markers: false,
                },
            })
        })
    });

  
	// 06. text-scale-anim //
	// const headings = document.querySelectorAll('.text-scale-anim');
	// headings.forEach(heading => {
	// 	const textNodes = [];
	// 	heading.childNodes.forEach(node => {
	// 		if (node.nodeType === Node.TEXT_NODE) {
	// 			node.textContent.split(' ').forEach((word, index, array) => {
	// 				const wordSpan = document.createElement('span');
	// 				wordSpan.classList.add('tp-word-span');
	// 				word.split('').forEach(letter => {
	// 					const letterSpan = document.createElement('span');
	// 					letterSpan.classList.add('tp-letter-span');
	// 					letterSpan.textContent = letter;
	// 					wordSpan.appendChild(letterSpan);
	// 				});
	// 				textNodes.push(wordSpan);
	// 				if (index < array.length - 1) {
	// 					textNodes.push(document.createTextNode(' '));
	// 				}
	// 			});
	// 		} else if (node.nodeType === Node.ELEMENT_NODE) {
	// 			textNodes.push(node.cloneNode(true));
	// 		}
	// 	});
	// 	heading.innerHTML = '';
	// 	textNodes.forEach(node => heading.appendChild(node));
	// 	const letters = heading.querySelectorAll('.tp-letter-span');
	// 	letters.forEach(letter => {
	// 		letter.addEventListener('mouseenter', () => {
	// 			gsap.to(letter, {
	// 				scaleY: 1.3,
	// 				y: '10%',
	// 				duration: 0.2,
	// 				ease: 'sine'
	// 			});
	// 		});
	// 		letter.addEventListener('mouseleave', () => {
	// 			gsap.to(letter, {
	// 				scaleY: 1,
	// 				y: '0%',
	// 				duration: 0.2,
	// 				ease: 'sine'
	// 			});
	// 		});
	// 	});
	// });





    ////////////////////////////////////////////////////
    // 07. Work Panel Js
    let wk = gsap.matchMedia();
    wk.add("(min-width: 991px)", () => {
        let tl = gsap.timeline();
        let projectpanels = document.querySelectorAll('.work-two-panel')
        projectpanels.forEach((section, index) => {
            tl.to(section, {
                scrollTrigger: {
                    trigger: section,
                    pin: section,
                    scrub: 1,
                    start: 'center center',
                    end: "bottom 60%",
                    endTrigger: '.work-two-panel-area',
                    pinSpacing: false,
                    markers: false,
                },
            })
        })
    });




    ////////////////////////////////////////////////////
    // 08. Sticky Js
    gsap.utils.toArray('.sticky-item').forEach(sticky => {
        if (window.innerWidth < 0 || window.innerWidth > 992) {
            ScrollTrigger.create({
            trigger: sticky,
            start: 'top top+=180',
            end: '+=786',
            pin: true,
            scrub: true,
            });
        }
    });





    ////////////////////////////////////////////////////
    // 09. Thumbnail Menu Js
    if ($('.thumbnail-three-area').length > 0) {
        let mm = gsap.matchMedia();
        mm.add("(min-width: 1200px)", () => {
            let thumbnail = gsap.timeline({
                scrollTrigger: {
                    trigger: ".thumbnail-three-area",
                    start: "top 170",
                    pin: true,
                    markers: false,
                    scrub: 1,
                    pinSpacing: false,
                    end: "bottom 70%",
                }
            });
            thumbnail.to(".thumbnail-three-bg", {
                width: "1110px",
                height: "560px",
            });
        });
    }



	////////////////////////////////////////////////////
	// 10. Video Js
    gsap.registerPlugin(ScrollTrigger);
    if ($('.video-panel-area').length > 0) {
        let tl = gsap.timeline({
            scrollTrigger: {
                trigger: "#video",
                start: "top 60%",
                end: "top 20%",
                scrub: true,
            }
        });
        // TEXT hide first
        tl.to(".video-left-text", {
            x: -200,
            opacity: 0,
            ease: "none",
            duration: 0.4
        }, 0);
        tl.to(".video-right-text", {
            x: 200,
            opacity: 0,
            ease: "none",
            duration: 0.4
        }, 0);
        // IMAGE animation
        tl.fromTo("#video img", 
            {
                scale: 0.24,
                y: -334.66,
                borderRadius: '5rem'
            },
            {
                scale: 1,
                y: 0,
                borderRadius: '0rem',
                ease: "none",
                duration: 1
            },
            0.4
        );
        // PLAY BUTTON appear after image
        tl.fromTo(".video-play-button",
            {
                opacity: 0,
                y: -50
            },
            {
                opacity: 1,
                y: 0,
                ease: "power2.out",
                duration: 0.7
            },
            1.2
        );
    }





	////////////////////////////////////////////////////
	// 11. Counter Card Animation  Js
    gsap.registerPlugin(ScrollTrigger);
    document.addEventListener("DOMContentLoaded", function () {
      if (window.innerWidth > 768) {
        const items = document.querySelectorAll(".counter-ip-wrap .counter-ip-item");
        if (items.length < 5) return; // skip if items are missing
        const counter = gsap.timeline({
          scrollTrigger: {
            trigger: ".counter-ip-wrap",
            start: "top 50%",
            toggleActions: "play none none reverse",
            markers: false,
          },
          defaults: {
            ease: "ease1",
            duration: 1,
          },
        });

        counter
          .from(items[0], {
            xPercent: 100,
          })
          .from(items[1], {
            xPercent: 30,
          }, "<")
          .from(items[2], {
            xPercent: -30,
          }, "<")
          .from(items[3], {
            xPercent: -60,
          }, "<")
          .from(items[4], {
            xPercent: -100,
          }, "<");
      }
    });






    ////////////////////////////////////////////////////
    // 12. Team Panel
    let tn = gsap.matchMedia();
    tn.add("(min-width: 1199px)", () => {
        let tl = gsap.timeline();
        let projectpanels = document.querySelectorAll('.team-ip-panel')
        projectpanels.forEach((section, index) => {
            tl.to(section, {
                scrollTrigger: {
                    trigger: section,
                    pin: section,
                    scrub: 1,
                    start: 'center center',
                    end: "bottom 60%",
                    endTrigger: '.team-ip-panel-area',
                    pinSpacing: false,
                    markers: false,
                },
            })
        })
    });





    ////////////////////////////////////////////////////
    // 13. team inner page Sticky Js
    gsap.utils.toArray('.team-ip-sticky').forEach(sticky => {
        if (window.innerWidth < 0 || window.innerWidth > 992) {
            ScrollTrigger.create({
            trigger: sticky,
            start: 'top top+=260',
            end: '+=2062',
            pin: true,
            scrub: true,
            });
        }
    });



    ////////////////////////////////////////////////////
    // 14. Branch Js
    gsap.utils.toArray('.branch-left').forEach(sticky => {
        if (window.innerWidth < 0 || window.innerWidth > 992) {
            ScrollTrigger.create({
            trigger: sticky,
            start: 'top top+=260',
            end: '+=760',
            pin: true,
            scrub: true,
            });
        }
    });




	////////////////////////////////////////////////////
	// 15. Video Four Js
    gsap.registerPlugin(ScrollTrigger);
    if ($(".video-four-panel-area").length) {
        let mm = gsap.matchMedia();
        mm.add("(min-width:426px)", () => {
            let tl = gsap.timeline({
                scrollTrigger:{
                    trigger:"#video-four",
                    start:"top 60%",
                    end:"top 15%",
                    scrub:1
                }
            });
            // text
            tl.to(".video-four-left-text",{
                x:-250,
                opacity:0,
                duration: 0.4
            },0);
            tl.to(".video-four-right-text",{
                x:250,
                opacity:0,
                duration: 0.4
            },0);
            // image
            tl.to("#video-four img",{
                x:0,
                y:0,
                scale:1,
                borderRadius:0,
                ease:"none",
            },0);
        });
    }



	////////////////////////////////////////////////////
	// 11. Counter Card Animation  Js
    gsap.registerPlugin(ScrollTrigger);
    document.addEventListener("DOMContentLoaded", function () {
      if (window.innerWidth > 992) {
        const items = document.querySelectorAll(".counter-four-wrap .counter-four-item");
        if (items.length < 4) return; // skip if items are missing
        const counter = gsap.timeline({
          scrollTrigger: {
            trigger: ".counter-four-wrap",
            start: "top 50%",
            toggleActions: "play none none reverse",
            markers: false,
          },
          defaults: {
            ease: "ease1",
            duration: 1,
          },
        });
        counter
          .from(items[0], {
            xPercent: 80,
          })
          .from(items[1], {
            xPercent: 30,
          }, "<")
          .from(items[2], {
            xPercent: -30,
          }, "<")
          .from(items[3], {
            xPercent: -60,
          }, "<");
      }
    });





	////////////////////////////////////////////////////
	// 12. Integration Animation  Js
gsap.registerPlugin(ScrollTrigger);

document.addEventListener("DOMContentLoaded", () => {
    initCircle();
});

function initCircle() {
    const circle = document.querySelector(".integration-four-circle");

    // prevent error if element not exists
    if (!circle) return;

    const items = gsap.utils.toArray(
        ".integration-four-circle .integration-four-item"
    );

    if (!items.length) return;

    const total = items.length;
    const angleStep = (Math.PI * 2) / total;

    function layout() {

        // use getBoundingClientRect (more reliable)
        const size = circle.getBoundingClientRect().width;

        const centerX = size / 2;
        const centerY = size / 2;

        const radius = (size / 2) - 80;

        items.forEach((el, i) => {
            const angle = i * angleStep;

            const x =
                centerX +
                radius * Math.cos(angle) -
                el.offsetWidth / 2;

            const y =
                centerY +
                radius * Math.sin(angle) -
                el.offsetHeight / 2;

            gsap.set(el, {
                x,
                y
            });
        });
    }

    layout();

    gsap.to(circle, {
        rotation: 360,
        ease: "none",
        transformOrigin: "50% 50%",
        scrollTrigger: {
            trigger: ".integration-four-wrap",
            start: "top bottom",
            end: "bottom top",
            scrub: 1
        }
    });

    window.addEventListener("resize", layout);
}








    }

////////////////////////////////////////////////////
// Важку GSAP-ініціалізацію прибираємо з критичного шляху.
// Раніше вона виконувалась 4.6 с на мобільному і блокувала головний потік,
// поки браузер мав відмальовувати сторінку. Тепер чекаємо повного load,
// а далі - першу вільну мить (requestIdleCallback).
(function () {
    "use strict";
    function run() { initCustomGsap(jQuery); }
    function schedule() {
        if (window.requestIdleCallback) requestIdleCallback(run, { timeout: 2000 });
        else setTimeout(run, 1);
    }
    if (document.readyState === 'complete') schedule();
    else window.addEventListener('load', schedule, { once: true });
})();
