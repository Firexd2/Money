jQuery(document).ready(function($) {

    var flag = window.innerWidth >= 768;
    jconfirm.defaults = {
        theme: 'material',
        closeIcon: true,
        closeIconClass: 'fa fa-close',
        typeAnimated: flag,
        animateFromElement: flag,
        animationSpeed: flag ? 400 : false,
        scrollToPreviousElementAnimate: flag
    };

    $(function(){
        if (window.innerWidth <= 768) {
            var navMain = $(".navbar-offcanvas-touch");
            navMain.on("click", "a:not([data-toggle])", null, function () {
                $('#button-toggle').click()
            });
        }
    });

    function onNavbar() {
        if (window.innerWidth >= 768) {
            $('.navbar-default .dropdown').on('mouseover', function(){
                $('.dropdown-toggle', this).next('.dropdown-menu').show();
            }).on('mouseout', function(){
                $('.dropdown-toggle', this).next('.dropdown-menu').hide();
            });
            $('.dropdown-toggle').click(function() {
                if ($(this).next('.dropdown-menu').is(':visible')) {
                    window.location = $(this).attr('href');
                }
            });
        } else {
            $('.navbar-default .dropdown').off('mouseover').off('mouseout');
        }
    }

    $(window).resize(function() {
        onNavbar();
    });
    onNavbar();

    $('body').on('click', '.help-button', function () {
        var name = $(this).parent().text().slice(0, -1);
        $.alert({
            theme: 'material',
            columnClass: 'col-lg-6 col-md-offset-3',
            title: name,
            type: 'blue',
            content: 'url: /help/' + name + '/'
        })
    });

    $('.version').on('click', function () {
        $.alert({
            theme: 'material',
            title: 'История версий',
            type: 'blue',
            icon: 'fa fa-code-fork',
            content: 'url: /panel/version/'
        })
    });

    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function () {
            navigator.serviceWorker.register('/static/js/sw.js').then(
                function (registration) {
                    // Registration was successful
                    console.log('ServiceWorker registration successful with scope: ', registration.scope);
                },
                function (err) {
                    // registration failed :(
                    console.log('ServiceWorker registration failed: ', err);
                });
        });
    }


});

var scriptsContent;

