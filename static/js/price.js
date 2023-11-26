const priceSlider = document.getElementById('priceSlider');
const priceDisplay = document.getElementById('credits');
const companyOfferDisplay = document.getElementById('companyOffer');
const sliderBubble = document.getElementById('sliderBubble');
const sliderWrapper = document.querySelector('.slider-container');

const credits = [100, 1000, 2000, 4000, 8000, 16000, 32000, 64000];

priceSlider.addEventListener('input', updatePrice);

function updatePrice() {
    const index = priceSlider.value;
    const credit = credits[index];
    priceDisplay.textContent = `Credits: ${credit}`;
    priceDisplay.style.fontWeight = 'normal';
    priceDisplay.style.fontSize = '24px';

    companyOfferDisplay.style.fontFamily = 'Quicksand, sans-serif';
    companyOfferDisplay.style.color = '#25254e'; 


    if (credit == 100) {
        companyOfferDisplay.innerHTML = `<span id="creditAmount"><b>$${credit * 0.80}</span> <span id="otherAmount"><b>@ $.80 / credit</span>`;
        document.getElementById('creditAmount').style.fontSize = '28px';
        document.getElementById('otherAmount').style.color = '#9d9d9d';
    } else {
        companyOfferDisplay.innerHTML = `<span id="creditAmount"><b>$${credit * 0.80}</span> <span id="otherAmount"><b>@ $.80 / credit</span>`;
        document.getElementById('creditAmount').style.fontSize = '28px';
        document.getElementById('otherAmount').style.color = '#9d9d9d';
        }

    updateSliderBubble();
}

function updateSliderBubble() {
    const index = priceSlider.value;
    const thumbSize = 20;
    const position = (priceSlider.clientWidth - thumbSize) / (credits.length - 1) * index;

    sliderBubble.textContent = credits[index];
    sliderBubble.style.left = `calc(${position}px + ${thumbSize / 2}px)`;

    sliderBubble.style.display = 'block';
}

function showSliderBubble() {
    sliderBubble.style.opacity = 1;
}

function hideSliderBubble() {
    sliderBubble.style.opacity = 0;
}

sliderWrapper.addEventListener('mouseover', () => {
    showSliderBubble();
});

sliderWrapper.addEventListener('mouseout', () => {
    hideSliderBubble();
});

updatePrice();