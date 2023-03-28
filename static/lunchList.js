function setLunchBuyer(player) {
  playerName = player.toLowerCase();
  console.log(playerName);
  $(`#${playerName}`).css("color", "#f39003");
}
