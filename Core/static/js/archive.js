jQuery(document).ready(function($) {

    function load_report(date_one, date_two) {
        var plan = location.pathname;
        $('#archive-stat').load(plan + 'archive/' + date_one + '/' + date_two + '/', function () {
            count_procent_table_tags();
            NProgress.done();
        })
    }

    $('body').on('click', '#submit-archive', function () {
    });


    function default_dates() {
        load_report('2018-03-05', '2018-03-15');
    }

    default_dates();

    $('body').on('click', '.help-dates', function (e) {
        var id = e.target.id;
        get_and_change_dates(id)
    });

    function get_and_change_dates(id) {
        var plan = location.pathname;
        $.post(plan + 'archive/' + id + '/', function (data) {
            $('#date-one').val(data.date_one);
            $('#date-two').val(data.date_two);
        })
    }

    $('body').on('click', '#edit-interval', function () {
        NProgress.set(0.4);
        $.confirm({
            title: 'Выбрать период',
            content: '    <div style="margin-bottom: 10px" class="input-group">\n' +
            '        <span style="width: 40px" class="input-group-addon"><b>1</b></span>\n' +
            '        <input style="width: 140%" name="name-plan" id="date-one" value="{{ date_one }}" type="date" class="form-control"/>\n' +
            '    </div>\n' +
            '    <div style="margin-bottom: 10px" class="input-group">\n' +
            '        <span style="width: 40px" class="input-group-addon"><b>2</b></span>\n' +
            '        <input style="width: 140%" name="name-plan" id="date-two" value="{{ date_two }}" type="date" class="form-control"/>\n' +
            '    </div>\n' +
            '    <div class="help-dates" style="margin-bottom: 15px">\n' +
            '\n' +
            '        <span id="time-all">за все время</span> <span id="time-1">за 1 месяц</span> <span id="time-3">за 3 месяца</span> <span id="time-6">за полгода</span> <span id="time-12">за год</span> <br>\n' +
            '        <span id="period-1">последний период</span> <span id="period-2">за 2 последних периода</span> <span id="period-3">за 3 последних периода</span>\n' +
            '    </div>',
            buttons:
                {
                    Ok: {
                        text: 'Выбрать',
                        btnClass: 'btn',
                        action:
                            function () {
                                var date_one = $('#date-one').val();
                                var date_two = $('#date-two').val();
                                load_report(date_one, date_two)
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


    // Надо описать логику первоначальной загрузки и логику вспомогательных кнопок


    function count_procent_table_tags() {
        var values =  $('.tags-value');
        var procent;
        var sum = 0;
        for (var i=0;i<values.length;i++) {
            sum += parseInt(values.eq(i).text())
        }
        for (var i=0;i<values.length;i++) {
            procent = parseInt(values.eq(i).text()) / sum * 100;
            values.eq(i).prev().css({'background': 'linear-gradient(to right, #ececec ' + procent + '%, white ' + procent + '%)'})
        }
    }

});