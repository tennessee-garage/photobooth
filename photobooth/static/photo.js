var countdown;
var set_id;

function countDownTick() {
    $('#counter').text(countdown);
    countdown--;

    setTimeout(
        function(){
            handleCountdown();
        },
        1000
    );
}

function startCountdown() {
    $('#take-photo').addClass("hidden");
    $('#countdown').removeClass("hidden");
    countdown = 3;
    countDownTick();
}

function handleCountdown() {
    if (countdown >= 1) {
        countDownTick()
    } else {
        $('#counter').text('smile!');
        take_photo()
    }
}

function handleWarmUp(response) {
    console.log("Warmup response: ", response)
}

function createPhotosetAndRedirect(layout_id) {
    var data = "layout_id=1";
    console.log('Creating a photoset: ', data);
    return axios.post('/api/photo_set', data).then(function (response) {
        handleCreatePhotosetAndRedirectResponse(response.data);
    }).catch(function (error) {
        handleError(error);
    });
}

function handleCreatePhotosetAndRedirectResponse(photoset) {
    console.log("Photoset response: ", photoset);
    urlParams = new URLSearchParams(location.search);
    urlParams.set('set_id', photoset['id']);

    href = location.pathname + '?' + urlParams.toString();
    window.location.replace(href);
}

function take_photo() {
    var data = "set_id=" + set_id
    console.log('Taking a photo: ', data);
    return axios.post('/api/photo', data).then(function (response) {
        handlePhotoResponse(response.data);
    }).catch(function (error) {
        handleError(error);
    });
}

function handlePhotoResponse(photo) {
    console.log("Photo response: ", photo)
    $('#countdown').addClass("hidden");
    $('#preview-pane').removeClass("hidden")
    $('#preview').attr("src", photo.photo_url);
}

function installListeners() {
    console.log("Installing listeners ...");
    $('#take-photo').click(function () {
        console.log("Taking a photo");
        startCountdown();
    });
}

function handleError(error) {
    console.error(error);
}

$( document ).ready(function() {
    urlParams = new URLSearchParams(location.search);
    set_id = urlParams.get('set_id');
    if (!(set_id > 0)) {
        createPhotosetAndRedirect();
    }

    installListeners();
});