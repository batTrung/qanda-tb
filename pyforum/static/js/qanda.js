$(function () {
    var csrftoken = $("input[name='csrfmiddlewaretoken']").val()

    var toggleSave = function () {
        let el = $(this);
        $.ajax({
            url: el.attr('data-url'),
            type: 'post',
            dataType: 'json',
            data: {
                'csrfmiddlewaretoken': csrftoken,
            },
            success: function (data) {
                el.closest('.qa-vote').html(data.html_votes);
            }
        });
    };

    var toggleVotes = function () {
        let el = $(this);

        $.ajax({
            url: el.attr('data-url'),
            type: 'post',
            dataType: 'json',
            data: {
                'voted': el.hasClass("voted") ? "TRUE" : "",
                'csrfmiddlewaretoken': csrftoken,
            },
            success: function (data) {
                el.closest('.qa-vote').html(data.html_votes);
            }
        });
    }

    var toggleAccept = function () {
        let el = $(this);
        $.ajax({
            url: el.attr('data-url'),
            type: 'post',
            dataType: 'json',
            data: {
                'csrfmiddlewaretoken': csrftoken,
            },
            success: function (data) {
                $(".qa-vote").find('.js-accept-qa').removeClass('text-success');
                el.closest('.qa-vote').html(data.html_votes);
            }
        });
    };

    var loadForm = function () {
        let el = $(this);

        $.ajax({
            url: el.attr('data-url'),
            dataType: 'json',
            type: 'get',
            beforeSend: function () {
                $('#modal-root').modal("show");
            },
            success: function (data) {
                $("#modal-root .modal-content").html(data.html_form)
            }
        })
    }

    var loadLargeForm = function () {
        let el = $(this);

        $.ajax({
            url: el.attr('data-url'),
            dataType: 'json',
            type: 'get',
            beforeSend: function () {
                $('#modal-lg-root').modal("show");
            },
            success: function (data) {
                $("#modal-lg-root .modal-content").html(data.html_form)
            }
        })
    }

    var submitRemoveForm = function () {
        let form = $(this);

        $.ajax({
            url: form.attr('action'),
            dataType: 'json',
            type: form.attr('method'),
            data: form.serialize(),
            success: function (data) {
                $('#modal-root').modal("hide");
                $('.modal-data').find(data.id_item).remove();
            }
        });
        return false;
    }

    var submitRedirectForm = function () {
        let form = $(this);

        $.ajax({
            url: form.attr('action'),
            dataType: 'json',
            type: form.attr('method'),
            data: form.serialize(),
            success: function (data) {
                $('#modal-root').modal("hide");
                window.location = data.redirect_url
            }
        });
        return false;
    }

    var submitReplaceLargeForm = function () {
        let form = $(this);

        $.ajax({
            url: form.attr('action'),
            dataType: 'json',
            type: form.attr('method'),
            data: form.serialize(),
            success: function (data) {
                if (data.is_valid) {
                   $('#modal-lg-root').modal("hide");
                   $('.modal-data').find(data.id_item).replaceWith(data.html_data)
                } else {
                   $('#modal-lg-root .modal-content').html(data.html_form)
                }
            }
        });
        return false;
    }
 

    //  Vote Comment and Quetion
    $('.js-toggle-qa').on('click', 'span.js-vote-qa', toggleVotes)

    // Saved Quetion
    $('.js-toggle-qa').on('click', 'span.js-save-qa', toggleSave)

    // Accept Answer
    $('.js-toggle-qa').on('click', 'span.js-accept-qa', toggleAccept)

    // Create  Comment
    $('form#js-create-comment-form').on('submit', function () {
        let form = $(this);

        $.ajax({
            url: form.attr('action'),
            dataTye: 'json',
            type: form.attr("method"),
            data: form.serialize(),
            success: function (data) {
                if (data.is_valid) {
                    $('#comments').append(data.html_data);
                    form[0].reset();
                }
            }
        });
        return false;
    });

    // Load Form
    $('.modal-block').on('click', '.btn-modal', loadForm)
    $('.modal-block').on('click', '.btn-lg-modal', loadLargeForm)


    // Submit Form and Remove Item
    $('#modal-root').on('submit', 'form#js-comment-delete-form', submitRemoveForm)
    $('#modal-root').on('submit', 'form#js-question-delete-form', submitRedirectForm)

    $('#modal-lg-root').on('submit', 'form#js-comment-update-form', submitReplaceLargeForm)
});
