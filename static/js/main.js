$(document).ready(function(){
    $('.ajaxCall').click(function () {
        $("#filterDropdownBtn").text($(this).text());
        var url = '/posts/category/'+$(this).attr("value");
        $.ajax({
            type: 'GET',
            url: url,
            success: function (data) {
                // console.log("success");
                $("#postContent").html(data)
            }
        });
    });
});