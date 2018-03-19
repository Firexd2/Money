jQuery(document).ready(function($) {

    var elem = $('.input-shopping-list');
    for (var i=0;i<elem.length;i++) {
        var buffer = elem.eq(i).next();
        buffer.text(elem.eq(i).val());
        elem.eq(i).width(buffer.width());
    }

    $('.delete-item').on('click', function () {
        var id = $('#name-list').val();
        $.post('/ajax/delete_item_shopping_list/' + $(this).closest('.item-list').attr('id') + '/', function () {
            load('shopping_list/' + id + '/')
        })
    });

    $('form').on('click', 'input[name=checkbox]', function () {
        if ($(this).is(':checked')) {
            $(this).prev().val('1');
            $(this).parent().next().css({'text-decoration': 'line-through'})
        } else {
            $(this).prev().val('0');
            $(this).parent().next().css({'text-decoration': 'none'})
        }
        $(this).submit()
    });

    $('form[name=shopping-list]').on('submit', function (e) {
        e.preventDefault();
        var data = $(this).serializeArray();
        $.ajax({
            type: "POST",
            url: '/ajax/new_shopping_list/',
            data: data,
            success: function(data) {}
        });
    });

    $('input[name=price], input[name=count], input[name=name-item]').on('blur', function() {
        $('form').submit()
    });

    $('input[name=name-list]').on('blur', function() {
        var data = $('form[name=shopping-list]').serializeArray();
        $.ajax({
            type: "POST",
            url: '/ajax/new_shopping_list/',
            data: data,
            success: function(data) {
                load('shopping_list/' + data.id + '/')
            }
        });
    });

    // $('form').on('blur', 'input[name=new-price], input[name=new-count], input[name=new-name-item]', function() {
    //     $('form').submit();
    // });

    $('body').unbind().on('click', '.show-item-shop', function () {
        var elem = $(this).next();
        if (elem.is(':hidden')) {
            elem.show(300)
        } else {
            elem.hide(300)
        }
    });

    $('body').on('input', '.input-shopping-list', function() {
        var buffer = $(this).next();
        buffer.text($(this).val());
        $(this).width(buffer.width());
    });

    $('#add-item').on('click', function () {
        var id = $('#name-list').val();
        $.ajax({
            type: "POST",
            url: '/ajax/new_shopping_list/',
            data: {'new-item': '', 'id': id},
            success: function(data) {load('shopping_list/' + data.id + '/')}
        });
    });

    $('select').on('change', function() {
        $(this).prev().val($(this).val());
        $('form').submit()
        
        // или как передать название категории
        //         var data = $('form[name=shopping-list]').serializeArray();
        // $.ajax({
        //     type: "POST",
        //     url: '/ajax/new_shopping_list/',
        //     data: data,
        //     success: function(data) {
        //         load('shopping_list/' + data.id + '/')
        //     }
        // });
    });

    $('#input-cost').on('click', function () {
        var data = $('form[name=shopping-list]').serializeArray();

        var tag = data[2].value;
        var validate = 1;

        var processed_data = {item: ''};
        var content = '<table class="table">' +
            '<thead>' +
            '<tr>' +
            '<td>Товар</td>' +
            '<td>Кол-во</td>' +
            '<td>Цена</td>' +
            '<td>Категория</td>' +
            '</tr>' +
            '</thead>' +
            '<tbody>';

        for (var i=3;i<data.length;i++) {

            if (data[i].name === 'id-item' && data[i+1].value === '1') {
                processed_data.item += data[i].value + ','
            }

            if (data[i].name === 'checkbox') {
                content += '<tr>' +
                    '<td>' + data[i+1].value + '</td>' +
                    '<td>' + data[i+2].value + '</td>' +
                    '<td>' + data[i+3].value + '</td>' +
                    '<td>' + data[i+4].value + '</td>' +
                    '</tr>';
                if (!((data[i+1].value !== '') && (data[i+2].value !== '') && (data[i+3].value !== '') && (data[i+4].value !== ''))) {
                    console.log((data[i+1].value, data[i+2].value, data[i+3].value, data[i+4].value));
                    validate = 0
                }
            }
        }

        content += '</tbody></table>';
        if (validate) {
            $.alert({
                content: content
            })
        } else {
            $.alert({
                type: 'red',
                icon: 'fa fa-exclamation-triangle',
                title: 'Операция отменена',
                content: 'Пожалуйста, внесите все данные в отмеченные продукты.'
            })
        }


        for (var i=0;i<data.length;i++) {
            console.log(data[i])
        }
    })


});