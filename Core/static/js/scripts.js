var arrayTags = [""];	// Массив, который содержит метки
var index = 0;

function removeByValue(arr, val) {
    for(var i=0; i<arr.length; i++) {
        if(arr[i] === val) {
            arr.splice(i, 1);
            break;
        }
    }
    index--;
}

function removeTag(el) {
    tag = $(el).prev().html();
    $(el).parent().remove();
    removeByValue(arrayTags, tag);
    $("#inputTag").focus();
}

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
            var category_id = $(this).attr('id');

            if (!(comment)) {
                comment = 'Без комментария';
            }
            if ((cost) && cost !== '0') {
                table.append('<tr>\n' +
                    '             <td>\n' +
                    '                 <input readonly value="' + comment + '" name="detail-comment-' + category_id + '-' + number + '" style="background: inherit;border: none;width: 150px; height: 18px; cursor: inherit;">' + '\n' +
                    '             </td>\n' +
                    '             <td>\n' +
                    '                 <input readonly name="value-' + category_id + '-' + number + '" class="middle-costs" style="background: inherit;border: none;width: 60px; cursor: inherit;" value="' + cost + '" type="number">\n' +
                    '             </td>\n' +
                    '             <td class="remove-middle-cost">\n' +
                    '                 <i class="fa fa-times remove-cost" style="color: red" aria-hidden="true"></i>\n' +
                    '             </td>\n' +
                    '         </tr>');

                $(this).siblings('.middle-comment').val('');
                $(this).siblings('.middle-cost').val('');
                $(this).parent().hide();
                count_amount();
            }
        });


        $('.caret-hide').on('click', function () {
            var item = $(this).parent().parent().find('.hide-detail');
            if (item.is(':hidden')) {
                item.show()
            } else {
                item.hide()
            }
        });

        function count_amount() {
            var amounts = $('.cost-amount');
            var all_amount = $('#cost-amount');
            var current_amount;
            var counts;
            var all_counts = 0;

            for (var i=0; i<amounts.length; i++) {
                counts = 0;
                current_amount = amounts.eq(i).parent().next().children().children().find('.middle-costs');
                for (var j=0;j<current_amount.length;j++) {
                    if (current_amount.eq(j).val()) {
                        counts += parseInt(current_amount.eq(j).val());
                    }
                }
                amounts.eq(i).val(counts);
                all_counts += counts;
                if (counts) {
                    amounts.eq(i).next().show()
                } else {
                    amounts.eq(i).next().hide()
                }
            }
            all_amount.val(all_counts)
        }

        $('.button-input-cost').on('click', function () {
            $('.input-cost').hide();
            $(this).prev().show()
        });

        $('.table-cost').on('click', '.remove-middle-cost', function () {
            $(this).parent().remove();
            count_amount()
        });

        $('body').click(function (event) {
            if ($('.td-cost').has(event.target).length === 0) {
                $('.input-cost').hide()
            }

            if ($('.td-amount').has(event.target).length === 0) {
                $('.hide-detail').hide()
            }

        });

        function tags() {

            var inputWidth = 16;

            $('.last_tag').on('click', function () {

                var text = $(this).children().text();
                var isExist = jQuery.inArray(text, arrayTags);

                if (isExist === -1) {
                    // Вставляем новую метку (видимый элемент)
                    $(insertTag(text)).insertBefore("#newTagInput");

                    // Вставляем новую метку в массив JavaScript
                    arrayTags[index] = text;
                    index++;
                }
            });

            // Вставка метки в список
            function insertTag(tag) {
                var liEl = '<li id="tag-'+tag+'" class="li_tags">'+
                    '<span href="javascript://" class="a_tag">'+tag+'</span>&nbsp;'+
                    '<a href="" onclick="removeTag(this); return false;"'+
                    ' class="del" id="del_'+tag+'">&times;</strong></a>' +
                    '<input hidden name="tags" value="'+tag+'" type="text">'+
                    '</li>';
                return liEl;
            }

            $("#inputTag").focus().val("");
            $("#hiddenTags").val("");

            // Проверяем нажатие клавиши
            $("#inputTag").keydown(function(event) {
                var textVal = jQuery.trim($(this).val()).toLowerCase();
                var keyCode = event.which;

                // Перемещаемся влево (нажата клавиша влево)
                if (keyCode === 37 && textVal === '') {
                    $("#newTagInput").insertBefore($("#newTagInput").prev());
                    $("#inputTag").focus();
                }

                // Перемещаемся вправо (нажата клавиша вправо)
                if (keyCode === 39 && textVal === '') {
                    $("#newTagInput").insertAfter($("#newTagInput").next());
                    $("#inputTag").focus();
                }

                // Удаляем предыдущую метку (нажата клавиша backspace)
                if (keyCode === 8 && textVal === '') {
                    deletedTag = $("#newTagInput").prev().find(".a_tag").html();
                    removeByValue(arrayTags, deletedTag);
                    $("#newTagInput").prev().remove();
                    $("#inputTag").focus();
                }

                // Удаляем следующую метку (нажата клавиша delete)
                if (keyCode === 46 && textVal === '') {
                    deletedTag = $("#newTagInput").next().find(".a_tag").html();
                    removeByValue(arrayTags, deletedTag);
                    $("#newTagInput").next().remove();
                    $("#inputTag").focus();
                }

                if ((47 < keyCode && keyCode < 106) || (keyCode === 32)) {

                    if (keyCode !== 32) {
                        // Пользователь все еще вводит метку
                        inputWidth = inputWidth + 7;
                        $(this).attr("style", "width:"+inputWidth+"px");
                        $("#newTagInput").attr("style", "width:"+inputWidth+"px");
                    } else if (keyCode === 32 && (textVal !== '')) {
                        // Пользователь создает новую метку
                        var isExist = jQuery.inArray(textVal, arrayTags);

                        if (isExist === -1) {
                            // Вставляем новую метку (видимый элемент)
                            $(insertTag(textVal)).insertBefore("#newTagInput");

                            // Вставляем новую метку в массив JavaScript
                            arrayTags[index] = textVal;
                            index++;
                        }
                        inputWidth = 16;
                        $(this).attr("style", "width:"+inputWidth+"px"); // Ширина элемента будет соответствовать длине ввода
                        $("#newTagInput").attr("style", "width:23px");
                        $(this).val("");
                    } else {
                        $(this).val("");
                    }
                }
            });

            $('#boxTags').on('click', function () {
                $('.input-tags').focus()
            })
        }
        tags()

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