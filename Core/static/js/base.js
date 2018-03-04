jQuery(document).ready(function($) {

    jconfirm.defaults = {
        theme: 'modern',
        closeIcon: true,
        closeIconClass: 'fa fa-close'
    };

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

        var li = $('.navbar-nav').children();
        var path = location.pathname;
        for (var i=0;i<li.length;i++) {

            if (li.eq(i).children('a').attr('href') === path) {
                li.eq(i).addClass('active');
                break
            }
        }

    }
    $(window).resize(function() {
        onNavbar();
    });
    onNavbar();
});