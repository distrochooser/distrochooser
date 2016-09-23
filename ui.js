$('#about').on('shown.bs.modal', function () {     		
    var label = [];
    var testData = [];
    var hitData = [];	

    var stats = vm.testCount;		
    for (var i = stats.length - 1; i >= 0; i--) {
        label.push(stats[i].MONTH + "/" +new Date().getFullYear());
        testData.push(parseInt(stats[i].count));
        hitData.push(parseInt(stats[i].hits));
    };
    var chartData = {
    labels : label,
    datasets : [
        {
            data : testData,
            label: "Tests",
            pointBorderColor: "rgba(75,192,192,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(75,192,192,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10
        },{
            data : hitData,
            label: "Hits",
            pointBorderColor: "rgba(75,192,192,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(75,192,192,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
            borderColor:"#cf7777",
            borderWidth: "3px"
        }
    ]};
    var tests = document.getElementById('testCountCanvas').getContext('2d');
    new Chart(tests, {
        type:"line",
        data:chartData
    });	        				
}); 