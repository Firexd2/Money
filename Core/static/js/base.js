jQuery(document).ready(function($) {

    jconfirm.defaults = {
        theme: 'modern',
        closeIcon: true,
        closeIconClass: 'fa fa-close'
    };

    $(function(){
        if (window.innerWidth <= 768) {
            var navMain = $(".navbar-collapse");
            navMain.on("click", "a:not([data-toggle])", null, function () {
                navMain.collapse('hide');
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

});

var scriptsContent;

