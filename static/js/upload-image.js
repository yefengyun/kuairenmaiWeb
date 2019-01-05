var imageUploadInput = document.querySelector('.upload-image__input');
var imageUploadPreview = document.querySelector('.upload-image__preview');

var fileReader = new FileReader();

if (!window.fileReader) {
  alert('您的浏览器不支持文件上传，请升级到最新版Chrome浏览器');
}


fileReader.addEventListener('load', function(event) {
  imageUploadPreview.src = event.target.result;
});

imageUploadInput.addEventListener('change', function(event) {
  fileReader.readAsDataURL(event.target.files[0]);
});

