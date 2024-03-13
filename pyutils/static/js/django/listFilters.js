django.jQuery(document).ready(function () {
  const addFilterButton = () => {
    django
      .jQuery("ul.object-tools")
      .append(
        "<li><button id='filterToggleButton' class='button bg-gray-100'>Filters</button>",
      );
    const $filterToggleButton = django.jQuery("#filterToggleButton");
    $filterToggleButton.click(onFilterToggleButtonClick);
    $filterToggleButton.click();
  };

  const onFilterToggleButtonClick = () => {
    const $filters = django.jQuery("#changelist-filter");
    $filters.toggle();
  };
  addFilterButton();
  console.log("listFilters.js loaded");
});
