var data = null;

$(function() {
	$.getJSON('result.json', function(d){ 
		data = d;

		for(var a in Object.keys(data.agents)) {
			$('#model').append('<li><a href="#">'+a+'</a></li>');
			$('#message').append('<li><a href="#">'+a+'</a></li>');
		}

		for(var n in Object.keys(data.timeSteps)) {
			$('#time').append('<li><a href="#">'+n+'</a></li>');
		}

		showGrid();

		$('#grid').click(function(){
			showGrid();
		});

		$('#model a').click(function(){
			showModel($(this).text);
		});

		$('#message a').click(function(){
			showMessage($(this).text);
		});

		$('#time a').click(function(){
			showTime(($(this).text);
		});
	});
});

function showGrid() {

}

function showModel(agent) {
	var nodeCount = 0;
	var nodes = [];
	var edges = [];

	var interGroupGap = 150;
	var intraGroupGap = 300;
	var graphGap = 100;

	var x = 0;
	var y = 0;

	for(var t in data.agents[agent].intermittent) {
		for(var s in data.agents[agent].intermittent[t]) {
			var n = data.agents[agent].intermittent[t][s];
			nodes.push({id: t+'-'+n.from, label: n.from, group: t, x: t*intraGroupGap, y: s*interGroupGap});
			for(var e in n.to) {
				edges.push({from: t+'-'+n.from, to: (t+1)+'-'+n.to[e].to, label: n.to[e].prob, arrows: 'to'});				
			}
		}
	}

	/*for(var t in data.agents[agent].intermittent) {
		nodes.push({id: t, label: 't'+t, group: 'time-step', x: t*intraGroupGap, y: });
	}*/

	for(var t in data.agents[agent].states) {
		for(var s in data.agents[agent].states[t]) {
			var n = data.agents[agent].states[t][s];
			nodes.push({id: t+'s-'+n.from, label: n.from, group: t, x: t*intraGroupGap, y: s*interGroupGap + graphGap*2});
			for(var e in n.to) {
				edges.push({from: t+'s-'+n.from, to: (t+1)+'s-'+n.to[e].to, label: n.to[e].prob, arrows: 'to'});				
			}
		}
	}

	$('#sceen').remove();
	$('body').append('<div id="sceen"></div>');

	var container = document.getElementById('sceen');
	var grid = {
		nodes: nodes,
		edges: edges
	};
	var options = {
		manipulation: false,
		nodes: {
			shape: 'dot',
			size: 30,
			font: {
				size: 32,
				color: '#ffffff'
			},
			borderWidth: 2,
			shadow:true,
			fixed: {x:true,y:true}
		},
		edges: {
			width: 2,
			smooth: {
				type: 'continuous',
				roundness: 0
			},
			font: {align: 'horizontal'}
		},
		physics: false
	};
	network = new vis.Network(container, grid, options);
}



var color = 'gray';
var len = undefined;

var nodes = [
	{id: 1, label: "1", group: 0, x:0, y:0},
	{id: 2, label: "2", group: 0, x:0, y:150},
	{id: 3, label: "3", group: 0, x:0, y:300},
	{id: 4, label: "4", group: 1, x:300, y:0},
	{id: 5, label: "5", group: 1, x:300, y:150},
	{id: 6, label: "6", group: 1, x:300, y:300},
	{id: 7, label: "7", group: 2, x:600, y:0},
	{id: 8, label: "8", group: 2, x:600, y:150}
];
var edges = [
	{from: 1, to: 4, label: '0.5', arrows: 'to'},
	{from: 1, to: 5, label: '0.4', arrows: 'to'},
	{from: 2, to: 4, label: '0.5', arrows: 'to'},
	{from: 2, to: 4, label: '0.2', arrows: 'to'},
	{from: 2, to: 6, label: '0.6', arrows: 'to'},
	{from: 3, to: 4, label: '0.6', arrows: 'to'},
	{from: 3, to: 6, label: '0.7', arrows: 'to'},
	{from: 4, to: 7, label: '0.8', arrows: 'to'},
	{from: 4, to: 8, label: '0.3', arrows: 'to'},
	{from: 5, to: 7, label: '0.5', arrows: 'to'},
	{from: 6, to: 7, label: '0.7', arrows: 'to'},
	{from: 6, to: 8, label: '0.2', arrows: 'to'}
]

// create a network
var container = document.getElementById('mynetwork');
var data = {
	nodes: nodes,
	edges: edges
};
var options = {
	manipulation: false,
	nodes: {
		shape: 'dot',
		size: 30,
		font: {
			size: 32,
			color: '#ffffff'
		},
		borderWidth: 2,
		shadow:true,
		fixed: {x:true,y:true}
	},
	edges: {
		width: 2,
		smooth: {
			type: 'continuous',
			roundness: 0
		},
		font: {align: 'horizontal'}
	},
	physics: false
};
network = new vis.Network(container, data, options);