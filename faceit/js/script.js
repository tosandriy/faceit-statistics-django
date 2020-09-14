var elo_chart = $(".elo_chart");
var graph_chart = $(".graph_chart");
var labels_chart = [];
for (i = 1; i < 21; i++){
    labels_chart.push(i)
};
labels_chart.reverse()
$(document).ready(function(){
    var elo =1876
    var red='#f00000',orange='#ffc000',green='#00f000',grey='#a5a5a5',darkgrey='#5a5a5a';
    var prevClr,barClr,nextLvl,prevLvl,nextClr;
    switch(true){case(elo<=800):lvl=1;prevClr=green;barClr=("#EEEEEE");nextClr=green;prevLvl=0;nextLvl=800;break;case(elo<=950):lvl=2;prevClr=("#EEEEEE");barClr=green;nextClr=green;prevLvl=800;nextLvl=950;break;case(elo<=1100):lvl=3;prevClr=green;barClr=green;nextClr=orange;prevLvl=950;nextLvl=1100;break;case(elo<=1250):lvl=4;prevClr=green;barClr=orange;nextClr=orange;prevLvl=1100;nextLvl=1250;break;case(elo<=1400):lvl=5;prevClr=orange;barClr=orange;nextClr=orange;prevLvl=1250;nextLvl=1400;break;case(elo<=1550):lvl=6;prevClr=orange;barClr=orange;nextClr=orange;prevLvl=1400;nextLvl=1550;break;case(elo<=1700):lvl=7;prevClr=orange;barClr=orange;nextLvl=red;prevLvl=1550;nextLvl=1700;break;case(elo<=1850):lvl=8;prevClr=orange;barClr=red;nextClr=red;prevLvl=1700;nextLvl=1850;break;case(elo<=2000):lvl=9;prevClr=red;barClr=red;nextClr=red;prevLvl=1850;nextLvl=2000;break;case(elo>2000):lvl=10;prevClr=red;barClr=red;nextClr=red;darkgrey=red;prevLvl=2000;nextLvl=0;break;default:prevClr=grey;barClr=grey;prevLvl='Err';nextLvl='Err';break;}
    var levelChart=new Chart(elo_chart,{
    type:'doughnut',
    data:{
        datasets:[{
            data:[
            ((lvl==1)?0:20),
            ((lvl==10||lvl==1)?((lvl==1)?elo:150):elo-prevLvl),
            ((lvl==10||lvl==1)?((lvl==1)?nextLvl-elo:0):nextLvl-elo),
            ((lvl==10)?0:20)],
            backgroundColor:[
                prevClr,
                barClr,
                ((lvl==10)?'red':grey),
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
                data: [1877,1856,1881,1906,1881,1858,1832,1806,1830,1855,1831,1806,1782,1806,1830,1803,1780,1757,1780,1755,1778,1803,1778,1804,1782,1755,1779,1804,1829,1852,1876],
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
    $(".lvl").css("color",barClr);
    $(".elo").html("ELO : " + elo);
    $(".remain").html("You need " + (nextLvl+1 - elo) + " ELO to the next level");
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
    $(".match_container").click(function(){return scrollPos = $(window).scrollTop(),$(this).parent().children(".scoreboard").toggleClass("scoreboard_show"),$(window).scrollTop(scrollPos)
    });
    $(".search_button_mobile").click(function(){return $(".search_block").toggleClass("vis"),
        $(".search_block_close").css({"display" : "block"}),
        $(".logo").toggleClass("disable"),
        $(".search_button_mobile").toggleClass("disable"),
        $(".search_input").focus()
    });
    $(".search_block_close").click(function(){return $(".search_block").toggleClass("vis"),
        $(".search_block_close").css({"display" : "none"}),
        $(".search_button_mobile").toggleClass("disable"),
        $(".logo").toggleClass("disable")
    
    });
    })
