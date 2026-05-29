const hero_images = document.querySelector('.hero-images');
const hero_image = document.querySelectorAll('.hero-image');

const next_button = document.querySelector('.next');
const prev_button = document.querySelector('.prev');

let index = 0;
const total_images = hero_image.length;

/* UPDATE SLIDER */
function updateSlider(){
    hero_images.style.transform = `translateX(-${index * 100}%)`;
}

/* NEXT */
function nextSlide(){

    index++;

    if(index >= total_images){
    index = 0;
    }

    updateSlider();
}

/* PREVIOUS */
function prevSlide(){

    index--;

    if(index < 0){
    index = total_images - 1;
    }

    updateSlider();
}

/* BUTTON EVENTS */
next_button.addEventListener('click', nextSlide);
prev_button.addEventListener('click', prevSlide);

/* AUTO SLIDE */
setInterval(nextSlide, 4500);