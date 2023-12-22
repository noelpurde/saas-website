let selectedFilters_geography = new Set();
let selectedFilters_headcount = new Set();
let selectedFilters_function = new Set();

///////////////////////////////////// - FILTERS G E O G R A P H Y - ///////////////////////////////////////////////
let filterList_geography = document.querySelector(".filter-list_geography");
const options_geography = document.querySelector(".options_geography");
const searchInput_geography = document.querySelector(".search-bar_geography");
const includeButtons_geography = document.querySelectorAll(".include_geography");
const excludeButtons_geography = document.querySelectorAll(".exclude_geography");
const optionElements_geography = document.querySelectorAll(".option_geography");

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
    //Filters for the AJAX
    const filters = {
      geography: Array.from(selectedFilters_geography),
      headcount: Array.from(selectedFilters_headcount),
      function: Array.from(selectedFilters_function),
  };
  updateData(filters);
}
function addFilter_geography(option_geography) {
    if (!selectedFilters_geography.has(option_geography)) {
        selectedFilters_geography.add(option_geography);
        updateFilters_geography();
    }
    else {
        selectedFilters_geography.delete(option_geography)
        updateFilters_geography();
    }
}

function addFilter_geography_include(option_geography) {
  if (!selectedFilters_geography.has(option_geography)) {
      selectedFilters_geography.add(option_geography);
      updateFilters_geography();
  }
}
includeButtons_geography.forEach((includeButton, index) => {
    includeButton.addEventListener("click", () => {
        const optionText = optionElements_geography[index].querySelector("span").textContent;
        addFilter_geography_include(optionText);
        updateFilters_geography();
    });
});
excludeButtons_geography.forEach((excludeButton, index) => {
    excludeButton.addEventListener("click", () => {
        const optionText = optionElements_geography[index].querySelector("span").textContent;
        selectedFilters_geography.delete(optionText);
        updateFilters_geography();
    });
});

///////////////////////////////////// - FILTERS H E A D C O U N T - ///////////////////////////////////////////////

let filterList_headcount = document.querySelector(".filter-list_headcount");
const options_headcount = document.querySelector(".options_headcount");
const searchInput_headcount = document.querySelector(".search-bar_headcount");
const includeButtons_headcount = document.querySelectorAll(".include_headcount");
const excludeButtons_headcount = document.querySelectorAll(".exclude_headcount");
const optionElements_headcount = document.querySelectorAll(".option_headcount");

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
      //Filters for the AJAX
      const filters = {
          geography: Array.from(selectedFilters_geography),
          headcount: Array.from(selectedFilters_headcount),
          function: Array.from(selectedFilters_function),
      };
      updateData(filters);
}
function addFilter_headcount(option_headcount) {
    if (!selectedFilters_headcount.has(option_headcount)) {
        selectedFilters_headcount.add(option_headcount);
        updateFilters_headcount();
    }
}
includeButtons_headcount.forEach((includeButton, index) => {
    includeButton.addEventListener("click", () => {
        const optionText = optionElements_headcount[index].querySelector("span").textContent;
        addFilter_headcount(optionText);
        updateFilters_headcount()
    });
});
excludeButtons_headcount.forEach((excludeButton, index) => {
    excludeButton.addEventListener("click", () => {
        const optionText = optionElements_headcount[index].querySelector("span").textContent;
        selectedFilters_headcount.delete(optionText);
        updateFilters_headcount();
    });
});

///////////////////////////////////// - FILTERS F U N C T I O N - ///////////////////////////////////////////////

let filterList_function = document.querySelector(".filter-list_function");
const options_function = document.querySelector(".options_function");
const searchInput_function = document.querySelector(".search-bar_function");
const includeButtons_function = document.querySelectorAll(".include_function");
const excludeButtons_function = document.querySelectorAll(".exclude_function");
const optionElements_function = document.querySelectorAll(".option_function");

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
      //Filters for the AJAX
      const filters = {
          geography: Array.from(selectedFilters_geography),
          headcount: Array.from(selectedFilters_headcount),
          function: Array.from(selectedFilters_function),
      };
      updateData(filters);
}
function addFilter_function(option_function) {
    if (!selectedFilters_function.has(option_function)) {
        selectedFilters_function.add(option_function);
        updateFilters_function();
    }
}
includeButtons_function.forEach((includeButton, index) => {
    includeButton.addEventListener("click", () => {
        const optionText = optionElements_function[index].querySelector("span").textContent;
        addFilter_function(optionText);
        updateFilters_function();
    });
});
excludeButtons_function.forEach((excludeButton, index) => {
    excludeButton.addEventListener("click", () => {
        const optionText = optionElements_function[index].querySelector("span").textContent;
        selectedFilters_function.delete(optionText);
        updateFilters_function();
    });
});

//---------------------------AJAX FUNCTION---------------------------

function updateData(filters) {
  fetch('/update_data', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify(filters),
  })
  .then(response => response.json())
  .then(data => {
      console.log('Updated data from server:', data);
      updateTable(data.filtered_data);
  })
  .catch(error => {
      console.error('Error updating data:', error);
  });
}


function updateTable(filteredData) {
  // Updating HTML table with the new filtered data dynamically
  const tableBody = document.querySelector('.search_table tbody');
  tableBody.innerHTML = '';  // Clear existing rows

  // Add the static header row
  const headerRow = document.createElement('tr');
  headerRow.innerHTML = `
    <th>Name</th>
    <th>Title</th>
    <th>Company</th>
    <th>Region</th>
    <th>Company Size</th>
    <th>Function</th>
    <th>Product Bought</th>
    <th>Email</th>
  `;
  tableBody.appendChild(headerRow);

  // Add dynamic rows
  filteredData.forEach(user => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${user[1]}</td>
      <td>${user[2]}</td>
      <td>${user[3]}</td>
      <td>${user[4]}</td>
      <td>${user[5]}</td>
      <td>${user[6]}</td>
      <td>${user[7]}</td>
      <td>${user[8]}</td>
    `;
    tableBody.appendChild(row);
  });
}

document.addEventListener('DOMContentLoaded', function() {
    fetch('/filter_db_to_js_update')
        .then(response => response.json())
        .then(data => {
            if (Array.isArray(data)) {
                // Handle each element of the array
                data.forEach(item => {
                    console.log(item);

                    // Filters being added from db filtered if empty
                    if (item.geography.length > 0 && item.geography[0] !== "") {
                        selectedFilters_geography.add(...item.geography);
                    }

                    if (item.headcount.length > 0 && item.headcount[0] !== "") {
                        selectedFilters_headcount.add(...item.headcount);
                    }

                    if (item.function.length > 0 && item.function[0] !== "") {
                        selectedFilters_function.add(...item.function);
                    }
                    // To update the filters added from db to admin page "Refresh Update"
                    updateFilters_geography();
                    updateFilters_headcount();
                    updateFilters_function();
                });
            }
        })
        .catch(error => console.error('Error:', error));
});