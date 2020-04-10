$(function () {

    // Scroll to load more items
    var page = 1;
    var block_request = false;
    $(window).scroll(function() {
        var margin = $(document).height() - $(window).height() - 200;
        if ($(window).scrollTop() > margin && block_request == false) {
            block_request = true;
            page += 1;
            $.ajax({
                url: '?page=' + page,
                dataType : 'json',
                type: 'get',
                success: function (data) {
                    if (data.is_valid) {
                        block_request = false;
                        $('#js-loading').show();
                        setTimeout(function () {
                            $('#js-tbody-questions').append(data.html_data);
                            let $item = $('#js-tbody-questions').find($(data.id_item))
                            $item.css("background-color", "#daf6fb")
                            setTimeout(function(){
                                $item.css({backgroundColor: ''})
                            }, 1500);
                            $('#js-loading').hide()
                        }, 500);
                    }
                }
            });
        }
    });

    // POPPER
    $('[data-toggle="tooltip"]').tooltip()
    $('[data-toggle="popover"]').popover()


    // Scroll 
    $(".js-scroll").each(function() {
        $(this).on("click", function(t) {
            $("html, body").animate({
                scrollTop: $($(this).attr("href")).offset().top
            }, 700)
        })
    });

});