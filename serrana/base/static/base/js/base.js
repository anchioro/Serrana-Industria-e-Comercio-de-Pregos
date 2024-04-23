$(document).ready(function() {
    const currentLocation = location.pathname;
    const $menuItems = $(".nav-link");
    const $logoText = $(".font-logo");
    const $logoSubText = $(".font-sub-logo");
    const $clearButton = $("#clear-button");
    const $searchField = $("#search-field");
    const $idAction = $("#id_action")
    const $idActionOption = $("#id_action option[value='']")
    const $collapseRow = $(".collapse-row");

    // Edition information in the products/history.html under the selected row
    $collapseRow.hide();
    $("[data-bs-toggle='collapse']").click(function() {
        var targetId = $(this).data("bs-target");
        $(targetId).closest(".collapse-row").toggle();
    });

    // Disable the placeholder text in selection field of products/action.html
    $idActionOption.text("Selecione uma opção");
    $idAction.on("click", function() {
        $(this).find($idActionOption).prop("disabled", true);
    });
    
    // Clear the search  input on click event
    $clearButton.click(function() {
        $searchField.val("");
        $searchField.focus();
    });

    // Set the subtitle of the logo according to the page's path in base.html
    var $lastLocation = $logoText.offset();
    const checkLocation = function() {
        const $currentLocation = $logoText.offset();
        $lastLocation = $currentLocation;

        const $offsetHeight = $logoText.height();
        const $top = $lastLocation.top;
        const $left = $lastLocation.left;

        $logoSubText.css({
            "position": "absolute",
            "top": $top+$offsetHeight-10 + "px",
            "left": $left + "px"
        });
    };

    $(window).on("resize scroll", function() {
        checkLocation();
    });

    // Add the color theme to the currently seleted tab of navbar
    $.each($menuItems, (_, menu) => {
        const $menu = $(menu);

        if ($menu.attr("href") === currentLocation) {
            $menu.addClass("color-theme");
        } else {
            $menu.removeClass("color-theme");
        }
    });

    // Call the fuction to set  the initial position for the logo text
    checkLocation();
});