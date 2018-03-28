jQuery(document).ready(function($) {

    jconfirm.defaults = {
        theme: 'material',
        closeIcon: true,
        closeIconClass: 'fa fa-close'
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
            icon: 'fa fa-question-circle-o',
            content: 'url: /help/' + name + '/'
        })
    })

});

var scriptsContent;

