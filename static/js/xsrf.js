function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    xsrfstring = getCookie('_xsrf');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            switch (settings.type) {
                case "GET":
                    settings.url += "&_xsrf=" + xsrfstring;
                    break;
                case "POST":
                    settings.data += "&_xsrf=" + xsrfstring;
                    break;
            }
        }
    });
});

