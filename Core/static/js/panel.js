jQuery(document).ready(function($) {

    function panel() {
        $('.slider-block-panel').on('click', function (event) {
            var elem = $(this).children().eq(0);
            if ($('.input-group').has(event.target).length === 0) {
                if (elem.css('margin-top') === '0px') {
                    elem.animate({'margin-top': '-105px'}, 300)
                } else {
                    elem.animate({'margin-top': '0'}, 300)
                }
            }
        });

        $('#btn-freemoney').on('click', function () {
            $(document).ajaxStart(function() { Pace.restart(); });
            var val = $(this).prev().val();
            if (val) {
                $.post('/ajax/correct_free_money/', {value: val}, function (data) {
                    if (data.status) {
                        location.reload()
                    } else {
                        $.alert({
                            type: 'red',
                            icon: 'fa fa-exclamation-triangle',
                            title: 'Операция отменена!',
                            content: 'Для успешного изменения суммы ваших накоплений вам нужно ввести число и/или использовать +/- перед числом для манипуляций с текущей суммой.'
                        })
                    }
                });

            }
        })
    }
    panel();

});