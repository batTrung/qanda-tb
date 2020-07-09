$(function () {
    var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    
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


    // Avoid dropdown menu close on click inside
    $('.notifications.dropdown-menu').on('click', function (e) {
        e.stopPropagation();
    })

    var content_actions = $('.notifications .content'),
        actions = $('.notifications .actions'),
        page_action = 2,
        request_action = false;


    // Click Notification Icon
    $('#myNotification').on('click', function () {
        var el = $(this);

        $.ajax({
            url: el.attr('data-url'),
            dataType: 'json',
            type: 'get',
            success: function (data) {
                if (data.is_valid) {
                    $('.notifications').find('.actions').html(data.html_data);
                    $('.count-actions').html('');
                }
            }
        });
    });


    // Scroll content actions
    content_actions.on('scroll', function () {
        let el = $(this);

        let isLoadMore = el.height() + el.scrollTop() > actions.height();
        if (isLoadMore && !request_action) {
            request_action = true;
            $.ajax({
                url: el.attr('data-url') + '?page=' + page_action,
                dataType: 'json',
                type: 'get',
                success: function (data) {
                    if (data.is_valid) {
                        page_action += 1;
                        request_action = true;
                        $('.notifications').find('.actions').append(data.html_data);
                        $('.count-actions').html('');
                    }
                }
            });
            setTimeout(function(){request_action=false}, 1000);
        }
    });


    $('.notifications').on('click', '.js-mark-read', function () {
        let el = $(this);

        $.ajax({
            url: el.attr('data-url'),
            dataType: 'json',
            type: 'post',
            data: {
                'csrfmiddlewaretoken': csrftoken,
            },
            success: function (data) {
                page_action = 2;
                $('.notifications').find('.actions').html(data.html_data);
            }
        });
    });


    $('.notifications').on('click', '.actions a', function () {
        let el = $(this);

        $.ajax({
            url: el.attr('data-url'),
            dataType: 'json',
            type: 'post',
            data: {
                'csrfmiddlewaretoken': csrftoken,
            },
            success: function (data) {
                el.removeClass('seen-color');
                if (data.is_valid) {
                    window.location = data.redirect_url;
                    window.location.reload()
                }
            }
        });

        return false;
    })

    $('#js-dropdown-event').on('hidden.bs.dropdown', function () {
          page_action = 2;
          $('.notifications').find('.actions').html('');

    });


});