const priceSlider = document.getElementById('priceSlider');
        const priceDisplay = document.getElementById('credits');
        const companyOfferDisplay = document.getElementById('companyOffer');
        
        // Define your price values here
        const credits = [100, 1000, 2000, 4000, 8000, 16000, 32000, 64000];
        
        priceSlider.addEventListener('input', updatePrice);

        function updatePrice() {
            const index = priceSlider.value;
            const credit = credits[index];
            priceDisplay.textContent = `CREDITS: ${credit}`;
            priceDisplay.style.fontWeight = 'bold';
            priceDisplay.style.fontSize = '24px';

            
            // You can customize the company offer based on the price here
            if (credit == 100) {
                companyOfferDisplay.textContent = "$80 @ $.80 / credit";
                companyOfferDisplay.style.fontWeight = 'bold';
                companyOfferDisplay.style.fontSize = '16px';
            } else if (credit == 1000) {
                companyOfferDisplay.textContent = "$880 @ $.80 / credit";
            } else if (credit == 2000) {
                companyOfferDisplay.textContent = "$1,760 @ $.80 / credit";
            } else if (credit == 4000) {
                companyOfferDisplay.textContent = "$3,520 @ $.80 / credit";
            } else if (credit == 8000) {
                companyOfferDisplay.textContent = "$7,040 @ $.80 / credit";
            } else if (credit == 16000) {
                companyOfferDisplay.textContent = "$14,080 @ $.80 / credit";
            } else if (credit == 32000) {
                companyOfferDisplay.textContent = "$28,160 @ $.80 / credit";
            } else if (credit == 64000) {
                companyOfferDisplay.textContent = "$56,320 @ $.80 / credit";
            }
        }

        // Set the maximum value of the slider to the number of prices
        priceSlider.max = credits.length - 1;

        // Initial update
        updatePrice();