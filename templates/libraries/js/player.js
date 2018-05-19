function init() {
    console.log('dallas');
    tag_div = document.getElementById('tag_div');
    tag_div.innerHTML = tag;

    win_icon_div = document.getElementById('q_left');

    wins_div = document.getElementById('win_count');
    wins_div.innerHTML = wins;

    losses_div = document.getElementById('loss_count');
    losses_div.innerHTML = losses;

    percentage_div = document.getElementById('percent_count');
    percentage_div.innerHTML = percentage;

    rank_div = document.getElementById('rank_count');
    rank_div.innerHTML = rank;

    scene_div = document.getElementById('scene_label_div');
    scene_div.innerHTML = "Current Rank in " + scene;

}
