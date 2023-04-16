function setLunchBuyer(player) {
  const Phrases = [
    `You're up, ${player}!`,
    `What's it going to be, ${player}?`,
    `Italian again, ${player}?`,
  ];

  let num = Math.floor(Math.random() * Phrases.length);

  $(`#${player}`)
    .css("color", "#f39003")
    .css("font-size", "3.8rem")
    .text(Phrases[num]);
}
