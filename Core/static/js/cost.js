function cost() {

    // глобальные переменные, нужные для манипуляций ввода трат в функциях, которые не относятся к таблице
    var category_id;
    var table;

    function input_cost() {

        $('.caret-hide').on('click', function () {
            var item = $(this).parent().parent().find('.hide-detail');
            if (item.is(':hidden')) {
                item.show()
            } else {
                item.hide()
            }
        });

        function add_cost(comment, cost) {
            var number = table.children().length;

            if (cost === undefined) {
                comment = $('.middle-comment').val();
                cost = $('.middle-cost').val();
            }
            if (!(comment)) {
                comment = 'Без комментария';
            }

            if (comment && cost) {
                if ((cost) && cost !== '0') {
                    table.append('<tr>\n' +
                        '<td>\n' +
                        '<input readonly class="comment-cost" value="' + comment + '" name="detail-comment-' + category_id + '-' + number + '" style="background: inherit;border: none;width: 150px; height: 18px; cursor: inherit;">' + '\n' +
                        '</td>\n' +
                        '<td>\n' +
                        '<input readonly name="value-' + category_id + '-' + number + '" class="middle-costs value-cost" style="background: inherit;border: none;width: 60px; cursor: inherit;" value="' + cost + '" type="number">\n' +
                        '</td>\n' +
                        '<td class="remove-middle-cost">\n' +
                        '<i class="fa fa-times remove-cost" style="color: red" aria-hidden="true"></i>\n' +
                        '</td>\n' +
                        '</tr>');

                    $('.middle-comment').val('');
                    $('.middle-cost').val('');
                    // this_.parent().hide();
                    count_amount();
                }
            }
        }

        function count_amount() {
            var amounts = $('.cost-amount');
            var all_amount = $('#cost-amount');
            var current_amount;
            var counts;
            var all_counts = 0;

            for (var i = 0; i < amounts.length; i++) {
                counts = 0;
                current_amount = amounts.eq(i).parent().next().children().children().find('.middle-costs');
                for (var j = 0; j < current_amount.length; j++) {
                    if (current_amount.eq(j).val()) {
                        counts += parseInt(current_amount.eq(j).val());
                    }
                }
                amounts.eq(i).text(counts);
                all_counts += counts;
                if (counts) {
                    amounts.eq(i).next().show()
                } else {
                    amounts.eq(i).next().hide()
                }
            }
            all_amount.text(all_counts)
        }

        $(document).on('click', '.preloaded-cost', function () {
            add_cost($(this).children().eq(0).text(), $(this).children().eq(1).text());
            // удаляем из текущего списка элемент и из общего, который скрытен
            $('#list-preloaded-cost').children().eq($(this).index()).remove();
            if ($('#list-preloaded-cost').children().length === 0) {
                $('#preloaded-info').remove()
            }
            $(this).remove()
        });

        function templateTablePreloadedCosts(content) {
            return '<div id="preloaded-info"><div class="input-cost-title">Не распределенные предзагруженные траты:</div>' +
                '<table class="preloaded-table">' +
                '  <tbody>' + content + '  </tbody>' +
                '</table></div>'
        }

        $('.button-input-cost').on('click', function () {
            category_id = $(this).attr('id');
            var category_name = $(this).attr('name');
            table = $(this).parent().next().find('.table-cost');
            var preloaded_costs = $('#list-preloaded-cost').children();

            content = '<div class="input-cost-title">Ручной ввод:</div>' +
                '<div style="margin: 0" class="input-cost">\n' +
                '<input placeholder="Сумма" class="form-control middle-cost" type="number">\n' +
                '<input placeholder="Доп. комментарий" class="form-control middle-comment" type="text">\n' +
                '</div>';

            if (preloaded_costs.length > 0) {
                var preloaded_content = '';
                var data;
                for (var i = 0; i < preloaded_costs.length; i++) {
                    data = preloaded_costs.eq(i).text().split('|');
                    preloaded_content += '<tr class="preloaded-cost"><td>' + data[0] + '</td><td>' + data[1] + '</td></tr>'
                }
                content = templateTablePreloadedCosts(preloaded_content) + content
            }

            $.confirm({
                title: category_name,
                content: content,
                buttons: {
                    ok_and_go_on: {
                        text: 'Ок и продолжить',
                        btnClass: 'btn',
                        action: function () {
                            add_cost();
                            return false
                        }
                    },
                    ok: {
                        text: 'Ок',
                        btnClass: 'btn',
                        action: function () {
                            add_cost()
                        }
                    }
                }
            })
        });

        $('#button-preloaded-costs').on('click', function () {
            $.confirm({
                title: 'Предзагрузка трат',
                content:
                '<div id="preloaded-info">' +
                '<div style="margin: 0" class="input-cost">\n' +
                '<div class="input-cost-title">Расшифруйте QR код чека:</div>\n' +
                '<input class="form-control str-qr-code" name="str-qr-code" placeholder="Данные QR кода" type="text">\n' +
                '<div class="input-cost-title">Или введите данные чека в ручную:</div>\n' +
                '<input class="form-control" name="date" placeholder="Дата" type="datetime-local">\n' +
                '<input class="form-control" name="summa" placeholder="Сумма (с копейками через точку)" type="text">\n' +
                '<input class="form-control" name="fn" placeholder="ФН" type="text">\n' +
                '<input class="form-control" name="fd" placeholder="ФД" type="text">\n' +
                '<input class="form-control" name="fp" placeholder="ФП" type="text">\n' +
                '</div></div>',
                buttons: {
                    ok: {
                        text: 'Загрузить',
                        btnClass: 'btn',
                        action: function () {
                            const str_qr_code = $('input[name=str-qr-code]').val();
                            var data;
                            if (str_qr_code) {
                                data = {'qr': str_qr_code}
                            } else {
                                data = {
                                    'date': $('input[name=date]').val(),
                                    'summa': $('input[name=summa]').val(),
                                    'fn': $('input[name=fn]').val(),
                                    'fd': $('input[name=fd]').val(),
                                    'fp': $('input[name=fp]').val()
                                }
                            }
                            var url = '/ajax/get-preloaded-costs/';
                            $.ajax({
                                type: "POST",
                                url: url,
                                data: data,
                                success: function (data) {
                                    if (!('traceback' in data)) {
                                        const container_costs = $('#list-preloaded-cost');
                                        container_costs.children().remove();
                                        for (var i = 0; i < data.length; i++) {
                                            container_costs.append('<span>' + data[i]['comment'] + '|' + data[i]['sum'] + '</span>')
                                        }
                                        $.alert({
                                            type: 'green',
                                            title: '<b>Операция выполнена!</b>',
                                            content: 'Траты предзагружены.'
                                        })
                                    } else {
                                        $.alert({
                                            type: 'red',
                                            title: '<b>Ошибка</b>',
                                            content: data['traceback']
                                        })
                                    }
                                }
                            })
                        }
                    },
                    cancel: {
                        text: 'Отмена',
                        action: function () {
                        }
                    }
                }
            })
        });

        $('.table-cost').on('click', '.remove-middle-cost', function () {
            $(this).parent().remove();
            count_amount()
        });

        $('body').click(function (event) {
            if ($('.td-amount').has(event.target).length === 0) {
                $('.hide-detail').hide()
            }
        });

        function tags() {

            var inputWidth = 16;

            $('.last_tag').on('click', function () {

                var text = $(this).text();
                var isExist = jQuery.inArray(text, arrayTags);

                if (isExist === -1) {
                    $(insertTag(text)).insertBefore("#newTagInput");

                    arrayTags[index] = text;
                    index++;
                }
            });

            function insertTag(tag) {
                var liEl = '<li id="tag-' + tag + '" class="li_tags">' +
                    '<span href="javascript://" class="a_tag">' + tag + '</span>&nbsp;' +
                    '<a onclick="removeTag(this); return false;"' +
                    ' class="del" id="del_' + tag + '">&times;</strong></a>' +
                    '<input hidden name="tags" value="' + tag + '" type="text">' +
                    '</li>';
                return liEl;
            }

            $("#inputTag").focus().val("");
            $("#hiddenTags").val("");

            $("#inputTag").on('input', function () {

                var textVal = jQuery.trim($(this).val()).toLowerCase();
                var inputWidth = textVal.length * 8;

                $(this).attr("style", "width:" + inputWidth + "px");
                $("#newTagInput").attr("style", "width:" + inputWidth + "px");

            });

            $('#boxTags').on('click', function () {
                $('.input-tags').focus()
            });

            var touchtime = 0;
            $('#boxTags').on("click", function () {
                if (((new Date().getTime()) - touchtime) < 500) {

                    var textVal = jQuery.trim($("#inputTag").val()).toLowerCase();
                    var isExist = jQuery.inArray(textVal, arrayTags);
                    if (isExist === -1) {
                        $(insertTag(textVal)).insertBefore("#newTagInput");
                        arrayTags[index] = textVal;
                        index++;
                    }
                    inputWidth = 16;
                    $("#inputTag").attr("style", "width:" + inputWidth + "px");
                    $("#newTagInput").attr("style", "width:23px");
                    $("#inputTag").val("");
                }
                touchtime = new Date().getTime();
            });


        }

        tags();

        $('.action-cost').on('click', function () {
            var _this = $(this);
            var id = _this.attr('id');
            var name = location.pathname.slice(1, -1);

            $.confirm({
                title: 'Подтверждение',
                type: 'red',
                content: 'Вы точно хотите удалить трату? Восстановить ее будет невозможно',
                buttons: {
                    Ok: {
                        text: 'Да',
                        btnClass: 'btn',
                        action: function () {
                            $.post('/ajax/delete_cost/', {id: id, name: name});
                            _this.remove()
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

        $('#submit-cost').on('click', function () {
            $(document).ajaxStart(function () {
                Pace.restart();
            });
            if ($('.value-cost').length && $('input[name=tags]').length) {

                $.confirm({
                    title: 'Подтвердите ввод',
                    content: function () {
                        var values = $('.value-cost'); // инпуты с водом
                        var comments = $('.comment-cost');
                        var html = '<table class="table">\n' +
                            '<thead>\n' +
                            '<tr>\n' +
                            '<th>Сумма</th>\n' +
                            '<th>Комментарий</th>\n' +
                            '</tr>\n' +
                            '</thead>\n' +
                            '<tbody style="text-align: left">';
                        var amount = 0;
                        var value;
                        var comment;

                        for (var i = 0; i < values.length; i++) {
                            value = values.eq(i).val();
                            comment = comments.eq(i).val();
                            amount += parseInt(value);
                            html += '<tr>\n' +
                                '<td>' + value + ' р.</td>\n' +
                                '<td>' + comment + '</td>\n' +
                                '</tr>'
                        }
                        return html + '</tbody>\n' +
                            '</table> ' +
                            '<div style="text-align: left"><h4>Общая сумма <b>' + amount + '</b> р.</h4></div>'

                    },
                    buttons: {
                        Ok: {
                            btnClass: 'btn',
                            text: 'Ок',
                            action: function () {
                                var data = $('form[name=cost]').serializeArray();
                                var url = '/ajax/input_cost/';
                                $.ajax({
                                    type: "POST",
                                    url: url,
                                    data: data,
                                    success: function () {
                                        load('stat/');
                                        $.alert({
                                            type: 'green',
                                            title: '<b>Операция выполнена!</b>',
                                            content: 'Траты успешно внесены'
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
            } else {
                var content = '';
                if (!($('input[name=tags]').length)) {
                    content = 'Вы не указали ни одной метки'
                } else {
                    content = 'Вы не ввели ни одной траты'
                }
                $.alert({
                    title: 'Операция отменена',
                    type: 'orange',
                    content: content
                });
            }
        })
    }

    input_cost()
}

window.scriptsContent = cost();