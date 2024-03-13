django.jQuery(document).ready(function () {

    const $listFilters = django.jQuery("#changelist-filter");
    const addFilterButton = () => {
        // if listFilters is not found, return
        if ($listFilters.length === 0) {
            return;
        }
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
        $listFilters.toggle();
    };
    addFilterButton();
    console.log("listFilters.js loaded");
});
