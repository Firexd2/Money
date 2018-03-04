jQuery(document).ready(function($) {
    function home() {

        $('#income').on('click', function () {
            var message;
            $.confirm({
                title: 'Подтверждение начала нового раcсчётного периода',
                icon: 'fa fa-question',
                type: 'orange',
                content: 'Вы точно хотите ввести месячный доход и начать новый месяц?',
                buttons: {
                    Да: {
                        btnClass: 'btn',
                        action: function () {
                            $.post('', {income: $('#income').prev().val()}, function (data) {
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
                                }
                            })
                        }
                    },
                    Отмена: function () {
                    }
                }
            })
        });

        $('#date').on('click', function () {
            var message;
            $.confirm({
                title: 'Подтверждение изменения траты',
                icon: 'fa fa-question',
                type: 'orange',
                content: 'Вы точно хотите изменить дату вашего плана?',
                buttons: {
                    Да: {
                        btnClass: 'btn',
                        action: function () {
                            $.post('', {date: $('#date').prev().val()}, function (data) {
                                if (data.status === 1) {
                                    message = 'Дата успешно изменена!';
                                    $.alert({
                                        icon: 'fa fa-check',
                                        type: 'green',
                                        title: '<b>Операция выполнена!</b>',
                                        content: message
                                    });
                                } else if (data.status === 0) {
                                    message = 'Дата не была изменена, так как нельзя поменять дату на будущую.';
                                    $.alert({
                                        icon: 'fa fa-exclamation-triangle',
                                        type: 'red',
                                        title: '<b style="color: red">Операция отменена!</b>',
                                        content: message
                                    });
                                }
                            })
                        }
                    },
                    Отмена: function () {
                    }
                }
            });
        });

        $('#delete').on('click', function () {

            $.confirm({
                title: 'Подтверждение удаления плана',
                icon: 'fa fa-exclamation-triangle',
                type: 'red',
                content: 'Вы точно хотите удалить ваш план распределения бюджета?',
                buttons: {
                    Да: {
                        btnClass: 'btn',
                        action: function () {
                            $.post('', {delete: ''}, function (data) {
                                if (data.status === 1) {
                                    location.href = '/panel/';
                                }
                            })
                        }
                    },
                    Отмена: function () {
                    }
                }
            })
        })
    }

    home();
});