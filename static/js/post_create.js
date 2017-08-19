$(document).on(function () {
    $(".postCategory").click(function () {
       $("#formDropdownBtn").text($(this).text());
    });
    $("#postCreateForm").submit(function(){
        var csrftoken = $.cookie('csrftoken');
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        if ($('#postAnonymous').is(":checked")){
            var anonymous = '1';
        } else {
            var anonymous = '0';
        }
        console.log(data);
        console.log(url);
        $.ajax({
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            data: {
                category_title: $('#formDropdownDtn').text(),
                title: $("#postTitle").text(),
                content: $("#postContent").text(),
                tags: $("#postTags").text(),
                public: $('input[name="public"]:checked').val(),
                anonymous: '0'
            },
            dataType: 'json',
            success: function (data) {
                console.log("success");
                console.log(data);
            }
        });
    });
});