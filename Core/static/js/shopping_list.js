jQuery(document).ready(function($) {

    var block_action = 1;

    var name_plan = location.pathname.slice(1,-1);

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

    $('form').on('click', 'input[name=checkbox]', function (e) {
        if (block_action) {
            block_action = 0;
            if ($(this).is(':checked')) {
                $(this).prev().val('1');
                $(this).parent().next().css({'text-decoration': 'line-through'})
            } else {
                $(this).prev().val('0');
                $(this).parent().next().css({'text-decoration': 'none'})
            }
            $(this).submit();
            show_button_input_cost()
        } else {
            e.preventDefault()
        }
    });

    $('form[name=shopping-list]').on('submit', function (e) {
        $(document).ajaxStart(function() { Pace.restart(); });
        e.preventDefault();
        var data = $(this).serializeArray();
        $.ajax({
            type: "POST",
            url: '/ajax/new_shopping_list/',
            data: data,
            success: function(data) {block_action = 1}
        });
    });

    $('input[name=price], input[name=count], input[name=name-item]').on('blur', function(e) {
        if (block_action) {
            block_action = 0;
            $('form').submit()
        }
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
        var id = $('#name-list').val();
        var name = $('input[name=name-list]').val();

        var flags = $('input[name=flag]');
        var elems_price = $('input[name=price]');
        var select = $('select');
        var validate = elems_price.length > 0;

        for (var i=0;i<elems_price.length;i++) {
            if (flags.eq(i).val() === '1') {
                if ((!(elems_price.eq(i).val())) || (!(select.eq(i).val()))) {
                    validate = false
                }
            }
        }

        if (validate) {
            $.confirm({
                title: '<span style="font-weight: 100">Внесение трат по списку: </span> ' + name,
                content: 'url: /table_input/' + id + '/',
                buttons: {
                    Ok: {
                        text: 'Ок',
                        btnClass: 'btn',
                        action: function () {
                            $(document).ajaxStart(function() { Pace.restart(); });
                            $.post('/ajax/input_cost_shopping_list/' + id + '/', {name: name_plan} , function () {
                                $.alert({
                                    title: 'Операция прошла успешно',
                                    type: 'green',
                                    icon: 'fa fa-check',
                                    content: 'Траты успешно внесены!'
                                })
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
            $.alert({
                type: 'red',
                title: 'Операция отменена',
                icon: 'fa fa-exclamation-triangle',
                content: 'Чтобы внести список в траты, необходимо у всех отмеченных записей вписать цену и выбрать категорию.'
            })
        }


    });

    function show_button_input_cost() {
        if ($('input[type=checkbox]:checked').length) {
            $('#input-cost').show()
        } else {
            $('#input-cost').hide()
        }
    }
    show_button_input_cost();

    $('#delete').on('click', function () {
        $.post('/ajax/delete_shopping_list/' + $('#name-list').val() + '/', function () {
            load('shopping_list/')
        })
    })

});