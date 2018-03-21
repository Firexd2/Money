var arrayTags = [""];
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

jQuery(document).ready(function($) {

    function input_cost() {

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

        $('.button-input-cost').on('click', function () {
            var category_id = $(this).attr('id');
            var category_name = $(this).attr('name');
            var table = $(this).parent().next().find('.table-cost');

            $.confirm({
                title: 'Ввод траты в "' + category_name + '"',
                icon: 'fa fa-plus-circle',
                content: '<div style="margin: 0" class="input-cost">\n' +
                '<input placeholder="Сумма" class="form-control middle-cost" type="number">\n' +
                '<input placeholder="Доп. комментарий" class="form-control middle-comment" type="text">\n' +
                '</div>',
                buttons: {
                    Ok: {
                        text: 'Внести',
                        btnClass: 'btn',
                        action: function () {
                            var comment = this.$content.find('.middle-comment').val();
                            var cost = this.$content.find('.middle-cost').val();
                            var number = table.children().length;

                            if (!(comment)) {
                                comment = 'Без комментария';
                            }
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

                                $(this).siblings('.middle-comment').val('');
                                $(this).siblings('.middle-cost').val('');
                                $(this).parent().hide();
                                count_amount();
                            }
                        }
                    },
                    cancel: {
                        text: 'Отмена',
                        action: function () {
                        }
                    }
                }
            });

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

            $("#inputTag").keydown(function(event) {
                var textVal = jQuery.trim($(this).val()).toLowerCase();
                var keyCode = event.which;

                if (keyCode === 37 && textVal === '') {
                    $("#newTagInput").insertBefore($("#newTagInput").prev());
                    $("#inputTag").focus();
                }

                if (keyCode === 39 && textVal === '') {
                    $("#newTagInput").insertAfter($("#newTagInput").next());
                    $("#inputTag").focus();
                }

                if (keyCode === 8 && textVal === '') {
                    deletedTag = $("#newTagInput").prev().find(".a_tag").html();
                    removeByValue(arrayTags, deletedTag);
                    $("#newTagInput").prev().remove();
                    $("#inputTag").focus();
                }

                if (keyCode === 46 && textVal === '') {
                    deletedTag = $("#newTagInput").next().find(".a_tag").html();
                    removeByValue(arrayTags, deletedTag);
                    $("#newTagInput").next().remove();
                    $("#inputTag").focus();
                }

                if ((47 < keyCode && keyCode < 106) || (keyCode === 32)) {

                    if (keyCode !== 32) {
                        inputWidth = inputWidth + 7;
                        $(this).attr("style", "width:"+inputWidth+"px");
                        $("#newTagInput").attr("style", "width:"+inputWidth+"px");
                    } else if (keyCode === 32 && (textVal !== '')) {
                        var isExist = jQuery.inArray(textVal, arrayTags);

                        if (isExist === -1) {
                            $(insertTag(textVal)).insertBefore("#newTagInput");

                            arrayTags[index] = textVal;
                            index++;
                        }
                        inputWidth = 16;
                        $(this).attr("style", "width:"+inputWidth+"px");
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
        tags();

        $('.action-cost').on('click', function () {
            var _this = $(this);
            var id = _this.attr('id');
            var name = location.pathname.slice(1,-1);

            $.confirm({
                title: 'Вы точно хотите удалить трату?',
                type: 'red',
                icon: 'fa fa-exclamation-triangle',
                content: 'Восстановить ее будет невозможно',
                buttons: {
                    Ok: {
                        text: 'Да',
                        btnClass: 'btn',
                        action: function () {
                            $.post('/ajax/delete_cost/', {id:id, name:name});
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
            $(document).ajaxStart(function() { Pace.restart(); });
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
                                        $('#input-cost-button-menu').click();
                                        $.alert({
                                            icon: 'fa fa-check',
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
                    icon: 'fa fa-exclamation-triangle',
                    content: content
                });
            }
        })
    }
    input_cost()
});