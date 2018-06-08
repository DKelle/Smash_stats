hide_wins_chart();

var color_dict =  {
 "sms": "#1f77b4",
 "austin": "#ff7f0e",
 "smashbrews": "#2ca02c",
 "colorado": "#d62728",
 "colorado_doubles": "#9467bd",
 "pro": "#8c564b",
 "pro_wiiu":"#e377c2",
};

// Cut off start and end quote
ranks_data = ranks_data.slice(1).slice(0, -1);
ranks_data = JSON.parse(ranks_data);
months_ranked = months_ranked.slice(1).slice(0, -1);
months_ranked = JSON.parse(months_ranked);
var my_series = [];
var my_scale_x = months_ranked;
var plot_index_to_scene = [];
for (var key in ranks_data) {
    var i = 0;
	// Build up the list that Zing will use to create the graph
    if (ranks_data.hasOwnProperty(key)) {
		var values = ranks_data[key];
		var lineColor = color_dict[key];
		var marker = {'backgroundColor': color_dict[key]};
		var text = key;
        plot_index_to_scene.push(key);

		var d = {'values': values, 'lineColor': lineColor, 'marker': marker, 'text': text};
		my_series.push(d);
    }
}

var myConfig = {
     type: 'line',
     backgroundColor:'#fff',
     title:{
       text:'Rankings for ' + tag + ' over time' ,
       adjustLayout: true,
       fontColor:"#000",
       marginTop: 7
     },
     legend:{
       align: 'center',
       verticalAlign: 'top',
       backgroundColor:'none',
       borderWidth: 0,
       item:{
         fontColor:'#000',
         cursor: 'hand'
       },
       marker:{
         type:'circle',
         borderWidth: 0,
         cursor: 'hand'
       }
     },
     plotarea:{
       margin:'dynamic 70'
     },
     plot:{

       aspect: 'spline',
       lineWidth: 2,
       marker:{
         borderWidth: 0,
         size: 5
       }
     },
     scaleX:{
       lineColor: '#000',
       zooming: true,
       zoomTo:[0,100],
       item:{
        "font-angle":-45,    
         fontColor:'#000'
       },
	   values: my_scale_x
     },
     scaleY:{
       minorTicks: 1,
       lineColor: '#000',
	   mirrored: true,
       tick:{
         lineColor: '#E3E3E5'
       },
       minorTick:{
         lineColor: '#E3E3E5'
       },
       minorGuide:{
         visible: true,
         lineWidth: 1,
         lineColor: '#E3E3E5',
         alpha: 0.7,
         lineStyle: 'dashed'
       },
       guide:{
         lineStyle: 'dashed'
       },
       item:{
         fontColor:'#000'
       }
     },
     tooltip:{
	   text: "Ranked %v in %t on %k. Click for info",
       borderWidth: 0,
       borderRadius: 3
     },
     preview:{
       adjustLayout: true,
       borderColor:'#E3E3E5',
       mask:{
         backgroundColor:'#E3E3E5'
       }
     },


     shapes:[
              {
                type:'rectangle',
                id:'view_all',
                height:'20px',
                width:'75px',
                borderColor:'#E3E3E5',
                borderWidth:1,
                borderRadius: 3,
                x:'85%',
                y:'11%',
                backgroundColor:'#53535e',
                cursor:'hand',
                label:{
                  text:'View All',
                  fontColor:'#E3E3E5',
                  fontSize:12,
                  bold:true
                }
              }
            ],
	series: my_series
};

zingchart.render({ 
    id: 'myChart', 
    data: myConfig, 
    height: "99%", 
    width: "99%" 
});

zingchart.shape_click = function(p){
  if(p.shapeid == "view_all"){
    zingchart.exec(p.id,'viewall');
  }
}

zingchart.node_click = function(e) {
	var rank = e.value;
	var date = e.scaletext;
    var scene = plot_index_to_scene[e.plotindex];

	big_wins_url = "http://ec2-18-216-108-45.us-east-2.compute.amazonaws.com:5000/big_wins?tag="+tag+"&date="+date+"&scene="+scene;
	big_wins = JSON.parse(httpGet(big_wins_url));

	bad_losses_url = "http://ec2-18-216-108-45.us-east-2.compute.amazonaws.com:5000/bad_losses?tag="+tag+"&date="+date+"&scene="+scene;
	bad_losses = JSON.parse(httpGet(bad_losses_url));

    if (big_wins.length + bad_losses.length == 0) {
        hide_wins_chart();
    }
    else {
        open_wins_chart();
    }

    format_recent_wins_losses_graph(big_wins, bad_losses);
}

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function format_recent_wins_losses_graph(wins, losses) {
    table = document.getElementById('wins_table');
    table.innerHTML = '';
    for (var i = 0; i < wins.length; i++) {
        add_table_row(table, wins[i]);
    }

    table = document.getElementById('losses_table');
    table.innerHTML = '';
    for (var i = 0; i < losses.length; i++) {
        add_table_row(table, losses[i]);
    }
}

function hide_wins_chart() {
    var container_div = document.getElementById('left_div');
    container_div.style.width = "0%";

    var container_div = document.getElementById('right_div');
    container_div.style.width = "100%";

    //var top_half = document.getElementById('top_half');
    //top_half.innerHTML = '';

    //var bottom_half = document.getElementById('bottom_half');
    //bottom_half.innerHTML = '';

}

function open_wins_chart() {
    var container_div = document.getElementById('left_div');
    container_div.style.width = "28%";

    var container_div = document.getElementById('right_div');
    container_div.style.width = "71%";

    //var top_half = document.getElementById('top_half');
    //top_half.innerHTML = 'Big Wins';
      
    //var bottom_half = document.getElementById('bottom_half');
    //bottom_half.innerHTML = 'Bad Losses';

}

function add_table_row(table, col_data) {
    var row = document.createElement("tr");
    row.className = "row100 body";
    var url = 'http://ec2-18-216-108-45.us-east-2.compute.amazonaws.com:5000/player?tag='+col_data[0];
	var createClickHandler = function(url) {
		return function() {
			document.location.href = url;
		}
	}
	row.onclick = createClickHandler(url);

    for(var i = 0; i < col_data.length; i++) {

        var c = document.createElement('td');
        c.className = "cell100 column" +  (i+1);
        c.innerHTML = col_data[i];

        row.appendChild(c);

    }

    table.appendChild(row);
}
