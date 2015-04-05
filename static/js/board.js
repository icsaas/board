
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
    runreport();
});

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function runreport() {
    oTable = $('#ranktable').dataTable({
        "bProcessing": true,
        "bDestory":true,
        "bAutoWidth":false,
        "bSortable": true,
        "bjQueryUI": true,
        "sAjaxSource": "/",
        "aoColumns": [
            { "mData": "排名" },
            { "mData": "参赛者" },
            { "mData": "所在组织" },
            { "mData": "评分" },
            { "mData": "准确率" },
            { "mData": "召回率"},
            { "mData": "最好成绩提交日"},
        ],
        "fnServerParams": function (aoData) {
        },
        "fnServerData": function (sSource, aoData, fnCallback) {
            aoData.push( { "_xsrf": getCookie('_xsrf')} );
            $.ajax({
                "dataType": 'json',
                "type": "POST",
                "url": sSource,
                "data": aoData,
                "success": fnCallback
            });
        }
   });
}