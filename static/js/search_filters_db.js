// Define the HiddenClass
class HiddenClass {
    constructor(selector) {
        this.selector = selector;
    }

    hideElements() {
        const elements = document.querySelectorAll(this.selector);
        elements.forEach(element => {
            element.style.display = 'none';
        });
    }

    showAllElements() {
        const elements = document.querySelectorAll(this.selector);
        elements.forEach(element => {
            element.style.display = '';
        });
    }
}

document.addEventListener("DOMContentLoaded", function() {
    // Create instances of HiddenClass for each filter
    const geographyHidden = new HiddenClass('.filters_geography .option_geography');
    const headcountHidden = new HiddenClass('.filters_headcount .option_headcount');
    const functionHidden = new HiddenClass('.filters_function .option_function');

    const geographyInput = document.querySelector(".search-bar_geography");
    const headcountInput = document.querySelector(".search-bar_headcount");
    const functionInput = document.querySelector(".search-bar_function");

    // Show all elements initially
    geographyHidden.showAllElements();
    headcountHidden.showAllElements();
    functionHidden.showAllElements();

    geographyInput.addEventListener("input", function() {
        applySearchFilter(geographyInput, geographyHidden);
    });

    headcountInput.addEventListener("input", function() {
        applySearchFilter(headcountInput, headcountHidden);
    });

    functionInput.addEventListener("input", function() {
        applySearchFilter(functionInput, functionHidden);
    });
});

// Function to apply search filter
function applySearchFilter(input, hiddenInstance) {
    const searchTerm = input.value.toLowerCase();

    hiddenInstance.showAllElements(); // Show all elements initially

    if (searchTerm.trim() !== "") {
        const matchingElements = document.querySelectorAll(`${hiddenInstance.selector}:not([hidden])`);
        matchingElements.forEach(element => {
            const optionText = element.textContent.toLowerCase();
            if (!optionText.includes(searchTerm)) {
                element.style.display = 'none';
            }
        });
    }
}

