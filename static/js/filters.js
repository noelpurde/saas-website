const filterList = document.querySelector(".filter-list");
const options = document.querySelector(".options_geography");
const searchInput = document.querySelector(".search-bar");
const includeButtons = document.querySelectorAll(".include");
const excludeButtons = document.querySelectorAll(".exclude");
const optionElements = document.querySelectorAll(".option_geography");

const selectedFilters = new Set();

function updateFilters() {
    filterList.innerHTML = "";
    selectedFilters.forEach((filter) => {
        const filterElement = document.createElement("div");
        filterElement.classList.add("filter");
        filterElement.textContent = filter;
        const removeButton = document.createElement("span");
        removeButton.classList.add("filter-remove");
        removeButton.textContent = "X";
        removeButton.addEventListener("click", () => {
            selectedFilters.delete(filter);
            updateFilters();
        });
        filterElement.appendChild(removeButton);
        filterList.appendChild(filterElement);
    });
}

function addFilter(option_geography) {
    if (!selectedFilters.has(option_geography)) {
        selectedFilters.add(option_geography);
        updateFilters();
        // Show the filter section when a filter is added
        filterSection.style.display = "block";
    }
}

includeButtons.forEach((includeButton, index) => {
    includeButton.addEventListener("click", () => {
        const optionText = optionElements[index].querySelector("span").textContent;
        addFilter(optionText);
    });
});

excludeButtons.forEach((excludeButton, index) => {
    excludeButton.addEventListener("click", () => {
        const optionText = optionElements[index].querySelector("span").textContent;
        selectedFilters.delete(optionText);
        updateFilters();
    });
});

searchInput.addEventListener("input", () => {
    // Your search functionality here
    // You can filter/search based on selected filters and the search input value
});
