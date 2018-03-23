function home() {
    var name = location.pathname.slice(1,-1);

    $('#income').on('click', function () {
        var value = $('#income').prev().val();
        if (value) {
            $(document).ajaxStart(function () {
                Pace.restart();
            });
            var message;
            $.confirm({
                title: 'Подтверждение начала нового расчётного периода',
                icon: 'fa fa-question',
                type: 'orange',
                content: 'Вы точно хотите ввести месячный доход и начать новый месяц?',
                buttons: {
                    Ok: {
                        text: 'Да',
                        btnClass: 'btn',
                        action: function () {
                            $.post('/ajax/start_new_period/', {income: value, name: name}, function (data) {
                                if (data.status === 1) {
                                    message = '<b>Операция прошла успешно!</b><br> На накопительный счет зачислено <b>' + data.balance + ' р.</b> остатка за предыдущий месяц, ' +
                                        'обнулены все траты, ' +
                                        'история трат перемещена в архив.';
                                    $.alert({
                                        icon: 'fa fa-check',
                                        type: 'green',
                                        title: '<b>Операция выполнена!</b>',
                                        content: message
                                    });
                                    $('#home-button-menu').click();
                                } else {
                                    $.alert({
                                        icon: 'fa fa-exclamation-triangle',
                                        type: 'red',
                                        title: 'Операция отменена!',
                                        content: 'Критическая ошибка. Попробуйте еще раз!'
                                    })
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
        }
    });

    $('#middle-income').on('click', function () {
        var value = $('#middle-income').prev().val();
        if (value) {
            $(document).ajaxStart(function () {
                Pace.restart();
            });
            $.confirm({
                title: 'Подтвердите действие',
                icon: 'fa fa-question',
                type: 'orange',
                content: 'Вы подтверждаете введение промежуточного дохода в текущий период?',
                buttons: {
                    Ok: {
                        text: 'Да',
                        btnClass: 'btn',
                        action: function () {
                            $.post('/ajax/middle_icone_plan/', {
                                name: name,
                                middle_income: value
                            }, function (data) {
                                if (data.status === 1) {
                                    $.alert({
                                        title: 'Операция выполнена!',
                                        icon: 'fa fa-check',
                                        type: 'green',
                                        content: 'Доход успешно добавлен и пропорционально распределён'
                                    });
                                    $('#home-button-menu').click();
                                } else {
                                    $.alert({
                                        icon: 'fa fa-exclamation-triangle',
                                        type: 'red',
                                        title: 'Операция отменена!',
                                        content: 'Критическая ошибка. Попробуйте еще раз!'
                                    })
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
        }
    });

    // $('#date').on('click', function () {
    //     $(document).ajaxStart(function() { Pace.restart(); });
    //     var message;
    //     $.confirm({
    //         title: 'Подтверждение изменения траты',
    //         icon: 'fa fa-question',
    //         type: 'orange',
    //         content: 'Вы точно хотите изменить дату вашего плана?',
    //         buttons: {
    //             Ok: {
    //                 text: 'Да',
    //                 btnClass: 'btn',
    //                 action: function () {
    //                     $.post('/ajax/edit_date/', {date: $('#date').prev().val(), name: name}, function (data) {
    //                         if (data.status === 1) {
    //                             message = 'Дата успешно изменена!';
    //                             $.alert({
    //                                 icon: 'fa fa-check',
    //                                 type: 'green',
    //                                 title: '<b>Операция выполнена!</b>',
    //                                 content: message
    //                             });
    //                         } else if (data.status === 0) {
    //                             message = 'Дата не была изменена, так как нельзя поменять дату на будущую.';
    //                             $.alert({
    //                                 icon: 'fa fa-exclamation-triangle',
    //                                 type: 'red',
    //                                 title: '<b style="color: red">Операция отменена!</b>',
    //                                 content: message
    //                             });
    //                         }
    //                         $('#home-button-menu').click();
    //                     })
    //                 }
    //             },
    //             Cancel: {
    //                 text: 'Отмена',
    //                 action : function () {
    //                 }
    //             }
    //         }
    //     });
    // });

    $('#delete').on('click', function () {
        $(document).ajaxStart(function() { Pace.restart(); });
        $.confirm({
            title: 'Подтверждение удаления плана',
            icon: 'fa fa-exclamation-triangle',
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
