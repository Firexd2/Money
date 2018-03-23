function panel_page() {

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
            $(document).ajaxStart(function () {
                Pace.restart();
            });
            var val = $(this).prev().val();
            if (val) {

                $.confirm({
                    title: 'Подтвердите действие',
                    icon: 'fa fa-question',
                    type: 'orange',
                    content: 'Вы подтверждаете изменение суммы ваших накоплений? Советуем поменять её один раз в начале пользования системой.',
                    buttons: {
                        Ok: {
                            text: 'Да',
                            action: function () {
                                $.post('/ajax/correct_free_money/', {value: val}, function (data) {
                                    if (data.status) {
                                        location.reload()
                                    } else {
                                        $.alert({
                                            type: 'red',
                                            icon: 'fa fa-exclamation-triangle',
                                            title: 'Операция отменена!',
                                            content: 'Для успешного изменения суммы ваших накоплений вам нужно ввести число больше 0 или 0.'
                                        })
                                    }
                                });
                            }
                        },
                        Cancel: {
                            text: 'Отмена',
                            action: function () {}
                        }
                    }
                })
            }
        })
    }

    panel();

}

window.scriptsContent = panel_page();