$(function () {
    $(".arrow_up").click(function () {
        $(this).hide()
    });

    $(".arrow_up").on('mousewheel DOMMouseScroll', onMouseScroll);

    function onMouseScroll(e) {
        e.preventDefault();
        var wheel = e.originalEvent.wheelDelta || -e.originalEvent.detail;
        var delta = Math.max(-1, Math.min(1, wheel));
        if (delta < 0) {//向下滚动
            console.log('向下滚动');
        } else {//向上滚动
            console.log('向上滚动');
        }
    }

    // $('.arrow_up').bind('mousewheel', function (event, delta) {
    //     var dir = delta > 0 ? 'mouseUp' : 'mouseDown';
    //     if (dir == 'mouseUp') {
    //         $(this).hide()
    //     } else {
    //         $(this).show()
    //             }
    //     return false;
    // });
})
