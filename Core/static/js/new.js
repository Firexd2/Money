jQuery(document).ready(function($) {

    function procent(value) {
        var amount = parseInt($('input[name=income]').val());
        if (amount && value) {
            return Math.round(value / (amount / 100))
        } else {
            if (amount) {
                return 0
            } else {
                return '-- ';
            }
        }
    }

    function Total() {
        var n = 0;
        var inputs = $('.cat');
        var amount = parseInt($('input[name=income]').val());
        var tr = $('#total-tr');
        for (var i=0; i<inputs.length; i++) {
            if (parseInt(inputs.eq(i).val())) {
                n += parseInt(inputs.eq(i).val());
            }
        }
        if ($('input[name=income]').val()) {
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
        if ($('input[name=income]').val()) {
            $('.ca').removeAttr("disabled");
            $('.cat').removeAttr("disabled");
        } else {
            $('.ca').attr("disabled", true);
            $('.cat').attr("disabled", true);
        }
    }


    function New() {

        // Для редактирования конфигурации
        MaxProcent();
        if ($('#table-icon').length > 0) {
            $('#table-icon').find('.' + $('input[name=icon]').val().slice(3)).parent().addClass('active-icons');
        }
        //

        $('input[name=income]').on('input', function () {
            OnOffInputs();
            MaxProcent();
        });



        $('body').on('input', '.cat', function () {
            MaxProcent();
        });

        $('#add-category').on('click', function () {
            var tr = $('tr');
            var income = $('input[name=income]').val();
            var disabled = '';
            var proc = '0';
            if (!(income)) {
                disabled = 'disabled';
                proc = '-- '
            }
            tr.eq(tr.length-4).after('<tr>\n' +
                '<td><b>' + (tr.length-3) + '</b></td>\n' +
                '<td><input ' + disabled +  ' name="name-cat' + (tr.length-3) + '" type="text" class="form-control ca" placeholder="Пример: На еду"/></td>\n' +
                '<td><input ' + disabled +  ' name="income' + (tr.length-3) + '" type="number" class="form-control cat"/></td>\n' +
                '<td style="text-align: center"><span>' + proc + '</span>%</td>\n' +
                '</tr>');
        });

        $('#remove-category').on('click', function () {
            $('tr').eq($('tr').length-4).remove();
            Total()
        });

        $('form[name=new]').on('submit', function (e) {

            function repeat_category() {
                var names_category = $('.ca');
                var array = [];
                var val;
                for (var i=0;i<names_category.length;i++) {
                    val = names_category.eq(i).val();
                    if (array.indexOf(val) === -1) {
                        array.push(val)
                    }
                }
                if (names_category.length !== array.length) {
                    return true
                } else {
                    return false
                }
            }
            if (repeat_category()) {
                e.preventDefault();
                $('#error-form').text(' Категории не могут иметь одинаковое название')
            }
            if ($('#o').text() !== '0') {
                e.preventDefault();
                if (!($('#name-input').val())) {
                    $('#error-form').text(' Вы не ввели название плана')
                } else if ($('#o').text() === '--') {
                    $('#error-form').text(' Вы не ввели и не распределили сумму')
                } else if (parseInt($('#o').text()) > 0) {
                    $('#error-form').text(' У вас остался неиспользованный остаток')
                } else {
                    $('#error-form').text(' Вы превысили лимит вашей суммы')
                }
            }



        });

        $('.icons').on('click', function () {
            var Class = $(this).children().attr('class');
            $('input[name=icon]').val(Class);
            $('.icons').removeClass('active-icons');
            $(this).addClass('active-icons');
        })

    }
    New();

});