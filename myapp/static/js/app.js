const slides = document.querySelector('.slides');
const slide = document.querySelectorAll('.slide');

const nextBtn = document.querySelector('.next');
const prevBtn = document.querySelector('.prev');

let index = 0;
const totalSlides = slide.length;

/* UPDATE SLIDER */
function updateSlider(){
    slides.style.transform = `translateX(-${index * 100}%)`;
}

/* NEXT */
function nextSlide(){

    index++;

    if(index >= totalSlides){
    index = 0;
    }

    updateSlider();
}

/* PREVIOUS */
function prevSlide(){

    index--;

    if(index < 0){
    index = totalSlides - 1;
    }

    updateSlider();
}

/* BUTTON EVENTS */
nextBtn.addEventListener('click', nextSlide);
prevBtn.addEventListener('click', prevSlide);

/* AUTO SLIDE */
setInterval(nextSlide, 4000);