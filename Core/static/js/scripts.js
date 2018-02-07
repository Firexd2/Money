$(document).ready(function() {

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


    function procent(value) {
        var amount = parseInt($('input[name=incom]').val());
        if (amount && value) {
            return (value / (amount / 100)).toFixed(2)
        } else {
            if (amount) {
                return 0
            } else {
                return '-- '
            }
        }
    }

    function Total() {
        var n = 0;
        var p = 0;
        var inputs = $('.cat');
        for (var i=0; i<inputs.length; i++) {
            if (parseInt(inputs.eq(i).val())) {
                n += parseInt(inputs.eq(i).val());
            }
            p += parseInt(inputs.eq(i).parent().next().children().text());
        }
        if (!(isNaN(p))) {
            $('#p').text(p);
            $('#n').text(n);
        } else {
            $('#p').text('-- ');
            $('#n').text('-- ');
        }
    }

    function MaxProcent() {
        var inputs = $('.cat');
        for (var i=0; i<inputs.length; i++) {
            inputs.eq(i).parent().next().children().text(procent(parseInt(inputs.eq(i).val())))
        }
        Total()
    }

    function OnOffInputs() {
        if ($('input[name=incom]').val()) {
            $('.ca').removeAttr("disabled");
            $('.cat').removeAttr("disabled");
        } else {
            $('.ca').attr("disabled", true);
            $('.cat').attr("disabled", true);

        }
    }

    function New() {
        $('input[name=incom]').on('input', function () {
            OnOffInputs();

            if ($(this).val()) {
                $('#amount').text($(this).val());
            } else {
                $('#amount').text('--');
            }
            MaxProcent();
        });
        $('.cat').on('input', function () {
            MaxProcent();
        })


    }
    New();

});