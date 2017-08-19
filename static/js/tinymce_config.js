(function(){
    tinymce.init({
        selector: "textarea",
        theme: "modern",
        menubar: false,
        autoresize_max_width: 400,
        autoresize_min_height: 240,
        autoresize_max_height: 240,
        paste_data_images: true,
        plugins: [
            "advlist autolink autoresize lists link image charmap print preview hr anchor pagebreak",
            "searchreplace wordcount visualblocks visualchars code fullscreen",
            "insertdatetime media nonbreaking save table contextmenu directionality",
            "emoticons template paste textcolor colorpicker textpattern codesample autoresize"
        ],
        toolbar1: "insertfile undo redo | bold italic bullist numlist outdent indent | link codesample preview",
        image_advtab: true,
        file_picker_callback: function(callback, value, meta) {
            if (meta.filetype == 'image') {
                $('#upload').trigger('click');
                $('#upload').on('change', function() {
                    var file = this.files[0];
                    var reader = new FileReader();
                    reader.onload = function(e) {
                        callback(e.target.result, {
                            alt: ''
                        });
                    };
                    reader.readAsDataURL(file);
                });
            }
        },
        templates: [{
            title: 'Test template 1',
            content: 'Test 1'
            }, {
            title: 'Test template 2',
            content: 'Test 2'
        }]
    });
})();
