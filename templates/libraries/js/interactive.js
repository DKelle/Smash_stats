function get_node_from_tag(nodes, tag) {
	console.log(tag);
	for (var i = 0; i < nodes.length; i++) {
		n = nodes[i];
		if (n.name == tag) {
			console.log('found the requested tag!');
			return n
		}
	}
	return nodes[0]
}

function get_all_links_with_node(control, n) {
	console.log('about to get all links with the node');
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

function get_all_nodes_with_links(control, links) {
	let nodes = new Set();
	for (var i = 0; i < links.length; i++) {
		link = links[i];
		nodes.add(link.source);
		nodes.add(link.target);
	}
	return Array.from(nodes);
}
google.load("jquery", "1");
google.setOnLoadCallback(function() {
	initialize().then(
		function(control) {
			var initial_node = get_node_from_tag(control.data.nodes, 'hakii');
			initial_node.isCurrentlyFocused = initial_node.isCurrentlyFocused;
			ls = get_all_links_with_node(control, initial_node);
			ns = get_all_nodes_with_links(control, links);
			control.links = ls;
			control.nodes = ns;
			console.log('found these relevant links');
			doTheTreeViz(control);
		}
	);
});

function doTheTreeViz(control) {
	console.log('inside do the viz with control:')
	console.log(control)

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

	node.select("circle")
		.style("fill", function(d) {
			return getColor(d);
		})
		// TODO this controls the radis
		.attr("r", function(d) {
			//return getRadius(d);
			return 10;
		})

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
							console.log('clicked was just detected and control is');
							console.log(control)
							d.isCurrentlyFocused = !d.isCurrentlyFocused;
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

	if (control.options.nodeLabel) {
		// text is done once for shadow as well as for text
		nodeEnter.append("svg:text")
			.attr("x", control.options.labelOffset)
			.attr("dy", ".31em")
			.attr("class", "shadow")
			.style("font-size", control.options.labelFontSize + "px")
			.text(function(d) {
				return d.shortName ? d.shortName : d.name;
			});
		nodeEnter.append("svg:text")
			.attr("x", control.options.labelOffset)
			.attr("dy", ".35em")
			.attr("class", "text")
			.style("font-size", control.options.labelFontSize + "px")
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
		return control.options.nodeFocus && d.isCurrentlyFocused ? control.options.nodeFocusRadius : r;
	}

	function getColor(d) {
		return control.options.nodeFocus && d.isCurrentlyFocused ? control.options.nodeFocusColor : control.color(d.group);
	}

}

function makeFilteredData(control, selectedNode) {
	// we'll keep only the data where filterned nodes are the source or target
	console.log('inside make filtered with control and node');
	console.log(control);
	console.log(selectedNode);

	console.log('this is a test');
	control.nodes = []
	console.log(control);
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
		control.nodes = control.data.nodes;
		control.links = control.data.links;
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
			width: $(control.divName).outerWidth(),
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
			height: $(control.divName).outerHeight()
		}, control.data.d3.options);

		var options = control.options;
		options.gap = options.gap * options.radius;
		control.width = options.width;
		control.height = options.height;
		control.data = control.data.d3.data;
		control.nodes = control.data.nodes;

		control.data.links = filter_bad_links(control.data.links)

		control.links = control.data.links;
		control.color = d3.scale.category20();
		control.clickHack = 200;
		organizeData(control);

		control.svg = d3.select(control.divName)
			.append("svg:svg")
			.attr("width", control.width)
			.attr("height", control.height);

		// get list of unique values in stylecolumn
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
