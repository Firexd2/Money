jQuery(document).ready(function($) {

    function stat() {
        var item_cost = $('.cost-table');
        var item_hide = $('.hide');
        var costs;
        var amount_cost = 0;

        for (var i=0;i<item_cost.length;i++) {
            costs = item_hide.eq(i).text().split(' ');

            if (costs.length === 1) {
                item_cost.eq(i).html(0);
                continue
            }

            for (var j=0;j<costs.slice(0,-1).length;j++) {

                amount_cost += parseInt(costs[j])
            }
            item_cost.eq(i).html(amount_cost);
            amount_cost = 0;
        }

        var category_all = $('.category-table');
        var balance = $('.balance-table');
        var item;
        var procent;

        var amount_costs = 0;
        var amount_max = 0;

        for (var q=0;q<category_all.length;q++) {
            item = category_all.eq(q).text().split('/');
            balance.eq(q).html(parseInt(item[1]) - parseInt(item[0]));
            procent = Math.round(100 - parseInt(item[0]) / parseInt(item[1]) * 100);
            amount_costs += parseInt(item[0]);
            amount_max += parseInt(item[1]);

            if (procent > 30) {
                balance.eq(q).css({'color': '#00f100'});
                category_all.eq(q).css({'color': '#00f100'});
            } else if (procent > 5) {
                balance.eq(q).css({'color': '#ffc211'});
                category_all.eq(q).css({'color': '#ffc211'});
            } else {
                balance.eq(q).css({'color': 'red'});
                category_all.eq(q).css({'color': 'red'});
            }
        }

        $('#amount-table-1').html(amount_costs);
        $('#amount-table-2').html(amount_max);
        $('#amount-balance').html(amount_max - amount_costs);
        $('#amount-balance-procent').html(Math.round(100 - amount_costs / amount_max * 100) + '%');


        function week_table() {
            function count_table() {
                var data = $('.category-table');
                var week = parseInt($('#week').val());
                var balance = $('.balance-week');
                var proc = $('.proc-week');
                var amount_balance = 0;
                var for_proc_cost = 0;
                var for_proc_limit = 0;
                var current;
                var cost;
                var limit;

                for (var i=0;i<data.length;i++) {
                    current = data.eq(i).text().split('/');
                    cost = parseInt(current[0]);
                    limit = parseInt(current[1]);

                    var result = count_for_week_table(week, cost, limit);
                    if (!(balance.eq(i).parent().is(':hidden'))) {
                        amount_balance += result[0];
                        for_proc_cost += cost;
                        for_proc_limit += limit;
                    }
                    balance.eq(i).html(result[0]);
                    proc.eq(i).html(parseInt(result[1]) + ' %');

                    if (result[1] > 30) {
                        balance.eq(i).css({'color': '#00f100'});
                    } else if (result[1] > 5) {
                        balance.eq(i).css({'color': '#ffc211'});
                    } else {
                        balance.eq(i).css({'color': 'red'});
                    }
                }

                $('#amount-table-week-1').html(amount_balance);
                $('#amount-balance-week').html(parseInt(100 - ((for_proc_cost - (for_proc_limit / 4) * week) / (for_proc_limit / 4) * 100)));
            }
            count_table();

            $('.check-cat').on('change', function () {
                checked_week_cat($(this).next().text());
                count_table()
            });

            function checked_week_cat(category) {
                var names = $('.name-cat');
                var name = location.pathname.slice(1,-1);
                for (var i=0;i<names.length;i++) {
                    if (category === names.eq(i).text()) {
                        if (names.eq(i).parent().is(':hidden')) {
                            names.eq(i).parent().show();
                        } else {
                            names.eq(i).parent().hide();
                        }
                        break
                    }
                }
                $.post('/ajax/toggle_category_week_table/', {category: category, name: name})
            }
        }

        week_table();

        function count_for_week_table(week, cost, limit) {

            var limit_for_week = limit / 4;
            var diff = limit_for_week - (cost - limit_for_week * week);
            var proc = 100 - ((cost - limit_for_week * week) / limit_for_week * 100);
            return [diff, proc]
        }


        $('.category-detail').on('click', function () {
            var id = $(this).attr('id');
            var name = $(this).attr('name');
            $.alert({
                title: name,
                content: 'url:/category/' + id + '/',
            });
        })

    }

    stat();

});