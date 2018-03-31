function home() {
    var name = location.pathname.slice(1,-1);

    $('form[name=new-period]').on('submit', function (e) {
        e.preventDefault();
        var $form = $(this);
        $(document).ajaxStart(function () {Pace.restart()});
            var message;
            $.confirm({
                title: 'Подтверждение начала нового расчётного периода',
                type: 'orange',
                content: 'Вы точно хотите начать новый рассчетный период?',
                buttons: {
                    Ok: {
                        text: 'Да',
                        btnClass: 'btn',
                        action: function () {
                            var data = $form.serializeArray();
                            var url = '/ajax/start_new_period/';
                            $.ajax({
                                type: "POST",
                                url: url,
                                data: data,
                                success: function (data) {
                                    if (data.status === 1) {
                                        message = '<b>Операция прошла успешно!</b><br> На накопительный счет зачислено <b>' + data.balance + ' р.</b> остатка за предыдущий месяц, ' +
                                            'обнулены все траты, ' +
                                            'история трат перемещена в архив.';
                                        $.alert({
                                            type: 'green',
                                            title: '<b>Операция выполнена!</b>',
                                            content: message
                                        });
                                        $('#home-button-menu').click();
                                    } else if (data.status === 2 ) {
                                        $.alert({
                                            title: 'Внимание!',
                                            type: 'orange',
                                            content: 'При перерасчете лимитов категорий получилось отрицательное значение, поэтому категории были рассчитаны по ровну. <b>Настоятельно рекомендуем сделать перерасчет лимитов в ручную в настройках!</b>'
                                        })
                                    } else if (data.status === 0) {
                                        $.alert({
                                            type: 'red',
                                            title: 'Операция отменена!',
                                            content: 'Критическая ошибка. Попробуйте еще раз!'
                                        })
                                    }
                                }
                            })


                        }
                    },
                    Cancel: {
                        text: 'Отмена',
                        action: function () {
                        }
                    }
                }
            });
        });


    $('form[name=middle-income]').on('submit', function (e) {
        e.preventDefault();
        var $form = $(this);
        $(document).ajaxStart(function () {Pace.restart()});
        $.confirm({
            title: 'Подтвердите действие',
            type: 'orange',
            content: 'Вы подтверждаете введение промежуточного дохода в текущий период?',
            buttons: {
                Ok: {
                    text: 'Да',
                    btnClass: 'btn',
                    action: function () {
                        var data = $form.serializeArray();
                        var url = '/ajax/middle_icone_plan/';
                        $.ajax({
                            type: "POST",
                            url: url,
                            data: data,
                            success: function (data) {
                                if (data.status === 1) {
                                    $.alert({
                                        title: 'Операция выполнена!',
                                        type: 'green',
                                        content: 'Деньги пропорционально распределёны'
                                    });
                                    $('#home-button-menu').click();
                                } else {
                                    $.alert({
                                        type: 'red',
                                        title: 'Операция отменена!',
                                        content: 'Критическая ошибка. Попробуйте еще раз!'
                                    })
                                }
                            }
                        })
                    }
                },
                Cancel: {
                    text: 'Отмена',
                    action: function () {
                    }
                }
            }
        })
    });

    $('#delete').on('click', function () {
        $(document).ajaxStart(function () {
            Pace.restart();
        });
        $.confirm({
            title: 'Подтверждение удаления плана',
            type: 'red',
            content: 'Вы точно хотите удалить ваш план распределения бюджета?',
            buttons: {
                Ok: {
                    text: 'Да',
                    btnClass: 'btn',
                    action: function () {
                        $.post('/ajax/delete_plan/', {name: name}, function (data) {
                            if (data.status === 1) {
                                location.href = '/panel/';
                            }
                        });
                    }
                },
                Cancel: {
                    text: 'Отмена',
                    action: function () {
                    }
                }
            }
        })
    })
}

window.scriptsContent = home();
