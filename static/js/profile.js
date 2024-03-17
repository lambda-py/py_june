document.getElementById('id_avatar').addEventListener('change', function() {
    var file = this.files[0];
    var reader = new FileReader();
    
    reader.onload = function(e) {
        document.getElementById('avatar-image').src = e.target.result;
    };
    
    reader.readAsDataURL(file);
});