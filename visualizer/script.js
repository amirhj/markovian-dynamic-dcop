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

function resetSceen() {
	$('#sceen').remove();
	$('body').append('<div id="sceen"></div>');
	$('#sceen').css('margin-top', $('nav').height()+'px');
	$('#sceen').css('height', ($(document).height() - $('nav').height())+'px');
}

function showTime(t) {

	
}

function showMessage(agent) {
	resetSceen();
	setHighchartsTheme();

	Highcharts.chart('sceen', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Stacked column chart'
        },
        xAxis: {
            categories: ['Apples', 'Oranges', 'Pears', 'Grapes', 'Bananas']
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Total fruit consumption'
            },
            stackLabels: {
                enabled: true,
                style: {
                    fontWeight: 'bold',
                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                }
            }
        },
        legend: {
            align: 'right',
            x: -30,
            verticalAlign: 'top',
            y: 25,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',
            borderColor: '#CCC',
            borderWidth: 1,
            shadow: false
        },
        tooltip: {
            headerFormat: '<b>{point.x}</b><br/>',
            pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
        },
        plotOptions: {
            column: {
                stacking: 'normal',
                dataLabels: {
                    enabled: true,
                    color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
                }
            }
        },
        series: [{
            name: 'John',
            data: [5, 3, 4, 7, 2]
        }, {
            name: 'Jane',
            data: [2, 2, 3, 2, 1]
        }, {
            name: 'Joe',
            data: [3, 4, 4, 2, 5]
        }]
    });
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

	resetSceen();

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

function setHighchartsTheme() {
	Highcharts.createElement('link', {
   href: 'https://fonts.googleapis.com/css?family=Unica+One',
   rel: 'stylesheet',
   type: 'text/css'
}, null, document.getElementsByTagName('head')[0]);

Highcharts.theme = {
   colors: ['#2b908f', '#90ee7e', '#f45b5b', '#7798BF', '#aaeeee', '#ff0066', '#eeaaee',
      '#55BF3B', '#DF5353', '#7798BF', '#aaeeee'],
   chart: {
      backgroundColor: {
         linearGradient: { x1: 0, y1: 0, x2: 1, y2: 1 },
         stops: [
            [0, '#2a2a2b'],
            [1, '#3e3e40']
         ]
      },
      style: {
         fontFamily: '\'Unica One\', sans-serif'
      },
      plotBorderColor: '#606063'
   },
   title: {
      style: {
         color: '#E0E0E3',
         textTransform: 'uppercase',
         fontSize: '20px'
      }
   },
   subtitle: {
      style: {
         color: '#E0E0E3',
         textTransform: 'uppercase'
      }
   },
   xAxis: {
      gridLineColor: '#707073',
      labels: {
         style: {
            color: '#E0E0E3'
         }
      },
      lineColor: '#707073',
      minorGridLineColor: '#505053',
      tickColor: '#707073',
      title: {
         style: {
            color: '#A0A0A3'

         }
      }
   },
   yAxis: {
      gridLineColor: '#707073',
      labels: {
         style: {
            color: '#E0E0E3'
         }
      },
      lineColor: '#707073',
      minorGridLineColor: '#505053',
      tickColor: '#707073',
      tickWidth: 1,
      title: {
         style: {
            color: '#A0A0A3'
         }
      }
   },
   tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.85)',
      style: {
         color: '#F0F0F0'
      }
   },
   plotOptions: {
      series: {
         dataLabels: {
            color: '#B0B0B3'
         },
         marker: {
            lineColor: '#333'
         }
      },
      boxplot: {
         fillColor: '#505053'
      },
      candlestick: {
         lineColor: 'white'
      },
      errorbar: {
         color: 'white'
      }
   },
   legend: {
      itemStyle: {
         color: '#E0E0E3'
      },
      itemHoverStyle: {
         color: '#FFF'
      },
      itemHiddenStyle: {
         color: '#606063'
      }
   },
   credits: {
      style: {
         color: '#666'
      }
   },
   labels: {
      style: {
         color: '#707073'
      }
   },

   drilldown: {
      activeAxisLabelStyle: {
         color: '#F0F0F3'
      },
      activeDataLabelStyle: {
         color: '#F0F0F3'
      }
   },

   navigation: {
      buttonOptions: {
         symbolStroke: '#DDDDDD',
         theme: {
            fill: '#505053'
         }
      }
   },

   // scroll charts
   rangeSelector: {
      buttonTheme: {
         fill: '#505053',
         stroke: '#000000',
         style: {
            color: '#CCC'
         },
         states: {
            hover: {
               fill: '#707073',
               stroke: '#000000',
               style: {
                  color: 'white'
               }
            },
            select: {
               fill: '#000003',
               stroke: '#000000',
               style: {
                  color: 'white'
               }
            }
         }
      },
      inputBoxBorderColor: '#505053',
      inputStyle: {
         backgroundColor: '#333',
         color: 'silver'
      },
      labelStyle: {
         color: 'silver'
      }
   },

   navigator: {
      handles: {
         backgroundColor: '#666',
         borderColor: '#AAA'
      },
      outlineColor: '#CCC',
      maskFill: 'rgba(255,255,255,0.1)',
      series: {
         color: '#7798BF',
         lineColor: '#A6C7ED'
      },
      xAxis: {
         gridLineColor: '#505053'
      }
   },

   scrollbar: {
      barBackgroundColor: '#808083',
      barBorderColor: '#808083',
      buttonArrowColor: '#CCC',
      buttonBackgroundColor: '#606063',
      buttonBorderColor: '#606063',
      rifleColor: '#FFF',
      trackBackgroundColor: '#404043',
      trackBorderColor: '#404043'
   },

   // special colors for some of the
   legendBackgroundColor: 'rgba(0, 0, 0, 0.5)',
   background2: '#505053',
   dataLabelsColor: '#B0B0B3',
   textColor: '#C0C0C0',
   contrastTextColor: '#F0F0F3',
   maskColor: 'rgba(255,255,255,0.3)'
};

// Apply the theme
Highcharts.setOptions(Highcharts.theme);
}