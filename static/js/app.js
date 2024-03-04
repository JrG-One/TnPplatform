const swiper = new Swiper('.swiper', {
    // Optional parameters
    direction: 'horizontal',
    loop: true,
    slidesPerView: 1,

    // Navigation arrows
    navigation: {
        nextEl: '.next-btn',
        prevEl: '.prev-btn',
    },

    breakpoints: {
        800: {
            slidesPerView: 2,
            spaceBetween: 10,
        },
        1050: {
            slidesPerView: 3,
            spaceBetween: 15,
        },
        1350: {
            slidesPerView: 4,
            spaceBetween: 20,
        },
    },

});