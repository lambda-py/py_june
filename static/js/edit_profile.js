document.getElementById('id_avatar').addEventListener('change', function() {
    let file = this.files[0];
    let reader = new FileReader();

    reader.onload = function(e) {
        document.getElementById('avatar-image').src = e.target.result;
    };

    reader.readAsDataURL(file);
});