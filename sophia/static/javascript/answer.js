'use strict';

/* globals MediaRecorder */

let mediaRecorder;
let recordedBlobs;

const errorMsgElement = document.querySelector('span#errorMsg');
const recordedVideo = document.querySelector('video#gum');
const recordButton = document.querySelector('button#record');
const playButton = document.querySelector('button#play');
const uploadButton = document.querySelector('button#upload');
const startButton = document.querySelector('button#start');
const nextButton = document.querySelector('button#next');


startButton.addEventListener('click', async () => {
    const hasEchoCancellation = document.querySelector('#echoCancellation').checked;
    const constraints = {
        audio: {
            echoCancellation: { exact: hasEchoCancellation }
        },
        video: {
            width: 2040, height: 1080
        }
    };
    console.log('Using media constraints:', constraints);
    await init(constraints);
});



//record button
recordButton.addEventListener('click', () => {

    if (recordButton.textContent === 'Record') {
        alert("Recording is started")
        startRecording();
    } else {
        alert("Your answer is recorded review your answer and then submit it!")
        stopRecording()
        recordButton.textContent = 'Record'
        playButton.disabled = false
        uploadButton.disabled = false
    }
});

//play button
playButton.addEventListener('click', () => {
    startButton.disabled = true
    recordButton.disabled = true
    const superBuffer = new Blob(recordedBlobs, { type: 'video/webm' });
    recordedVideo.src = null;
    recordedVideo.srcObject = null;
    recordedVideo.src = window.URL.createObjectURL(superBuffer);
    recordedVideo.controls = true;
    recordedVideo.play();
    startButton.disabled = true
    recordButton.disabled = true
    gum.disabled = true
    setTimeout(myFunction, 5000);
    uploadButton.disabled = false
});

//csrf
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
let ass_name = document.getElementById("assname").innerHTML;
//upload func
uploadButton.addEventListener('click', () => {
    const blob = new Blob(recordedBlobs, { type: 'video/mp4' });
    const fd = new FormData();
    fd.append('data', blob);
    fd.append('ass_name', ass_name)
    $.ajax({
        type: 'POST',
        url: 'fileUpload/',
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        mode: "same-origin",
        beforeSend: function () {
            playButton.disabled = true
            uploadButton.disabled = true
            startButton.disabled = true
            recordButton.disabled = true
        },
        success: function () {
            alert("Your assessment is submited successfully! Exit The Assessment.")
            document.getElementById("exit").style.visibility = "visible";
        },
        error: function () { // if error occured
            alert("Error occured.please try again");
            uploadButton.disabled = false

        },
        complete: function () {

            if (response == 'complete')
                playButton.disabled = true
                uploadButton.disabled = true
                startButton.disabled = true
                recordButton.disabled = true;
        },

        data: fd,
        processData: false,
        contentType: false
    })


});

//handleDataAvailable
function handleDataAvailable(event) {
    console.log('handleDataAvailable', event);
    if (event.data && event.data.size > 0) {
        recordedBlobs.push(event.data);
    }
}

//startRecording
function startRecording() {
    recordedBlobs = []
    let options = {
        MimeType: 'video/webm;codecs=vp9,opus'
    }
    try {
        mediaRecorder = new MediaRecorder(window.stream, options)



    } catch (e) {
        console.error('Exception while creating MediaRecorder:', e);
        errorMsgElement.innerHTML = `Exception while creating MediaRecorder: ${JSON.stringify(e)}`
        return;
    }

    console.log('Created MediaRecorder', mediaRecorder, 'with options', options);
    recordButton.textContent = 'Stop';
    playButton.disabled = true;
    uploadButton.disabled = true;
    mediaRecorder.onstop = (event) => {
        console.log('Recorder stopped: ', event);
        console.log('Recorded Blobs: ', recordedBlobs);
    };
    mediaRecorder.ondataavailable = handleDataAvailable;
    mediaRecorder.start();
    console.log('MediaRecorder started', mediaRecorder);
}

//stopRecording
function stopRecording() {
    mediaRecorder.stop();
}

function handleSuccess(stream) {
    recordButton.disabled = false;
    console.log('getUserMedia() got stream:', stream);
    window.stream = stream;

    const gumVideo = document.querySelector('video#gum');
    gumVideo.srcObject = stream;
}

async function init(constraints) {
    try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        handleSuccess(stream);
    } catch (e) {
        console.error('navigator.getUserMedia error:', e);
        errorMsgElement.innerHTML = `navigator.getUserMedia error:${e.toString()}`;
    }
}

// next button

var visibleDiv = 0;
function showDiv() {
    $(".grid").hide();
    $(".grid:eq(" + visibleDiv + ")").show();
}
showDiv()
function showNext() {
    if (visibleDiv == $(".grid").length - 1) {
        visibleDiv = 0;
    }
    else {
        visibleDiv++;
    }
    showDiv();
}
function showPrev() {
    if (visibleDiv == 0) {
        visibleDiv = $(".grid").length - 1
    }
    else {
        visibleDiv--;
    }
    showDiv();
}

