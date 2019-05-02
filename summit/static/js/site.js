//
//var progressUrl = "{% url 'celery_progress:task_status' task_id %}";
//document.addEventListener("DOMContentLoaded", function () {
//  CeleryProgressBar.initProgressBar(progressUrl);
//});

//var progressUrl = "{% url 'celery_progress:task_status' task_id %}";
//$(function () {
//  CeleryProgressBar.initProgressBar(progressUrl)
//});

//function updateProgress (progressUrl) {
//    fetch(progressUrl).then(function(response) {
//        response.json().then(function(data) {
//            // update the appropriate UI components
//            setProgress(data.state, data.details);
//            setTimeout(updateProgress, 500, progressUrl);
//        });
//    });
//}
//var progressUrl = '{% url "task_status" task_id %}';  // django template usage
//updateProgress(progressUrl);


// Generate 32 char random uuid
/*function gen_uuid() {
    var uuid = ""
    for (var i=0; i < 32; i++) {
        uuid += Math.floor(Math.random() * 16).toString(16);
    }
    return uuid
}

// Add upload progress for multipart forms.
$(function() {
    $('form[@enctype=multipart/form-data]').submit(function(){
        // Prevent multiple submits
        if ($.data(this, 'submitted')) return false;

        var freq = 1000; // freqency of update in ms
        var uuid = gen_uuid(); // id for this upload so we can fetch progress info.
        var progress_url = '/admin/upload_progress/'; // ajax view serving progress info

        // Append X-Progress-ID uuid form action
        this.action += (this.action.indexOf('?') == -1 ? '?' : '&') + 'X-Progress-ID=' + uuid;

        var $progress = $('<div id="upload-progress" class="upload-progress"></div>').
            appendTo(document.body).append('<div class="progress-container"><span class="progress-info">uploading 0%</span><div class="progress-bar"></div></div>');

        // progress bar position
        $progress.css({
            position: ($.browser.msie && $.browser.version < 7 )? 'absolute' : 'fixed',
            left: '50%', marginLeft: 0-($progress.width()/2), bottom: '20%'
        }).show();

        // Update progress bar
        function update_progress_info() {
            $progress.show();
            $.getJSON(progress_url, {'X-Progress-ID': uuid}, function(data, status){
                if (data) {
                    var progress = parseInt(data.uploaded) / parseInt(data.length);
                    var width = $progress.find('.progress-container').width()
                    var progress_width = width * progress;
                    $progress.find('.progress-bar').width(progress_width);
                    $progress.find('.progress-info').text('uploading ' + parseInt(progress*100) + '%');
                }
                window.setTimeout(update_progress_info, freq);
            });
        };
        window.setTimeout(update_progress_info, freq);

        $.data(this, 'submitted', true); // mark form as submitted.
    });
});*/

//$(function() {
    //console.log("here!");
    // Submit post on submit
    /*$('#project-form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!");  // sanity check
        create_project();
    });

    function create_project() {
        console.log("create project is working!") // sanity check
        console.log($('#project-title').val())
    };*/

    /*function upload(event) {
        event.preventDefault();
        var data = new FormData($('form').get(0));

        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            success: function(data) {
                alert('success');
            }
        });

        return false;
    }

    $(function() {
        $('form').submit(upload);
    });*/

    //$(document).ready(function() {
            // bind 'myForm' and provide a simple callback function
      //      $('#file-upload-form').ajaxForm(function() {
        //        alert("Thank you for your comment!");
          //  });
        //});


    // AJAX for posting
  /*  function create_post() {
        console.log("create post is working!") // sanity check
        $.ajax({
            url : "create/", // the endpoint
            type : "POST", // http method
            data : { the_project : $('#project-text').val() }, // data sent with the post request

            // handle a successful response
            success : function(json) {
                $('#project-text').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };*/

//});