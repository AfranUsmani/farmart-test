function uploadFile() {
  var fileInput = document.getElementById('fileInput');
  var file = fileInput.files[0];
  var url = 'http://127.0.0.1:8000/upload/';
  var filename = file.name;
  if (!file) {
    showMessage('Please select a file');
    return;
  }

  fetch(url, {
    method: 'PUT',
    headers: {
      'Content-Type': file.type,
      'X-File-Name': filename
    },
    body: file
  })
    .then(response => {
      if (response.ok) {
        showMessage('Upload successful');
        return response.json();
      } else {
        showMessage('Upload failed');
        throw new Error('Response not OK');
      }
    })
    .then(data => {
      var message = `Uploaded file: ${data.filename}, shortened URL: ${data.url}`;
      showMessage(message);
    })
    .catch(error => {
      showMessage('Error: ' + error.message);
    });
}

function showMessage(message) {
  var messageDiv = document.getElementById('message');
  messageDiv.textContent = message;
}
