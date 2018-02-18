$(document).ready(function() {

    function onNavbar() {
        if (window.innerWidth >= 768) {
            $('.navbar-default .dropdown').on('mouseover', function(){
                $('.dropdown-toggle', this).next('.dropdown-menu').show();
            }).on('mouseout', function(){
                $('.dropdown-toggle', this).next('.dropdown-menu').hide();
            });
            $('.dropdown-toggle').click(function() {
                if ($(this).next('.dropdown-menu').is(':visible')) {
                    window.location = $(this).attr('href');
                }
            });
        } else {
            $('.navbar-default .dropdown').off('mouseover').off('mouseout');
        }
    }
    $(window).resize(function() {
        onNavbar();
    });
    onNavbar();

    function procent(value) {
        var amount = parseInt($('input[name=income]').val());
        if (amount && value) {
            return Math.round(value / (amount / 100))
        } else {
            if (amount) {
                return 0
            } else {
                return '-- '
            }
        }
    }

    function Total() {
        var n = 0;
        var inputs = $('.cat');
        var amount = parseInt($('input[name=income]').val());
        var tr = $('#total-tr');
        for (var i=0; i<inputs.length; i++) {
            if (parseInt(inputs.eq(i).val())) {
                n += parseInt(inputs.eq(i).val());
            }
        }
        if ($('input[name=income]').val()) {
            $('#p').text(100 - Math.ceil(n / (amount / 100)));
            $('#o').text(amount - n);
            if (n === amount) {
                tr.css({'background': 'rgba(28, 255, 0, 0.35)'})
            } else if (n > amount) {
                tr.css({'background': 'rgba(255, 7, 0, 0.31)'})
            } else {
                tr.css({'background': 'none'})
            }
        } else {
            $('#p').text('-- ');
            $('#o').text('--');
            tr.css({'background': 'none'})
        }
    }

    function MaxProcent() {
        var inputs = $('.cat');
        for (var i=0; i<inputs.length; i++) {
            inputs.eq(i).parent().next().children().text(procent(parseInt(inputs.eq(i).val())))
        }
        Total()
    }

    function OnOffInputs() {
        if ($('input[name=income]').val()) {
            $('.ca').removeAttr("disabled");
            $('.cat').removeAttr("disabled");
        } else {
            $('.ca').attr("disabled", true);
            $('.cat').attr("disabled", true);
        }
    }

    function New() {
        $('input[name=income]').on('input', function () {
            OnOffInputs();

            if ($(this).val()) {
                $('#amount').text($(this).val());
            } else {
                $('#amount').text('--');
            }
            MaxProcent();
        });

        $('body').on('input', '.cat', function () {
            MaxProcent();
        });

        $('#add-category').on('click', function () {
            var tr = $('tr');
            var income = $('input[name=income]').val();
            var disabled = '';
            var proc = '0';
            if (!(income)) {
                disabled = 'disabled';
                proc = '-- '
            }
            tr.eq(tr.length-4).after('<tr>\n' +
                '<td><b>' + (tr.length-3) + '</b></td>\n' +
                '<td><input ' + disabled +  ' name="name-cat' + (tr.length-3) + '" type="text" class="form-control ca" placeholder="Пример: На еду"/></td>\n' +
                '<td><input ' + disabled +  ' name="income' + (tr.length-3) + '" type="number" class="form-control cat"/></td>\n' +
                '<td style="text-align: center"><span>' + proc + '</span>%</td>\n' +
                '</tr>');
        });

        $('#remove-category').on('click', function () {
            $('tr').eq($('tr').length-4).remove();
            Total()
        });

        $('form[name=new]').on('submit', function (e) {

            if ($('#o').text() !== '0') {
                e.preventDefault();
                if (!($('#name-input').val())) {
                    $('#error-form').text(' Вы не ввели название конфигурации')
                } else if ($('#o').text() === '--') {
                    $('#error-form').text(' Вы не ввели и не распределили сумму')
                } else if (parseInt($('#o').text()) > 0) {
                    $('#error-form').text(' У вас остался неиспользованный остаток')
                } else {
                    $('#error-form').text(' Вы превысили лимит вашей суммы')
                }
            }
        });

        $('.icons').on('click', function () {
            var Class = $(this).children().attr('class');
            $('input[name=icon]').val(Class);
            $('.icons').removeClass('active-icons');
            $(this).addClass('active-icons');
        })

    }
    New();



//    ДЕТАЛИЗАЦИЯ КОНФИГУРАЦИИ

    function table() {
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
        var balance_procent = $('.balance-table-procent');
        var item;
        var procent;

        var amount_costs = 0;
        var amount_max = 0;

        for (var q=0;q<category_all.length;q++) {
            item = category_all.eq(q).text().split('/');
            balance.eq(q).html(parseInt(item[1]) - parseInt(item[0]));
            procent = Math.round(100 - parseInt(item[0]) / parseInt(item[1]) * 100);
            balance_procent.eq(q).html(procent + '%');
            amount_costs += parseInt(item[0]);
            amount_max += parseInt(item[1]);

            if (procent > 30) {
                balance.eq(q).css({'color': '#00f100'});
                balance_procent.eq(q).css({'color': '#00f100'});
                category_all.eq(q).css({'color': '#00f100'});
            } else if (procent > 5) {
                balance.eq(q).css({'color': '#ffc211'});
                balance_procent.eq(q).css({'color': '#ffc211'});
                category_all.eq(q).css({'color': '#ffc211'});
            } else {
                balance.eq(q).css({'color': 'red'});
                balance_procent.eq(q).css({'color': 'red'});
                category_all.eq(q).css({'color': 'red'});
            }
        }

        $('#amount-table-1').html(amount_costs);
        $('#amount-table-2').html(amount_max);
        $('#amount-balance').html(amount_max - amount_costs);
        $('#amount-balance-procent').html(Math.round(100 - amount_costs / amount_max * 100) + '%')
    }

    table();

    function input_cost() {
        $('.btn-cost').on('click', function () {
            var comment = $(this).siblings('.middle-comment').val();
            var cost = $(this).siblings('.middle-cost').val();
            var table = $(this).parent().parent().next().find('.table-cost');
            var number = table.children().length;

            table.append('<tr>\n' +
                '             <td>\n' +
                '                 <textarea name="detail-comment-' + number + '" style="background: inherit;border: none;width: 180px; height: 22px; cursor: inherit;">' + comment + '</textarea>\n' +
                '             </td>\n' +
                '             <td>\n' +
                '                 <input name="value-' + number + '" class="" style="background: inherit;border: none;width: 40px; cursor: inherit;" value="' + cost + '" type="number">\n' +
                '             </td>\n' +
                '             <td style="text-align: center">\n' +
                '                 <i class="fa fa-times remove-cost" style="color: red" aria-hidden="true"></i>\n' +
                '             </td>\n' +
                '         </tr>')
        });


        $('.caret-hide').on('click', function () {
            var item = $(this).parent().parent().find('.hide-detail');
            if (item.is(':hidden')) {
                item.show()
            } else {
                item.hide()
            }
        })
    }



    input_cost()

});

                                // <tr>
                                //     <td>
                                //         <textarea style="background: inherit;border: none;width: 180px; height: 22px; cursor: inherit;">Полотенце Максюшке</textarea>
                                //     </td>
                                //     <td>
                                //         <input class="" style="background: inherit;border: none;width: 40px; cursor: inherit;" value="3567" type="number">
                                //     </td>
                                //     <td style="text-align: center">
                                //         <i class="fa fa-times" style="color: red" aria-hidden="true"></i>
                                //     </td>
                                // </tr>