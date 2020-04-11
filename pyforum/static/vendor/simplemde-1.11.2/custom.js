function youtube_parser(url) {
    var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#\&\?]*).*/;
    var match = url.match(regExp);
    return (match && match[7].length == 11) ? match[7] : url;
}

var Toolbar_YouTube = {
    name: "YouTube",
    title: "Link YouTube",
    className: "fa fa-youtube js-youtube",
    action: function(editor) {
        var cm = editor.codemirror;

        swal({
            title: "YouTube",
            text: "Nhập link Youtube",
            content: "input",
            animation: "slide-from-top",
            inputPlaceholder: "https://",
            buttons: true,
        }).then(function(inputValue) {
            if (inputValue === false) return false;
            if (inputValue === "") {
                swal("Hãy nhập một đường link!");
                return false;
            }
            var youtubeID = youtube_parser(inputValue);
            cm.replaceSelection('[![Yes](https://img.youtube.com/vi/' + youtubeID + '/0.jpg)](https://www.youtube.com/watch?v=' + youtubeID + ')');
            swal.close();
        });
    }
}

var Toolbar_br = {
    name: "br",
    title: "Xuống dòng",
    className: "fa fa-level-down fa-rotate-90",
    action: function(editor) {
        var cm = editor.codemirror;
        cm.replaceSelection("<br />");
    }
};

var getOptions = function () {
    return {
        spellChecker: false,
        status: true,
        toolbar: [
            "undo",
            "redo",
            "|",
            "bold",
            "italic",
            "heading",
            "|",
            "table",
            "unordered-list",
            "ordered-list",
            "|",
            "link",
            "image",
            Toolbar_YouTube,
            "|",
            "code",
            "horizontal-rule",
            Toolbar_br,
            "|",
            "preview",
            "side-by-side",
            "fullscreen",
            "|",
            "guide",
        ],
    }
}

$(function() {
    $('table').addClass("table");
});