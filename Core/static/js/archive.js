function archive() {

    function load_report(date_one, date_two) {
        var plan = location.pathname;

        $('#archive-stat').load(plan + 'archive/' + date_one + '/' + date_two + '/', function () {
            count_procent_table_tags();
        });
    }

    $('#archive-stat').on('click', '#edit-interval', function () {
        $(document).ajaxStart(function() { Pace.restart(); });
        $.confirm({
            title: 'Выбрать период',
            content: 'url:/alert/change_date/',
            buttons:
                {
                    Ok: {
                        text: 'Выбрать',
                        btnClass: 'btn',
                        action:
                            function () {
                                var date_one = $('#date-one').val();
                                var date_two = $('#date-two').val();
                                if ((date_one || date_two) && (date_one <= date_two)) {
                                    load_report(date_one, date_two)
                                } else {
                                    $.alert({
                                        title: 'Операция отменена',
                                        type: 'orange',
                                        content: 'Вы должны ввести две даты, причем вторая дата должна быть не раньше первой.'
                                    });
                                }
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

    function default_dates() {
        var plan = location.pathname;
        $.post(plan + 'archive/' + 'time-all' + '/', function (data) {
            load_report(data.date_one, data.date_two)
        })
    }

    default_dates();



    function count_procent_table_tags() {
        var values =  $('.tags-value');
        var procent;
        var sum = 0;
        for (var i=0;i<values.length;i++) {
            sum += parseInt(values.eq(i).text().replace('.', ''))
        }
        for (var i=0;i<values.length;i++) {
            procent = parseInt(values.eq(i).text().replace('.', '')) / sum * 100;
            values.eq(i).prev().css({'background': 'linear-gradient(to right, #ececec ' + procent + '%, white ' + procent + '%)'})
        }
    }

    function open_details_archive() {
        $('.navigation').on('click', function () {
            var id = $(this).attr('id');
            $.alert({
                title: 'Детализация архива',
                content: 'url: /archive/detail/' + id + '/'
            })
        })
    }

    open_details_archive();
}

window.scriptsContent = archive();

