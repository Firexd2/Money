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
    }

    panel();

    $('form[name=income]').on('submit', function (e) {
        e.preventDefault();
        var $form = $(this);
        $(document).ajaxStart(function () {
            Pace.restart();
        });
        $.confirm({
            title: 'Подтвердите действие',
            type: 'orange',
            content: 'Вы подтверждаете ввод дохода?',
            buttons: {
                Ok: {
                    text: 'Да',
                    btnClass: 'btn',
                    action: function () {
                        var data = $form.serializeArray();
                        var url = '/ajax/add_money/';
                        $.ajax({
                            type: "POST",
                            url: url,
                            data: data,
                            success: function () {
                                location.reload()
                            }
                        })
                    }
                },
                Cancel: {
                    text: 'Отмена',
                    action: function () {}
                }
            }
        })
    });

    $('form[name=take-money]').on('submit', function (e) {
        e.preventDefault();
        var $form = $(this);
        $(document).ajaxStart(function () {
            Pace.restart();
        });
        $.confirm({
            title: 'Подтвердите действие',
            type: 'orange',
            content: 'Вы подтверждаете изъятие денег с накопительного счета?',
            buttons: {
                Ok: {
                    text: 'Да',
                    btnClass: 'btn',
                    action: function () {
                        var data = $form.serializeArray();
                        var url = '/ajax/take_money/';
                        $.ajax({
                            type: "POST",
                            url: url,
                            data: data,
                            success: function () {
                                location.reload()
                            }
                        })
                    }
                },
                Cancel: {
                    text: 'Отмена',
                    action: function () {}
                }
            }
        })
    });
    $(".spincrement").spincrement({
        from: 0,
        duration: 2000,
        thousandSeparator: "."
    });
}

window.scriptsContent = panel_page();