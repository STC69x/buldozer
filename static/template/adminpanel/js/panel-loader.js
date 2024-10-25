$(document).ready(function () {
    var loading = '<center style="margin-top:2rem"><div class="loader">Загрузка...</div></center><br>';
    $(".form1").click(function () {
        $(".panel-data").html(loading);
        $(".panel-data").load('/pages/form1.html');
    });

    $(".table1").click(function () {
        $(".panel-data").html(loading);
        $(".panel-data").load('/pages/table1.html');
    });
});

function start() {
    if ($("#resultdata").html() === "") {
        $("#resultdata").html("")
    }
    $('#loadingdata').html('<code>Processing Request...</code>');
    $("input").attr("disabled", "disabled");
    $("select").attr("disabled", "disabled");
    $("button").attr("disabled", "disabled");
}

function finish() {
    $('#loadingdata').html("");
    $("input").removeAttr("disabled");
    $("select").removeAttr("disabled");
    $("button").removeAttr("disabled");
}
