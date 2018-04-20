google.load("jquery", "1");
google.setOnLoadCallback(function() {
	initialize().then(

		function(control) {

            // Set onclicks for the legends
            // sms
            //legend = document.getElementById('dot_sms');
            //legend.addEventListener("click", function(){
            //    //ns = get_top_10_nodes_from_scene(control, 'sms');
            //    //control.data.nodes = ns;
            //    //control.data.links = [];
            //    doTheTreeViz(control);
            //});

            //// austin
            //legend = document.getElementById('dot_austin');
            //legend.addEventListener("click", function(){
            //    temp('austin');
            //});

			var initial_node = get_node_from_tag(control.data.nodes, tag);

            // Append this node to our stats nav player queue
            p_queue.push(initial_node.name);

			initial_node.isCurrentlyFocused = initial_node.isCurrentlyFocused;

            initial_node.fixed = true;
            initial_node.x = control.width/2;
            initial_node.y = control.height/2;

			ls = get_all_links_with_node(control, initial_node);
			ns = get_all_nodes_with_links(control, links, initial_node);
			control.links = ls;
			control.nodes = ns;

			doTheTreeViz(control);
		}
	);
});

function get_top_10_nodes_from_scene(control, scene) {
    scenes = ['temp', 'sms', 'austin', 'smashbrews', 'colorado', 'colorado_doubles', 'pro_melee', 'pro_smash4'];
    group = scenes.indexOf(scene);
	ns = []
    for (var i = 0; i < control.nodes.length; i++) {
        if (control.nodes[i].rank && control.nodes[i].rank < 11) {
            ns.push(control.nodes[i]);
        }
    }
    control.data.nodes = ns;
    return ns;
}

function get_node_from_tag(nodes, tag) {
	for (var i = 0; i < nodes.length; i++) {
		n = nodes[i];
		if (n.name == tag) {
			return n
		}
	}
	return nodes[0]
}

function get_all_links_with_node(control, n) {
	links = [];
	for (var i = 0; i < control.data.links.length; i++) {
		var link = control.data.links[i];
		if (link.target && link.source) {
			if (link.target.name == n.name || link.source.name == n.name) {
				links.push(link);
			}
		}
	}
	return links;
}

function get_all_nodes_with_links(control, links, initial_node) {
	let nodes = new Set();
    nodes.add(initial_node);
	for (var i = 0; i < links.length; i++) {
		link = links[i];
		nodes.add(link.source);
		nodes.add(link.target);
	}
    ns = Array.from(nodes);
    ns[0].isCurrentlyFocused = true;
	return ns;
}


function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function get_bracket_display_name(bracket) {
	map = {'RAA': 'SMS', 'heat':'Heatwave', 'hw':'Heatwave', 'austinsmash': 'Smashpack', 'np9': 'NP', 'smashbrews': 'smashbrews', 'smashco': 'CSU', 'alibaba': 'Alibaba'};
	for (var key in map) {
		if (bracket.toLowerCase().includes(key.toLowerCase())) {
			// display name will be just 'SMS' or 'Heatwave', etc
			display_name = map[key];
			console.log(bracket);
			var thenum = bracket.split("/").pop().replace( /^\D+/g, '');
			console.log('the number is '+ thenum);

			display_name = display_name + ' ' + thenum;
			return display_name
		}
	}
}
var p_queue = [];
function update_stats_nav(node) {
    tag = node.name;
    // Is this player already in the queue? If so, remove them
    i = p_queue.indexOf(tag);
    if (i > -1) {
        p_queue.splice(i,1);
    }
    else {
        p_queue.push(node.name);
    }

    // Find out which players to show stats for
    p1 = p_queue[p_queue.length-1];
    matches = 0;
    results = 0;
    for(var i = p_queue.length-1; i--; i > -1) {
		p2 = p_queue[i];
		url = "http://ec2-18-216-108-45.us-east-2.compute.amazonaws.com:5000/h2h?tag1="+p1+"&tag2="+p2;

		result = JSON.parse(httpGet(url));
		matches = result.length;

		if (matches > 0) {
			break;
		}
    }

	if (matches > 0) {

		// Make sure the sidenav is actually visible
		document.getElementById('mySidenav').style.width = '25%';

		// We have found some results between two players. Set their tags in the stats nav.
		t1 = document.getElementById('tag1');
		t2 = document.getElementById('tag2');
		t1.innerHTML = p1;
		t2.innerHTML = p2;

		// Actually add their matches to the nav stats
		matches_div = document.getElementById('matches');

		// remove all old match results
		var ul = document.getElementById("matches_list");
		while (ul.hasChildNodes()) {
			ul.removeChild(ul.childNodes[0]);
		}

		for(var i = 0; i < result.length; i ++) {
			r = result[i];
			winner = r[2];
			bracket = r[5];
            scene = r[4];
			match_text = winner + ':' + bracket;
			display_name = get_bracket_display_name(bracket);

            // Was the winner p1 or p2?
            var li_class = "loser";
            if (p1 == winner) {
                li_class = "winner";
                console.log('winner was p1')
            }
            li_class += ' ' + scene;

			// Add this match to the ul
			var li = document.createElement("li");
			li.appendChild(document.createTextNode(display_name));
			li.setAttribute("id", "matches_li");
			li.setAttribute("class", li_class);

            // Create a link to this bracket
            var a = document.createElement('a');
			a.setAttribute("href", bracket);
            li.appendChild(a);
			ul.appendChild(li);
		}

	}
	else {
		// Close the sidenav
		document.getElementById('mySidenav').style.width = '0%';
		
	}

    // Change the tags displayed on the stats nav
}

function doTheTreeViz(control) {

	var svg = control.svg;

	var force = control.force;

	control.links = filter_bad_links(control.links)
	force.nodes(control.nodes)
		.links(control.links)
		.start();

	// Update the links
	var link = svg.selectAll("line.link")
		.data(control.links, function(d) {
			return d.unique;
		});

	// Enter any new links
	link.enter().insert("svg:line", ".node")
		.attr("class", "link")
		.attr("x1", function(d) {
			return d.source.x;
		})
		.attr("y1", function(d) {
			return d.source.y;
		})
		.attr("x2", function(d) {
			return d.target.x;
		})
		.attr("y2", function(d) {
			return d.target.y;
		})
		.append("svg:title")
		.text(function(d) {
			return d.source[control.options.nodeLabel] + ":" + d.target[control.options.nodeLabel];
		});

	// Exit any old links.
	link.exit().remove();

	// Update the nodes
	var node = svg.selectAll("g.node")
		.data(control.nodes, function(d) {
			return d.unique;
		});
        //.attr("d", function(d) { return line(d.values); })
        //.style("stroke", function(d) { return color(d.name); });

	node.select("circle")
		.style("fill", function(d) {
			return getColor(d);
		})
		.attr("r", function(d) {
			return getRadius(d);
		});

	node.append('circle')
		.attr('r', 3)
		.style('fill', 'black');


	// Enter any new nodes.
	var nodeEnter = node.enter()
		.append("svg:g")
		.attr("class", "node")
		.attr("transform", function(d) {
			return "translate(" + d.x + "," + d.y + ")";
		})
		.on("dblclick", function(d) {
			control.nodeClickInProgress = false;
			if (d.url) window.open(d.url);
		})
		.on("click", function(d) {
			// this is a hack so that click doesnt fire on the1st click of a dblclick
			if (!control.nodeClickInProgress) {
				control.nodeClickInProgress = true;
				setTimeout(function() {
					if (control.nodeClickInProgress) {
						control.nodeClickInProgress = false;
						if (control.options.nodeFocus) {
							d.isCurrentlyFocused = !d.isCurrentlyFocused;
                            update_stats_nav(d);
                            if  (d.fixed == 6 || !d.fixed) {
                                d.fixed = true;
                            }
                            else {
                                d.fixed = false;
                            }
							doTheTreeViz(makeFilteredData(control));
						}
					}
				}, control.clickHack);
			}
		})
		.call(force.drag);

	nodeEnter
		.append("svg:circle")
		.attr("r", function(d) {
			return getRadius(d);
		})
		.style("fill", function(d) {
			return getColor(d);
		})
		.append("svg:title")
		.text(function(d) {
			return d[control.options.nodeLabel];
		});

	nodeEnter.append("circle")
		.attr("r", 3)
		.style("fill", 'black');

	if (control.options.nodeLabel) {
		// text is done once for shadow as well as for text
		nodeEnter.append("svg:text")
			.attr("x", control.options.labelOffset)
			.attr("dy", ".31em")
			.attr("class", "shadow")
			.style("font-size", control.options.labelFontSize + "px")
			.style("font-weight", "bold")
			.text(function(d) {
				return d.shortName ? d.shortName : d.name;
			});
		nodeEnter.append("svg:text")
			.attr("x", control.options.labelOffset)
			.attr("dy", ".35em")
			.attr("class", "text")
			.style("font-size", control.options.labelFontSize + "px")
			.style("font-weight", "bold")
			.text(function(d) {
				return d.shortName ? d.shortName : d.name;
			});
	}

	// Exit any old nodes.
	node.exit().remove();
	control.link = svg.selectAll("line.link");
	control.node = svg.selectAll("g.node");
	force.on("tick", tick);

	if (control.options.linkName) {
		link.append("title")
			.text(function(d) {
				return d[control.options.linkName];
			});
	}

	function tick() {
		link.attr("x1", function(d) {
				return d.source.x;
			})
			.attr("y1", function(d) {
				return d.source.y;
			})
			.attr("x2", function(d) {
				return d.target.x;
			})
			.attr("y2", function(d) {
				return d.target.y;
			});
		node.attr("transform", function(d) {
			return "translate(" + d.x + "," + d.y + ")";
		});

	}

	function getRadius(d) {
		var r = control.options.radius * (control.options.nodeResize ? Math.sqrt(d[control.options.nodeResize]) / Math.PI : 1);
        var r = d.radius;
		return r;
		return control.options.nodeFocus && d.isCurrentlyFocused ? 25 : r;
	}

	function getColor(d) {
        // TODO update this as we get more scenes
		return control.options.nodeFocus && d.isCurrentlyFocused ? control.options.nodeFocusColor : control.color_map[d.group];
	}

}

function get_top_10_nodes(control, selectedNode) {
	ns = []
    for (var i = 0; i < control.data.nodes.length; i++) {
        if (control.data.nodes[i].rank && control.data.nodes[i].rank < 11) {
            ns.push(control.data.nodes[i]);
        }
    }
    return ns;
}

function makeFilteredData(control, selectedNode) {
	// we'll keep only the data where filterned nodes are the source or target

	control.nodes = []
	var newNodes = [];
	var newLinks = [];

	for (var i = 0; i < control.data.links.length; i++) {
		var link = control.data.links[i];
		if (link.target && link.source) {
			if (link.target.isCurrentlyFocused || link.source.isCurrentlyFocused) {
				newLinks.push(link);
				addNodeIfNotThere(link.source, newNodes);
				addNodeIfNotThere(link.target, newNodes);
			}
		}
	}
	// if none are selected reinstate the whole dataset
	if (newNodes.length > 0) {
		control.links = newLinks;
		control.nodes = newNodes;
	} else {
        control.links = [];
        control.nodes = get_top_10_nodes(control, selectedNode);
		//control.nodes = control.data.nodes;
		//control.links = control.data.links;
	}
	return control;

	function addNodeIfNotThere(node, nodes) {
		for (var i = 0; i < nodes.length; i++) {
			if (nodes[i].unique == node.unique) return i;
		}
		return nodes.push(node) - 1;
	}
}

function organizeData(control) {

	for (var i = 0; i < control.nodes.length; i++) {
		var node = control.nodes[i];
		node.unique = i;
		node.isCurrentlyFocused = false;
	}

	for (var i = 0; i < control.links.length; i++) {
		var link = control.links[i];
		link.unique = i;
		link.source = control.nodes[link.source];
		link.target = control.nodes[link.target];
	}
	return control;
}

function filter_bad_links(links) {
	//filter out the bad links
	var newlinks = []
	for (var i = 0; i < links.length; i++) {
		if (links[i].target && links[i].source) {
			newlinks.push(links[i])
		}
	}
	return newlinks
}

function initialize() {

	var initPromise = $.Deferred();

	getTheData().then(function(data) {
		var control = {};
		control.data = data;
		control.divName = "#chart";

		control.options = $.extend({
			stackHeight: 12,
			radius: 5,
			fontSize: 14,
			labelFontSize: 8,
			nodeLabel: null,
			markerWidth: 0,
			markerHeight: 0,
			width: window.innerWidth,
			gap: 1.5,
			nodeResize: "",
			linkDistance: 80,
			charge: -120,
			styleColumn: null,
			styles: null,
			linkName: null,
			nodeFocus: true,
			nodeFocusRadius: 25,
			nodeFocusColor: "black",
			labelOffset: "5",
			gravity: .05,
			height: window.innerHeight
		}, control.data.d3.options);

		var options = control.options;
		options.gap = options.gap * options.radius;
		control.width = options.width;
		control.height = options.height;
		control.data = control.data.d3.data;
		control.nodes = control.data.nodes;
        control.cur = [0, 0]
        control.last_mouse = [0, 0]
        control.last_vb = [0, 0]

		control.data.links = filter_bad_links(control.data.links)

		control.links = control.data.links;
		control.color = d3.scale.category10();
        control.color_map = [];
        for (var i = 0; i < 10; i++) {
            control.color_map.push(control.color(i));

        }
		control.clickHack = 200;
		organizeData(control);

		control.svg = d3.select(control.divName)
			.append("svg:svg")
			.attr("width", control.width)
			.attr("height", control.height)
            .attr("viewBox", "0 0 " + control.width + " " + control.height )
            .attr("preserveAspectRatio", "xMinYMin");

		// On mouse move
		function handler(e) {
			e = e || window.event;

			var pageX = e.pageX;
			var pageY = e.pageY;

			// IE 8
			if (pageX === undefined) {
				pageX = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
				pageY = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
			}

			control.last_mouse = control.cur;
			control.cur = [pageX, pageY];
		}
		// attach handler to the click event of the document
		if (document.attachEvent) document.attachEvent('onclick', handler);
		else document.addEventListener('click', handler);
		document.onmousemove = handler;


		// Panning and zooming
		var zoomListener = d3.behavior.zoom()
		  .scaleExtent([0.1, 8])
		  .on("zoom", zoomHandler);

		var dragListener = d3.behavior.drag()
			.on("drag", function() {
				dragX = d3.event.dx;
				dragY = d3.event.dy;
			});

        function resize() {
                var width = window.innerWidth, height = window.innerHeight;
                control.svg.attr("width", width).attr("height", height);
                    control.force.size([width, height]).resume();
        }
        window.addEventListener('resize', resize); 

		zoomListener(control.svg); 
		control.svg.call(dragListener);

		var dragging = 0;   
		var dragX = 0, dragY = 0;

		dragListener.on("dragstart", function() {
		  dragging = 1;
		}); 

		dragListener.on("dragend", function() {
		  dragging = 0;
		  dragX = 0;
		  dragY = 0;
		}); 

		function zoomHandler() {
			var pos = control.cur;
			var scale = d3.event.scale;
			var temptrans = d3.event.translate;

			var trans = d3.transform(control.svg.attr("transform"));
			var tpos = trans.translate;
			var tscale = trans.scale;
			var tx = tpos[0];
			var ty = tpos[1];
			var mx = pos[0] - control.width/2;
			var my = pos[1] - control.height/2;

			var dx =  (mx - tx - dragX)/tscale[0];
			var dy =  (my - ty - dragY)/tscale[1];
			var dx2 = (mx - dx)/scale - dx;
			var dy2 = (my - dy)/scale - dy;

            var temp = 0;
            if (dy < 0) { temp = 50; }
            else { temp = -50; }
            oldView = control.svg.viewBox;
            dmouse = [control.last_mouse[0] - pos[0], control.last_mouse[1] - pos[1]];
            control.last_mouse = pos;
            // Only change the viewbox if it is not a huge jump
            //var dist  = oldView.x - dx;
			var newViewBox = [
                control.last_vb[0] + dmouse[0],
                control.last_vb[1] + dmouse[1],
				(control.width / scale),
				(control.height / scale)
			].join(" ");

			control.last_vb[0] += dmouse[0],
			control.last_vb[1] += dmouse[1],

            control.svg.attr('viewBox', newViewBox);

			var tform = "translate(" + dx + "," + dy + ")scale(" + scale + ")translate(" + dx2 + "," + dy2 + ")";
			//control.svg.attr("transform", tform); 
		}


		control.linkStyles = [];
		if (control.options.styleColumn) {
			var x;
			for (var i = 0; i < control.links.length; i++) {
				if (control.linkStyles.indexOf(x = control.links[i][control.options.styleColumn].toLowerCase()) == -1)
					control.linkStyles.push(x);
			}
		} else
			control.linkStyles[0] = "defaultMarker";

		control.force = d3.layout.force().
		size([control.width, control.height])
			.linkDistance(control.options.linkDistance)
			.charge(control.options.charge)
			.gravity(control.options.gravity);

		initPromise.resolve(control);
	});
	return initPromise.promise();
}


function getTheData() {
	var dataPromise = $.Deferred();
	// return a promise if data is being received asynch and resolve it when done.
	dataPromise.resolve(mcpherTreeData);
	return dataPromise.promise();
}
