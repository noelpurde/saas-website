document.addEventListener("DOMContentLoaded", function() {
    const geographyInput = document.querySelector(".search-bar_geography");
    const headcountInput = document.querySelector(".search-bar_headcount");
    const functionInput = document.querySelector(".search-bar_function");

    const geographyOptions = document.querySelectorAll(".filters_geography .option_geography");
    const headcountOptions = document.querySelectorAll(".filters_headcount .option_headcount");
    const functionOptions = document.querySelectorAll(".filters_function .option_function");

    function applySearchFilter(input, options) {
        const searchTerm = input.value.toLowerCase();

        options.forEach(function(option) {
            const optionText = option.textContent.toLowerCase();
            if (optionText.includes(searchTerm)) {
                option.classList.remove("hidden");
            } else {
                option.classList.add("hidden");
            }
        });
    }

    geographyInput.addEventListener("input", function() {
        applySearchFilter(geographyInput, geographyOptions);
    });

    headcountInput.addEventListener("input", function() {
        applySearchFilter(headcountInput, headcountOptions);
    });

    functionInput.addEventListener("input", function() {
        applySearchFilter(functionInput, functionOptions);
    });
});
console.log("Hey");