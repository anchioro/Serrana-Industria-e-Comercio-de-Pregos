$(document).ready(function() {
    const currentLocation = location.pathname;
    const $menuItems = $(".nav-link");
    const $logoText = $(".font-logo");
    const $logoSubText = $(".font-sub-logo");
    const $clearButton = $("#clear-button");
    const $searchField = $("#search-field");
    
    $clearButton.click(function() {
        $searchField.val("");
        $searchField.focus();
    });

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

    $(window).on('resize scroll', function() {
        checkLocation();
    });

    $.each($menuItems, (_, menu) => {
        const $menu = $(menu);

        if ($menu.attr("href") === currentLocation) {
            $menu.attr("class", "nav-link link-dark color-theme");
        } else {
            $menu.attr("class", "nav-link link-dark");
        }
    });

    checkLocation();
});