+ function($) {
    'use strict';

    // UPLOAD CLASS DEFINITION
    // ======================

    var dropZone = document.getElementById('drop-zone');
    var uploadForm = document.getElementById('js-upload-form');
    var fileCount = 0;

    var startUpload = function(files) {
        console.log(files)
        for(var index = 0; index < files.length; index++){
            if(fileCount > 0){
                $('.fileList').append('<li>' + files[index].name +  ' </li>');
            }
            else{
                $('.fileList').html('<li>' + files[index].name +  ' </li>');;
            }
            fileCount++;
        };
    }

    uploadForm.addEventListener('submit', function(e) {
        var uploadFiles = document.getElementById('js-upload-files').files;
        e.preventDefault()

        startUpload(uploadFiles)
    })

    dropZone.ondrop = function(e) {
        e.preventDefault();
        this.className = 'upload-drop-zone';

        startUpload(e.dataTransfer.files)
    }

    dropZone.ondragover = function() {
        this.className = 'upload-drop-zone drop';
        return false;
    }

    dropZone.ondragleave = function() {
        this.className = 'upload-drop-zone';
        return false;
    }

}(jQuery);