function play(e) {
    var audio = document.getElementById("audioplayer")
    var source = document.getElementById('audiosource');
    console.log("play:" + e.getAttribute('data-audiosrc'))
    source.src = e.getAttribute('data-audiosrc');
    audio.load()
    audio.play();
}