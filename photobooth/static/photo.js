var countdown;

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
    init_camera();
    $('#take-photo').addClass("hidden");
    $('#countdown').removeClass("hidden");
    countdown = 3;
    countDownTick();
}

function handleCountdown() {
    if (countdown >= 1) {
        countDownTick()
    } else {
        take_photo()
    }
}

function init_camera() {
    var data = {
    };
    console.log('Initializing camera: ', data);
    return axios.post('/camera/warmup', data).then(function (response) {
        handleWarmUp(response.data);
    }).catch(function (error) {
        handleError(error);
    });
}

function handleWarmUp(response) {
    console.log("Warmup response: ", response)
}

function take_photo() {
    var data = {
    };
    console.log('Taking a photo: ', data);
    return axios.post('/camera/snap', data).then(function (response) {
        handleSnapResponse(response.data);
    }).catch(function (error) {
        handleError(error);
    });
}

function handleSnapResponse(photo) {
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

installListeners();
