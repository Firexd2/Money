jQuery(document).ready(function($) {

    $('form[name=shopping-list]').on('submit', function (e) {
        e.preventDefault();
        var data = $(this).serializeArray();
        $.ajax({
            type: "POST",
            url: '/ajax/new_shopping_list/',
            data: data,
            success: function() {
                alert('ok')
            }
        });

    });


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
        var count = $('.item-list').length + 1;

        $(this).before('<div class="item-list">\n' +
            '               <b>' + count + '.</b> <input type="text" placeholder="Название" maxlength="23" name="name-item" class="input-shopping-list">\n' +
            '               <div class="input-buffer"></div>\n' +
            '               <i class="fa fa-caret-down show-item-shop" aria-hidden="true"></i>\n' +
            '               <div hidden class="info-item-shop">\n' +
            '                   <input style="width: 30px" placeholder="0" name="count" type="number"> <span style="color: gray">шт.</span> <input style="width: 70px" placeholder="0" name="price" type="number"> <span style="color: gray">цена</span>\n' +
            '                </div>\n' +
            '           </div>')

    })

});