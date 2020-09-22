var elo_chart = $(".elo_chart");
var graph_chart = $(".graph_chart");
var labels_chart = [];
for (i = 1; i < 21; i++){
    labels_chart.push(i)
}
labels_chart.reverse();
$(document).ready(function(){
    var elo = 2500;
    var elo_array = [1877,1856,1881,1906,1881,1858,1832,1806,1830,1855,1831,1806,1782,1806,1830,1803,1780,1757,1780,1755,1778,1803,1778,1804,1782,1755,1779,1804,1829,1852,1876];
    var red='#FE1F00',silver = "#EEEEEE",orange='#FF6309',yellow = "#FFC800",green='#1CE400',grey='#A5A5A5',darkgrey='#5A5A5A';
    var prev_clr,bar_clr,next_lvl,prev_lvl;
    switch(true){case(elo<=800):lvl=1;prev_clr=green;bar_clr=silver;prev_lvl=0;next_lvl=800;break;case(elo<=950):lvl=2;prev_clr=silver;bar_clr=green;prev_lvl=800;next_lvl=950;break;case(elo<=1100):lvl=3;prev_clr=green;bar_clr=green;prev_lvl=950;next_lvl=1100;break;case(elo<=1250):lvl=4;prev_clr=green;bar_clr=yellow;prev_lvl=1100;next_lvl=1250;break;case(elo<=1400):lvl=5;prev_clr=yellow;bar_clr=yellow;prev_lvl=1250;next_lvl=1400;break;case(elo<=1550):lvl=6;prev_clr=yellow;bar_clr=yellow;prev_lvl=1400;next_lvl=1550;break;case(elo<=1700):lvl=7;prev_clr=yellow;bar_clr=yellow;next_lvl=orange;prev_lvl=1550;next_lvl=1700;break;case(elo<=1850):lvl=8;prev_clr=yellow;bar_clr=orange;prev_lvl=1700;next_lvl=1850;break;case(elo<=2000):lvl=9;prev_clr=orange;bar_clr=orange;prev_lvl=1850;next_lvl=2000;break;case(elo>2000):lvl=10;prev_clr=orange;bar_clr=red;darkgrey=red;prev_lvl=2000;next_lvl=0;break;default:prev_clr=grey;bar_clr=grey;prev_lvl='Err';next_lvl='Err';break;}
    var levelChart=new Chart(elo_chart,{
    type:'doughnut',
    data:{
        datasets:[{
            data:[
            ((lvl==1)?0:20),
            ((lvl==10||lvl==1)?((lvl==1)?elo:150):elo-prev_lvl),
            ((lvl==10||lvl==1)?((lvl==1)?next_lvl-elo:0):next_lvl-elo),
            ((lvl==10)?0:20)],
            backgroundColor:[
                prev_clr,
                bar_clr,
                darkgrey],
            borderColor: "#141414",
            borderWidth: 3
            }]},
    options:{
        tooltips:{enabled:false},
        maintainAspectRatio:false,
        cutoutPercentage:75,
        rotation:-(7/6)*Math.PI,
        circumference:4/3*Math.PI}});
    
    var ELOChart = new Chart(graph_chart, {
        type: 'line',
        data: {
            labels: labels_chart,
            datasets: [{
                data: elo_array,
                borderColor: "#ff8c00",
                backgroundColor: "rgba(255, 140, 0, 0.2)",
                fill: true
            }],
            options: {
                elements: {
                    line: {
                        tension: 0,
                    }
                }
            }
        },
        options: {
            legend: {
                display: false
            },
            scales: {
                xAxes: [{
                    gridLines: {
                    color: '#282828',
                    lineWidth: 1
                    }
                }],
                yAxes:[{
                    gridLines: {
                        color: '#282828',
                        lineWidth: 1
                    }
                }]
            }
        }
    });
    $(".lvl").html(lvl);
    $(".lvl").css("color",bar_clr);
    $(".elo").html("ELO : " + elo);
    if (elo<2001){
        $(".remain").html("You need " + (next_lvl+1 - elo) + " ELO to the next level");
    }
    else{
        $(".remain").hide();
        $(".lvl").css("margin-top","50px");
    } 
    $(".match").each(function (index, element) {
        if ($(this).children(".match_container").children(".result").children(".current_result").html() == "WIN") {
            $(this).children(".match_container").addClass("match_win");
        }
        else{
           $(this).children(".match_container").addClass("match_lose"); 
        } 
    });
    $(".result").each(function (index, element) {
        (($(this).children(".current_result").html()=="WIN")?$(this).addClass("positive"):$(this).addClass("negative"));
        
    });
    $(".kad").each(function (index, element) {
        let list1 = $(this).html().split(" / ");
        ((Number(list1[0])>=Number(list1[2]))?$(this).addClass("positive"):$(this).addClass("negative"))
    });
    $(".kd").each(function (index, element) {
        ((Number($(this).html())>=1)?$(this).addClass("positive"):$(this).addClass("negative"))
    });
    $(".elo_change").each(function (index, element) {
        (($(this).html()>0)?$(this).addClass("positive"):$(this).addClass("negative"))
    });
    $(".date").each(function(index, element) {
        $(this).html($(this).html().replace(" ", "<br>"))
    });
    $(".match_container").click(function(){return scrollPos = $(window).scrollTop(),$(this).parent().children(".scoreboard").toggleClass("scoreboard_show"),$(window).scrollTop(scrollPos)
    });
    $(".search_button_mobile").click(function(){return $(".search_block").toggleClass("vis"),
        $(".search_block_close").css({"display" : "block"}),
        $(".logo").toggleClass("disable"),
        $(".search_button_mobile").toggleClass("disable"),
        $(".search_field").focus()
    });
    $(".search_block_close").click(function(){return $(".search_block").toggleClass("vis"),
        $(".search_block_close").css({"display" : "none"}),
        $(".search_button_mobile").toggleClass("disable"),
        $(".logo").toggleClass("disable")
    
    });
    $(".games_select").click(function(){
        $(this).toggleClass("games_select_open");
        $(".select_list").toggleClass("list-open");
    });
    $(".select_list_item").click(function(){
        $(".select_list_item").removeClass("select_list_item_selected");
        $(this).toggleClass("select_list_item_selected");
        $(".games_select").toggleClass("games_select_open");
        $(".select_list").toggleClass("list-open");
        $(".cur_select").html($(this).html());
    });

})
