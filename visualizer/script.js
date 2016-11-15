var data = null;

$(function() {
	$.getJSON('results.json', function(d){ 
		data = d;

		//console.log(data.agents);
		for(var a in data.agents) {
			$('#model').append('<li><a href="#">'+a+'</a></li>');
			$('#message').append('<li><a href="#">'+a+'</a></li>');
		}

		for(var n in data.timeSteps) {
			$('#time').append('<li><a href="#">'+n+'</a></li>');
		}

		showGrid();

		$('#grid').click(function(){
			showGrid();
		});

		$('#model a').click(function(){
			showModel($(this).text());
		});

		$('#message a').click(function(){
			showMessage($(this).text());
		});

		$('#time a').click(function(){
			showTime($(this).text());
		});
	});
});

function showGrid() {

}

function showModel(agent) {
	var nodes = [];
	var edges = [];

	var maxY = 0;

	var interGroupGap = 150;
	var intraGroupGap = 300;
	var graphGap = 100;

	for(var t in data.agents[agent].intermittent) {
		var countY = 0;
		for(var s in data.agents[agent].intermittent[t]) {
			var n = data.agents[agent].intermittent[t][s];
			nodes.push({id: t+'-'+n.from, label: n.from, group: t, x: t*intraGroupGap, y: s*interGroupGap});
			countY += 1;
			for(var e in n.to) {
				edges.push({from: t+'-'+n.from, to: (parseInt(t)+1)+'-'+n.to[e].to, label: n.to[e].prob, arrows: 'to'});				
			}
		}
		if(countY > maxY) {
			maxY = countY;
		}
	}

	/*for(var t in data.agents[agent].intermittent) {
		nodes.push({id: t, label: 't'+t, group: 'time-step', x: t*intraGroupGap, y: });
	}*/

	for(var t in data.agents[agent].states) {
		for(var s in data.agents[agent].states[t]) {
			var n = data.agents[agent].states[t][s];
			nodes.push({id: t+'s-'+n.from, label: n.from, group: t, x: t*intraGroupGap, y: (maxY + parseInt(s))*interGroupGap + graphGap});
			for(var e in n.to) {
				edges.push({from: t+'s-'+n.from, to: (parseInt(t)+1)+'s-'+n.to[e].to, label: n.to[e].prob, arrows: 'to'});				
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