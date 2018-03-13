jQuery(document).ready(function($) {

    function load_report() {
        var plan = location.pathname;
        var date_one = '2018-03-11';
        var date_two = '2018-03-14';
        $('#archive-stat').load(plan + 'archive/' + date_one + '/' + date_two + '/', function () {
            count_procent_table_tags()
        })
    }


    // function default_dates() {
    //
    //
    //     load_report(date_one, date_two);
    // }

    // default_dates();

    load_report();

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