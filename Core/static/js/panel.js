jQuery(document).ready(function($) {

    function panel() {
        $('.slider-block-panel').on('click', function (event) {
            var elem = $(this).children().eq(0);
            if ($('.input-group').has(event.target).length === 0) {
                if (elem.css('margin-top') === '0px') {
                    elem.animate({'margin-top': '-105px'}, 300)
                } else {
                    elem.animate({'margin-top': '0'}, 300)
                }
            }
        });

        $('body').on('click', '#btn-freemoney', function () {
            var val = $(this).prev().val();
            if (val) {
                $.post('/ajax/correct_free_money/', {value: val});
                location.reload()
            }
        })
    }
    panel();

});