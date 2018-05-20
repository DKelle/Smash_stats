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
for (var key in ranks_data) {
	// Build up the list that Zing will use to create the graph
    if (ranks_data.hasOwnProperty(key)) {
		var values = ranks_data[key];
		var lineColor = color_dict[key];
		var marker = {'backgroundColor': color_dict[key]};
		var text = key;

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

zingchart.click = function(p) {
    console.log(p);
}
