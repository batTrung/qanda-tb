$(function () {
    var options = getOptions();
    var sml = new SimpleMDE({
            element: $('textarea')[0],
            options
        });

    $("form").attr('novalidate', 'novalidate');
    var csrftoken = $("input[name='csrfmiddlewaretoken']").val();

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
                $('#answers').find('.color-accept').removeClass('bg-light');
                el.closest('.qa-vote').html(data.html_votes);
                if (data.id_item) {
                    $('#answers').find(data.id_item).find('.color-accept').addClass('bg-light');
                }
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
                   $('.modal-data').find(data.id_item).replaceWith(data.html_data);
                   $('pre > code').each(function() {
                         hljs.highlightBlock(this);
                    });
                } else {
                   $('#modal-lg-root .modal-content').html(data.html_form)
                }
            }
        });
        return false;
    }
     
    var submitReplyForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr('action'),
            dataType: 'json',
            type: form.attr('method'),
            data: form.serialize(),
            success: function (data) {
                if (data.is_valid) {
                    form.closest('.qa-reply').after(data.html_data);
                    form[0].reset();
                }
            }
        });
        return false;
    }

    var loadMore = function (el, page) {
        $.ajax({
            url: el.attr('data-url')+ '?page=' + page,
            dataType: 'json',
            type: 'get',
            success: function (data) {
                if (data.is_valid) {
                    el.before(data.html_data);
                    page += 1;
                } else {
                    el.html('')
                }
            }
        });
        return false;
    }

    //  Vote Answer and Quetion
    $('.js-toggle-qa').on('click', 'span.js-vote-qa', toggleVotes)

    // Saved Quetion
    $('.js-toggle-qa').on('click', 'span.js-save-qa', toggleSave)

    // Accept Answer
    $('.js-toggle-qa').on('click', 'span.js-accept-qa', toggleAccept)

    // Create  Answer
    $('form#js-create-answer-form').on('submit', function () {
        let form = $(this);

        $.ajax({
            url: form.attr('action'),
            dataTye: 'json',
            type: form.attr("method"),
            data: form.serialize(),
            success: function (data) {
                if (data.is_valid) {
                    $('#answers').append(data.html_data);
                    form[0].reset();
                    const $codemirror = $('textarea[name="content"]').nextAll('.CodeMirror')[0].CodeMirror;
                    $codemirror.getDoc().setValue("");
                    $('pre > code').each(function() {
                         hljs.highlightBlock(this);
                    });
                }
            }
        });
        return false;
    });

    // Load Form
    $('.modal-block').on('click', '.btn-modal', loadForm)
    $('.modal-block').on('click', '.btn-lg-modal', loadLargeForm)


    // Submit Form and Remove Item
    $('#modal-root').on('submit', 'form#js-answer-delete-form', submitRemoveForm)
    $('#modal-root').on('submit', 'form#js-question-delete-form', submitRedirectForm)

    $('#modal-lg-root').on('submit', 'form#js-answer-update-form', submitReplaceLargeForm)

    // CRUD Reply
    $('#answers').on('submit', 'form.js-create-reply-form', submitReplyForm)

    var pageAnswer = 2;
    var pageReply = 2;

    $('#js-load-more-answers').on('click', function () {
        let el = $(this);

        $.ajax({
            url: el.attr('data-url')+ '?page=' + pageAnswer,
            dataType: 'json',
            type: 'get',
            success: function (data) {
                if (data.is_valid) {
                    $('#answers').append(data.html_data);
                    pageAnswer += 1;
                } else {
                    el.hide();
                }
            }
        });
        return false;
    });

    $('#answers').on('click', '#js-load-more-replies', function () {
        let el = $(this);
        
        $.ajax({
            url: el.attr('data-url')+ '?page=' + pageReply,
            dataType: 'json',
            type: 'get',
            success: function (data) {
                if (data.is_valid) {
                    el.before(data.html_data);
                    pageReply += 1;
                } else {
                    el.hide();
                }
            }
        });
        return false;
    });

});
