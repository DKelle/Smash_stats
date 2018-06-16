function init() {
    tag_div = document.getElementById('top_div');
	tag_div.innerHTML = 'Rankings for ' + capitalize_first_letters(scene) + ' on ' + date;

	create_table(JSON.parse(prev_ranks), JSON.parse(cur_ranks));
	//ranks_data = get_ranks_data(scene, date);

}

function create_table(prev, cur) {
	//Put this data in the table
	table = document.getElementById('ranks_table');

	// We need to sort this by ranks
	sorted_results = {}
	for (var tag in cur) {
		// check if the property/tag is defined in the object itself, not in parent
		if (cur.hasOwnProperty(tag)) {           
			//Add this tag to the table
			rank = cur[tag];
			var delta = 0;
			if (prev.hasOwnProperty(tag)) {
				var old_rank = prev[tag];
				delta = old_rank - rank;	
			}
			col_data = [tag, rank, delta];
			sorted_results[rank] = col_data;
		}
	}
    var thead = document.createElement('thead');
    add_table_rows(table, sorted_results);
}

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function add_table_rows(table, cols) {

    var up_glyph = "glyphicon glyphicon-chevron-up"
    var down_glyph = "glyphicon glyphicon-chevron-down" 


    var tbody = document.createElement('tbody');
    for (var rank in cols) {
        col_data = cols[rank];
        var row = document.createElement("tr");

        var url = 'http://ec2-18-216-108-45.us-east-2.compute.amazonaws.com:5000/player?tag='+col_data[0];
        var createClickHandler = function(url) {
            return function() {
                document.location.href = url;
            }
        }
        row.onclick = createClickHandler(url);

        glyph_col = col_data.length-1;
        tag_col = 0;
        for(var i = 0; i < col_data.length; i++) {

            var c = document.createElement('td');
            c.innerHTML = col_data[i];

            if (i == tag_col) {
                // Capitalize the first letter of each word
                caps_tag = capitalize_first_letters(col_data[i]);
				c.innerHTML = caps_tag;
            }
            if (i == glyph_col) {
                up =  col_data[i] > 0 ? true : false;
                var glyph = document.createElement('i');

                // Only give this person a glyph if their ranked changed
                if (col_data[i] != 0) {
                    glyph.className = up ? up_glyph : down_glyph;
                    glyph.style.color = up ? '#6ddc6d' : '#ff7272';
                    glyph.style.fontSize = '1.8em';
                    c.appendChild(glyph);
                }
            }

            row.appendChild(c);
        }
        tbody.appendChild(row);
    }
    table.appendChild(tbody);
}

function processData(data) {
  // taking care of data
}

function handler() {
  if(this.status == 200 &&
    this.responseXML != null &&
    this.responseXML.getElementById('test').textContent) {
    // success!
    processData(this.responseXML.getElementById('test').textContent);
  } else {
    // something went wrong
  }
}

function capitalize_first_letters(str) {
    return str.replace(/\w\S*/g, function(txt){
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}

function previous_month(date) {
	console.log('we are getting previous mont ' + date);
	var prev = prev_date(date);
	var url = 'http://ec2-18-216-108-45.us-east-2.compute.amazonaws.com:5000/ranks?scene='+scene+'&date='+prev;
	console.log('date is ' + prev);
	window.location.replace(url);
}

function next_month(date) {
	console.log('we are getting next mont ' + date);
	var next = next_date(date);
	var url = 'http://ec2-18-216-108-45.us-east-2.compute.amazonaws.com:5000/ranks?scene='+scene+'&date='+next;
	window.location.replace(url);
}

function next_date(date) {
	y = date.split('-')[0];
	m = date.split('-')[1];

	// Incremet the year if this was december
	y = m == '12' ? parseInt(y) + 1 : y;
	m = m == '12' ? '01' : String(parseInt(m) + 1).padStart(2, '0');

	date = y + '-' + m + '-01';
	return date;

}

function prev_date(date) {
	y = date.split('-')[0];
	m = date.split('-')[1];

	// Incremet the year if this was december
	y = m == '01' ? parseInt(y) - 1 : y;
	m = m == '01' ? '12' : String(parseInt(m) - 1).padStart(2, '0');

	date = y + '-' + m + '-01';
	return date;

}
