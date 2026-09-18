function formatTime(sec) {
    if (!isFinite(sec) || sec < 0) return "0:00";
    var m = Math.floor(sec / 60);
    var s = Math.floor(sec % 60).toString().padStart(2, "0");
    return m + ":" + s;
}

function play(e) {
    var audio = document.getElementById("audio-el");
    var track = document.getElementById("hifi-track");
    var discImg = document.getElementById("hifi-disc-img");
    var discDot = document.getElementById("hifi-disc-dot");
    var name = (e.getAttribute("data-track") || e.textContent || "").trim();
    var cover = e.getAttribute("data-cover");

    audio.src = e.getAttribute("data-audiosrc");
    if (track) track.textContent = name || "Now playing";
    if (discImg && discDot) {
        if (cover) {
            discImg.src = cover;
        } else {
            discImg.classList.add("d-none");
            discDot.classList.remove("d-none");
        }
    }
    audio.load();
    audio.play().catch(function (err) {
        console.error("Playback failed:", err);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    var audio = document.getElementById("audio-el");
    var player = document.getElementById("audioplayer");
    var playBtn = document.getElementById("hifi-playpause");
    var playIcon = document.getElementById("hifi-icon-play");
    var pauseIcon = document.getElementById("hifi-icon-pause");
    var seek = document.getElementById("hifi-seek");
    var currentEl = document.getElementById("hifi-current");
    var durationEl = document.getElementById("hifi-duration");
    var volume = document.getElementById("hifi-volume");
    var discImg = document.getElementById("hifi-disc-img");
    var discDot = document.getElementById("hifi-disc-dot");

    if (discImg && discDot) {
        discImg.addEventListener("load", function () {
            discImg.classList.remove("d-none");
            discDot.classList.add("d-none");
        });
        discImg.addEventListener("error", function () {
            discImg.classList.add("d-none");
            discDot.classList.remove("d-none");
        });
    }

    if (audio && player) {
        var seeking = false;

        audio.addEventListener("play", function () {
            player.classList.add("playing");
            playBtn.setAttribute("aria-label", "Pause");
            playBtn.disabled = false;
            playIcon.classList.add("d-none");
            pauseIcon.classList.remove("d-none");
        });

        audio.addEventListener("pause", function () {
            player.classList.remove("playing");
            playBtn.setAttribute("aria-label", "Play");
            playIcon.classList.remove("d-none");
            pauseIcon.classList.add("d-none");
        });

        audio.addEventListener("loadedmetadata", function () {
            seek.max = audio.duration;
            durationEl.textContent = formatTime(audio.duration);
            playBtn.disabled = false;
        });

        audio.addEventListener("timeupdate", function () {
            if (seeking) return;
            seek.value = audio.currentTime;
            currentEl.textContent = formatTime(audio.currentTime);
        });

        audio.addEventListener("ended", function () {
            player.classList.remove("playing");
        });

        playBtn.addEventListener("click", function () {
            if (audio.paused) {
                audio.play();
            } else {
                audio.pause();
            }
        });

        seek.addEventListener("input", function () {
            seeking = true;
            currentEl.textContent = formatTime(Number(seek.value));
        });

        seek.addEventListener("change", function () {
            audio.currentTime = Number(seek.value);
            seeking = false;
        });

        volume.addEventListener("input", function () {
            audio.volume = Number(volume.value);
        });
    }

    // Active-search dropdown: clear results on outside click / Escape.
    var searchInput = document.getElementById("live-search-input");
    var searchResults = document.getElementById("live-search-results");
    if (searchInput && searchResults) {
        document.addEventListener("click", function (e) {
            if (e.target === searchInput || searchResults.contains(e.target)) return;
            searchResults.innerHTML = "";
        });
        searchInput.addEventListener("keydown", function (e) {
            if (e.key === "Escape") searchResults.innerHTML = "";
        });
    }
});
