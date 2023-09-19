const filterList = document.querySelector(".filter-list_geography");
const options = document.querySelector(".options_geography");
const searchInput = document.querySelector(".search-bar_geography");
const includeButtons = document.querySelectorAll(".include");
const excludeButtons = document.querySelectorAll(".exclude");
const optionElements = document.querySelectorAll(".option_geography");

const selectedFilters = new Set();

function updateFilters() {
    filterList.innerHTML = "";
    selectedFilters.forEach((filter_geography) => {
        const filterElement = document.createElement("div");
        filterElement.classList.add("filter_geography");
        filterElement.textContent = filter_geography;
        const removeButton = document.createElement("span");
        removeButton.classList.add("filter-remove_geography");
        removeButton.textContent = "X";
        removeButton.addEventListener("click", () => {
            selectedFilters.delete(filter_geography);
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

//Map check to remove existent filters
function removeContinent(classname) {
  if(selectedFilters.has(classname)){
    selectedFilters.delete(classname);
    updateFilters();
  }
}

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
/////////////////////////////////////////////////////////////////////////////////
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
        addFilter("Europe")
        removeContinent("Europe")
        break;
      case "asia":
        addFilter("Asia")
        removeContinent("Asia")
        break;
      case "northAmerica":
        addFilter("North America")
        removeContinent("North America")
        break;
      case "southAmerica":
        addFilter("South America")
        removeContinent("South America")
        break;
      case "africa":
        addFilter("Africa")
        removeContinent("Africa")
        break;
      case "oceania":
        addFilter("Oceania")
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


  
  
  

