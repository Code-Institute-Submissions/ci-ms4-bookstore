$(document).ready(function () {
    let ctx = document.getElementById("dashboardChart")
    let PRODUCTS_URL = '/rest-api/products/'
    let ORDERS_URL = '/rest-api/orders/'   
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Globally scoping these variables on initialization.

    let labels = []
    let dataSetUpvote = []
    let dataSetDownvote = []
    let dataSetPrice = []

    // Generates random rgba colors for the chart 

    let colRandom = () => Math.random() * 256 >> 0;

    // Sets up the CSRF token being passed to the API

    const request = new Request(
        PRODUCTS_URL,
        {headers: {'X-CSRFToken': csrftoken}}
    );


    // On load performs a fetch request for the first 10 items in the Products category. Add pagination.

    fetch(request, {
        method: 'GET',
        mode: 'same-origin'})
        .then(
        response => response.json())
        .then(data =>  {   
        
        let fetchDataResult = data.results

        fetchDataResult.forEach(item => {
            dataSetPrice.push(item.price)
            dataSetUpvote.push(item.upvote)
            dataSetDownvote.push(item.downvote)
            labels.push(item.title)  
        });
    });

    // Chart that loads on loading the page.
    let dashChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: []
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });


    // Functionality for adding more datasets to the chart and updating it

    function addDataSet(chart, label, colors, data) {

		chart.data.datasets.push({
	    label: label,
        backgroundColor: colors,
        data: data
    });
    chart.update();
    }   

    function removeData(chart) {
        chart.data.labels.pop();
        chart.data.datasets.forEach((dataset) => {
            dataset.data.pop();
        });
    }

    // Event listeners for adding / removing data from the Chart object. Randomizing colours for each new dataset, to make separations clearer.

    $('#redrawChartBtn').click(() => { 

        let dashChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: []
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });       

        removeData(dashChart)

        // Conditional logic to check what datasets to draw.

        if ($('#upvotesCheck').prop('checked')) {
            let colors = []

            dataSetUpvote.forEach(item = () =>{
                colors.push(`rgba(${colRandom()}, ${colRandom()}, ${colRandom()}, 0.5)`)
            });
            addDataSet(dashChart, '# of Upvotes', colors ,dataSetUpvote);
        };
        if ($('#downvotesCheck').prop('checked')) {
            let colors = []

            dataSetDownvote.forEach(item = () =>{
                colors.push(`rgba(${colRandom()}, ${colRandom()}, ${colRandom()}, 0.5)`)
            });
            addDataSet(dashChart, '# of Downvotes', colors ,dataSetDownvote);
        };

        if ($('#priceCheck').prop('checked')) {
            let colors = []

            dataSetPrice.forEach(item = () =>{
                colors.push(`rgba(${colRandom()}, ${colRandom()}, ${colRandom()}, 0.5)`)
            });
            addDataSet(dashChart, 'Item price ( In $ )', colors, dataSetPrice);
        };
        
        
        dashChart.update()
        
        
    });

    $('#downvotesCheck').change(() => {        
        let checkBox = $('#downvotesCheck')
        
        checkBox.attr("checked", !checkBox.attr("checked"));                
    });

    $('#upvotesCheck').change(() => { 
        let checkBox = $('#upvotesCheck')
        
        checkBox.attr("checked", !checkBox.attr("checked"));    
    });

    $('#priceCheck').change(() => { 
        let checkBox = $('#priceCheck')
        
        checkBox.attr("checked", !checkBox.attr("checked"));  
    });
});