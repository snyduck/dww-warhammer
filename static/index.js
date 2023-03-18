function playSound() {
    let sound = new Audio(("{{ url_for('static', filename='audio/wrong.mp3') }}"))
    sound.play()
}

$("span").on("click", function () {
    $("#lmaohiddentext").text("More like SNOREHAMMER");
    playSound()
})