$(function () {
    Highcharts.chart("gameType", {
        chart: {
            type: "pie"
        },
        title:  {
            text: "Game modes over the last {{ stats.number }} matches"
        },
        series: [{
            data: {{ stats.gameModes|tojson|safe }}
        }]
    });
    Highcharts.chart("players", {
        chart: {
            type: "bar"
        },
        xAxis: {
            categories: ["matches"]
        },
        title:  {
            text: "Most active players"
        },
        series: {{ stats.players|tojson|safe }}
    });
    Highcharts.chart("picks", {
        chart: {
            type: "column"
        },
        title:  {
            text: "Popular picks"
        },
        plotOptions: {
            column: {
                stacking: "normal"
            }
        },
        xAxis: {
            categories: {{ stats.heroes|tojson|safe }}
        },
        series: {{ stats.picks|tojson|safe }}
    });
    Highcharts.chart("durations", {
        chart: {
            type: "scatter"
        },
        yAxis: {
            title: {
                text: "length in minutes"
            }
        },
        xAxis: {
            labels: {
                enabled: false
            },
            tickInterval: 1,
        },
        title:  {
            text: "Game durations"
        },
        series: {{ stats.durations|tojson|safe }}
    });
});
