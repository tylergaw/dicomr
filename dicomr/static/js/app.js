$(function() {
  function enableUpload() {
    $('.btn-upload').removeClass('btn-hidden');
  }

  function uploadFiles(form, files) {
    form.parent().addClass('is-uploading');

    var data = new FormData(form.get(0));

    $.each(files, function(i, file) {
      data.append('files', file);
    });

    $.ajax({
      url: form.attr('action'),
      type: 'POST',
      data: data,
      dataType: 'json',
      cache: false,
      contentType: false,
      processData: false,
      complete: function() {
        form.parent().removeClass('is-uploading');
      },
      success: function(res) {
        // TODO: This can be smoother later.
        console.log(res);
        // window.location = '/records/' + res.result.id;
      },
      error: function(err) {
        form.parent().addClass('is-error');
        console.log(JSON.parse(err.responseText));
      }
    });
  }

  function initDragon() {
    var form = $('.upload-form');
    var input = $('#upload-input');
    form.on('drag dragstart dragend dragover dragenter dragleave drop', function(event) {
      event.preventDefault();
      event.stopPropagation();
    })
    .on('dragover dragenter', function() {
      form.addClass('is-dragover');
    })
    .on('dragleave dragend drop', function() {
      form.removeClass('is-dragover');
    })
    .on('drop', function(event) {
      droppedFiles = event.originalEvent.dataTransfer.files;

      if (droppedFiles) {
        uploadFiles(form, droppedFiles);
      }
    });

    input.on('change', enableUpload);
  }

  initDragon();
});
