document.addEventListener("DOMContentLoaded", function() {
    const geoInput = document.querySelector(".search-bar_geography");
    const headInput = document.querySelector(".search-bar_headcount");
    const funcInput = document.querySelector(".search-bar_function");

    const geoOptions = document.querySelectorAll(".filters_geography .option_geography");
    const headOptions = document.querySelectorAll(".filters_headcount .option_headcount");
    const funcOptions = document.querySelectorAll(".filters_function .option_function");

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

    geoInput.addEventListener("input", function() {
        applySearchFilter(geoInput, geoOptions);
    });

    headInput.addEventListener("input", function() {
        applySearchFilter(headInput, headOptions);
    });

    funcInput.addEventListener("input", function() {
        applySearchFilter(funcInput, funcOptions);
    });
});

console.log("Hello2");
