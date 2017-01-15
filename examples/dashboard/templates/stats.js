$(function () {
    $("#boots").text("{{ stats.boots }}");
    $("#potions").text("{{ stats.potions }}");
    $("#minions").text("{{ stats.minions }}");
    $("#topsold").text("{{ stats.topsold }}");
    $(".number").text("{{ stats.number }}");
    csstat = {{ stats.topcs|tojson|safe }};
    $("#cs-player").text(csstat.player);
    $("#cs-actor").text(csstat.actor);
    $("#cs-cs").text(csstat.cs);
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
            min: -0.5,
            max: 1.5
        },
        title:  {
            text: "Game durations"
        },
        series: {{ stats.durations|tojson|safe }}
    });

    $(".highcharts-credits").hide();
});
