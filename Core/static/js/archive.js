function load_report(date_one, date_two) {
    var plan = location.pathname;

    $('#archive-stat').load(plan + 'archive/' + date_one + '/' + date_two + '/', function () {
        count_procent_table_tags();
        NProgress.done();
    });
}

function default_dates() {
    var plan = location.pathname;
    $.post(plan + 'archive/' + 'time-all' + '/', function (data) {
        load_report(data.date_one, data.date_two)
    })
}

default_dates();

function get_and_change_dates(id) {
    var plan = location.pathname;
    $.post(plan + 'archive/' + id + '/', function (data) {
        $('#date-one').val(data.date_one);
        $('#date-two').val(data.date_two);
    })
}

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

