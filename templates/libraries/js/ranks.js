function init() {
    //tag_div = document.getElementById('tag_div');
    //tag_div.innerHTML = tag;

	create_table(JSON.parse(prev_ranks), JSON.parse(cur_ranks));
	//ranks_data = get_ranks_data(scene, date);

}

function create_table(prev, cur) {
	//Put this data in the table
	table = document.getElementById('ranks_table');
    table.innerHTML = '';

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

	for (var rank in sorted_results) {
		col_data = sorted_results[rank];
		add_table_row(table, col_data);
	}
}

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function add_table_row(table, col_data) {
    var up_glyph = "glyphicon glyphicon-chevron-up"
    var down_glyph = "glyphicon glyphicon-chevron-down" 

    var row = document.createElement("tr");
    row.className = "row100 body";

	var url = 'http://ec2-18-216-108-45.us-east-2.compute.amazonaws.com:5000/player?tag='+col_data[0];
	var createClickHandler = function(url) {
		return function() {
			document.location.href = url;
		}
	}
	row.onclick = createClickHandler(url);

    glyph_col = col_data.length-1;
    for(var i = 0; i < col_data.length; i++) {

        var c = document.createElement('td');
        c.className = "cell100 column" +  (i+1);
        c.innerHTML = col_data[i];

        if (i == glyph_col) {
            up =  col_data[i] > 0 ? true : false;
            var glyph = document.createElement('i');

            // Only give this person a glyph if their ranked changed
            if (col_data[i] != 0) {
                glyph.className = up ? up_glyph : down_glyph;
                glyph.style.color = up ? 'green' : 'red';
                glyph.style.fontSize = '1.8em';
                c.appendChild(glyph);
            }
        }

        row.appendChild(c);

    }

    table.appendChild(row);
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

