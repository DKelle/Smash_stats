function init() {
    console.log('dallas');
    tag_div = document.getElementById('tag_div');
    tag_div.innerHTML = tag;

    wins_div = document.getElementById('q1_div');
    wins_div.innerHTML = wins;

    losses_div = document.getElementById('q2_div');
    losses_div.innerHTML = losses;

    percentage_div = document.getElementById('q3_div');
    percentage_div.innerHTML = percentage;
}
