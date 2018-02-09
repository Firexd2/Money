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
            return Math.round(value / (amount / 100))
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
        var inputs = $('.cat');
        var amount = parseInt($('input[name=incom]').val());
        var tr = $('#total-tr');
        for (var i=0; i<inputs.length; i++) {
            if (parseInt(inputs.eq(i).val())) {
                n += parseInt(inputs.eq(i).val());
            }
        }
        if ($('input[name=incom]').val()) {
            $('#p').text(100 - Math.ceil(n / (amount / 100)));
            $('#o').text(amount - n);
            if (n === amount) {
                tr.css({'background': 'rgba(28, 255, 0, 0.35)'})
            } else if (n > amount) {
                tr.css({'background': 'rgba(255, 7, 0, 0.31)'})
            } else {
                tr.css({'background': 'none'})
            }
        } else {
            $('#p').text('-- ');
            $('#o').text('--');
            tr.css({'background': 'none'})
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

        $('body').on('input', '.cat', function () {
            MaxProcent();
        });

        $('#add-category').on('click', function () {
            var tr = $('tr');
            var incom = $('input[name=incom]').val();
            var disabled = '';
            var proc = '0';
            if (!(incom)) {
                disabled = 'disabled';
                proc = '-- '
            }
            tr.eq(tr.length-4).after('<tr>\n' +
                '<td><b>' + (tr.length-3) + '</b></td>\n' +
                '<td><input ' + disabled +  ' name="name-cat' + (tr.length-3) + '" type="text" class="form-control ca" placeholder="Пример: На еду"/></td>\n' +
                '<td><input ' + disabled +  ' name="incom' + (tr.length-3) + '" type="number" class="form-control cat"/></td>\n' +
                '<td style="text-align: center"><span>' + proc + '</span>%</td>\n' +
                '</tr>');
        });

        $('#remove-category').on('click', function () {
            $('tr').eq($('tr').length-4).remove();
            Total()
        });

        $('form[name=new]').on('submit', function (e) {

            if ($('#o').text() !== '0') {
                e.preventDefault();
                if (!($('#name-input').val())) {
                    $('#error-form').text(' Вы не ввели название конфигурации')
                } else if ($('#o').text() === '--') {
                    $('#error-form').text(' Вы не ввели и не распределили сумму')
                } else if (parseInt($('#o').text()) > 0) {
                    $('#error-form').text(' У вас остался неиспользованный остаток')
                } else {
                    $('#error-form').text(' Вы превысили лимит вашей суммы')
                }
            }
        })
    }
    New();
});