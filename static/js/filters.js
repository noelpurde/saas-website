///////////////////////////////////// - MAP - ///////////////////////////////////////////////
// Get all path elements within the SVG
const paths = document.querySelectorAll("path");

// Function to change CSS variables based on class
function updateCSSVariables(className) {
  const root = document.documentElement; // Get the root HTML element

  switch (className) {
    case 'europe':
      root.style.setProperty('--europe_stroke', 'rgb(156, 62, 189)');
      root.style.setProperty('--europe_width', '4');
      root.style.setProperty('--europe_fill', 'rgb(230, 218, 239)');
      break;
    case 'northAmerica':
      root.style.setProperty('--northAmerica_stroke', 'rgb(156, 62, 189)');
      root.style.setProperty('--northAmerica_width', '4');
      root.style.setProperty('--northAmerica_fill', 'rgb(230, 218, 239)');
      break;
    case 'southAmerica':
      root.style.setProperty('--southAmerica_stroke', 'rgb(156, 62, 189)');
      root.style.setProperty('--southAmerica_width', '4');
      root.style.setProperty('--southAmerica_fill', 'rgb(230, 218, 239)');
      break;
    case 'asia':
      root.style.setProperty('--asia_stroke', 'rgb(156, 62, 189)');
      root.style.setProperty('--asia_width', '4');
      root.style.setProperty('--asia_fill', 'rgb(230, 218, 239)');
      break;
    case 'africa':
      root.style.setProperty('--africa_stroke', 'rgb(156, 62, 189)');
      root.style.setProperty('--africa_width', '4');
      root.style.setProperty('--africa_fill', 'rgb(230, 218, 239)');
      break;
    case 'oceania':
      root.style.setProperty('--oceania_stroke', 'rgb(156, 62, 189)');
      root.style.setProperty('--oceania_width', '4');
      root.style.setProperty('--oceania_fill', 'white');
      break;
    default:
      // Reset the CSS variables for other classes or when no class is found
      root.style.setProperty('--stroke', 'black');
      root.style.setProperty('--width', '1');
      root.style.setProperty('--fill', 'white');
      break;
  }
}

// Function to reset CSS variables based on class
function resetCSSVariables(className) {
  const root = document.documentElement; // Get the root HTML element

  switch (className) {
    case 'europe':
    case 'northAmerica':
    case 'southAmerica':
    case 'asia':
    case 'africa':
    case 'oceania':
      // Reset the CSS variables for the specific classes
      root.style.removeProperty('--europe_stroke');
      root.style.removeProperty('--northAmerica_stroke');
      root.style.removeProperty('--southAmerica_stroke');
      root.style.removeProperty('--asia_stroke');
      root.style.removeProperty('--africa_stroke');
      root.style.removeProperty('--oceania_stroke');

      root.style.removeProperty('--europe_width');
      root.style.removeProperty('--northAmerica_width');
      root.style.removeProperty('--southAmerica_width');
      root.style.removeProperty('--asia_width');
      root.style.removeProperty('--africa_width');
      root.style.removeProperty('--oceania_width');

      root.style.removeProperty('--europe_fill');
      root.style.removeProperty('--northAmerica_fill');
      root.style.removeProperty('--southAmerica_fill');
      root.style.removeProperty('--asia_fill');
      root.style.removeProperty('--africa_fill');
      root.style.removeProperty('--oceania_fill');
      break;
    default:
      // Reset the CSS variables for other classes or when no class is found
      root.style.setProperty('--stroke', 'black');
      root.style.setProperty('--width', '1');
      break;
  }
}
// Add mouseenter and mouseleave event listeners to each path
for (let i = 0; i < paths.length; i++) {
  const path = paths[i];
  let className;

  path.addEventListener('mouseenter', () => {
    // Get the class name of the hovered path
    className = path.getAttribute('class');

    // Update CSS variables based on class
    updateCSSVariables(className);
  });

  path.addEventListener('mouseleave', () => {
    // Reset CSS variables using the stored class name
    resetCSSVariables(className);
  });
}

        // Function to handle path click event
        function getPathClassName(event) {
          const path = event.target;
          const h1Element = document.getElementById("test");
          if (path.tagName === "path") {
              const className = path.getAttribute("class");
              h1Element.textContent=className;
          }
      }

      // Attach click event listener to all SVG paths
      const svgPaths = document.querySelectorAll("svg path");
      svgPaths.forEach(path => {
          path.addEventListener("click", getPathClassName);
      });

///////////////////////////////////// - MAP INTERACTION WITH FILTERS - ///////////////////////////////////////////////

// Function to handle path click event
function getPathClassName(event) {
  const path = event.target;
  if (path.tagName === "path") {
    const className = path.getAttribute("class");
    let continentName = className

    // Check if the class name matches one of the continents
    switch (continentName) {
      case "europe":
        addFilter_geography("Europe")
        removeContinent("Europe")
        break;
      case "asia":
        addFilter_geography("Asia")
        removeContinent("Asia")
        break;
      case "northAmerica":
        addFilter_geography("North America")
        removeContinent("North America")
        break;
      case "southAmerica":
        addFilter_geography("South America")
        removeContinent("South America")
        break;
      case "africa":
        addFilter_geography("Africa")
        removeContinent("Africa")
        break;
      case "oceania":
        addFilter_geography("Oceania")
        removeContinent("Oceania")
        break;
      default:
  
        break;
    }
  }
}

// Add event listeners to SVG paths with continent classes
document.querySelectorAll("path").forEach((path) => {
  path.addEventListener("click", getPathClassName);
}); 

///////////////////////////////////// - FILTERS G E O G R A P H Y - ///////////////////////////////////////////////
  
const filterList_geography = document.querySelector(".filter-list_geography");
const options_geography = document.querySelector(".options_geography_geography");
const searchInput_geography = document.querySelector(".search-bar_geography");
const includeButtons_geography = document.querySelectorAll(".include_geography");
const excludeButtons_geography = document.querySelectorAll(".exclude_geography");
const optionElements_geography = document.querySelectorAll(".option_geography");

const selectedFilters_geography = new Set();

function updateFilters_geography() {
    filterList_geography.innerHTML = "";
    selectedFilters_geography.forEach((filter_geography) => {
        const filterElement_geography = document.createElement("div");
        filterElement_geography.classList.add("filter_geography");
        filterElement_geography.textContent = filter_geography;
        const removeButton_geography = document.createElement("span");
        removeButton_geography.classList.add("filter-remove_geography");
        removeButton_geography.textContent = "X";
        removeButton_geography.addEventListener("click", () => {
            selectedFilters_geography.delete(filter_geography);
            updateFilters_geography();
        });
        filterElement_geography.appendChild(removeButton_geography);
        filterList_geography.appendChild(filterElement_geography);
    });
}

function addFilter_geography(option_geography) {
    if (!selectedFilters_geography.has(option_geography)) {
        selectedFilters_geography.add(option_geography);
        updateFilters_geography();
        // Show the filter section when a filter is added
        filterSection.style.display = "block";
    }
}

includeButtons_geography.forEach((includeButton, index) => {
    includeButton.addEventListener("click", () => {
        const optionText = optionElements_geography[index].querySelector("span").textContent;
        addFilter_geography(optionText);
    });
});

excludeButtons_geography.forEach((excludeButton, index) => {
    excludeButton.addEventListener("click", () => {
        const optionText = optionElements_geography[index].querySelector("span").textContent;
        selectedFilters_geography.delete(optionText);
        updateFilters_geography();
    });
});

searchInput_geography.addEventListener("input", () => {
    // Your search functionality here
    // You can filter/search based on selected filters and the search input value
});

//Map check to remove existent filters
function removeContinent(classname) {
  if(selectedFilters_geography.has(classname)){
    selectedFilters_geography.delete(classname);
    updateFilters_geography();
  }
}
  
///////////////////////////////////// - FILTERS H E A D C O U N T - ///////////////////////////////////////////////

const filterList_headcount = document.querySelector(".filter-list_headcount");
const options_headcount = document.querySelector(".options_headcount_headcount");
const searchInput_headcount = document.querySelector(".search-bar_headcount");
const includeButtons_headcount = document.querySelectorAll(".include_headcount");
const excludeButtons_headcount = document.querySelectorAll(".exclude_headcount");
const optionElements_headcount = document.querySelectorAll(".option_headcount");

const selectedFilters_headcount = new Set();

function updateFilters_headcount() {
    filterList_headcount.innerHTML = "";
    selectedFilters_headcount.forEach((filter_headcount) => {
        const filterElement_headcount = document.createElement("div");
        filterElement_headcount.classList.add("filter_headcount");
        filterElement_headcount.textContent = filter_headcount;
        const removeButton_headcount = document.createElement("span");
        removeButton_headcount.classList.add("filter-remove_headcount");
        removeButton_headcount.textContent = "X";
        removeButton_headcount.addEventListener("click", () => {
            selectedFilters_headcount.delete(filter_headcount);
            updateFilters_headcount();
        });
        filterElement_headcount.appendChild(removeButton_headcount);
        filterList_headcount.appendChild(filterElement_headcount);
    });
}

function addFilter_headcount(option_headcount) {
    if (!selectedFilters_headcount.has(option_headcount)) {
        selectedFilters_headcount.add(option_headcount);
        updateFilters_headcount();
        // Show the filter section when a filter is added
        filterSection.style.display = "block";
    }
}

includeButtons_headcount.forEach((includeButton, index) => {
    includeButton.addEventListener("click", () => {
        const optionText = optionElements_headcount[index].querySelector("span").textContent;
        addFilter_headcount(optionText);
    });
});

excludeButtons_headcount.forEach((excludeButton, index) => {
    excludeButton.addEventListener("click", () => {
        const optionText = optionElements_headcount[index].querySelector("span").textContent;
        selectedFilters_headcount.delete(optionText);
        updateFilters_headcount();
    });
});

searchInput_headcount.addEventListener("input", () => {
    // Your search functionality here
    // You can filter/search based on selected filters and the search input value
});


///////////////////////////////////// - FILTERS F U N C T I O N - ///////////////////////////////////////////////

const filterList_function = document.querySelector(".filter-list_function");
const options_function = document.querySelector(".options_function_function");
const searchInput_function = document.querySelector(".search-bar_function");
const includeButtons_function = document.querySelectorAll(".include_function");
const excludeButtons_function = document.querySelectorAll(".exclude_function");
const optionElements_function = document.querySelectorAll(".option_function");

const selectedFilters_function = new Set();

function updateFilters_function() {
    filterList_function.innerHTML = "";
    selectedFilters_function.forEach((filter_function) => {
        const filterElement_function = document.createElement("div");
        filterElement_function.classList.add("filter_function");
        filterElement_function.textContent = filter_function;
        const removeButton_function = document.createElement("span");
        removeButton_function.classList.add("filter-remove_function");
        removeButton_function.textContent = "X";
        removeButton_function.addEventListener("click", () => {
            selectedFilters_function.delete(filter_function);
            updateFilters_function();
        });
        filterElement_function.appendChild(removeButton_function);
        filterList_function.appendChild(filterElement_function);
    });
}

function addFilter_function(option_function) {
    if (!selectedFilters_function.has(option_function)) {
        selectedFilters_function.add(option_function);
        updateFilters_function();
        // Show the filter section when a filter is added
        filterSection.style.display = "block";
    }
}

includeButtons_function.forEach((includeButton, index) => {
    includeButton.addEventListener("click", () => {
        const optionText = optionElements_function[index].querySelector("span").textContent;
        addFilter_function(optionText);
    });
});

excludeButtons_function.forEach((excludeButton, index) => {
    excludeButton.addEventListener("click", () => {
        const optionText = optionElements_function[index].querySelector("span").textContent;
        selectedFilters_function.delete(optionText);
        updateFilters_function();
    });
});

searchInput_function.addEventListener("input", () => {
    // Your search functionality here
    // You can filter/search based on selected filters and the search input value
});
