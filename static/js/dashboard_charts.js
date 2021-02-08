$(document).ready(function () {
    let ctx = document.getElementById("dashboardChart")
    let PRODUCTS_URL = '/rest-api/products/'
    let ORDERS_URL = '/rest-api/orders/'   
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

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


    // Sorts the original data from the fetch-request.

    fetch(request, {
        method: 'GET',
        mode: 'same-origin'})
        .then(
        response => response.json())
        .then(data =>  {   
        
        let fetchDataResult = data.results

        fetchDataResult.forEach(item => {
            console.log(item)
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


    // Functionality for adding datasets to the chart and updating it

    function addDataSet(chart, label, colors, data) {

		chart.data.datasets.push({
	    label: label,
        backgroundColor: colors,
        data: data
    });
    chart.update();
    }   

    // Event listeners for adding / removing data from the Chart object. Randomizing colours for each new dataset, to make separations clearer.

    $('#downvotesCheck').change(function (e) {        
        
        let colors = []
        dataSetDownvote.forEach(item = () =>{
            colors.push(`rgba(${colRandom()}, ${colRandom()}, ${colRandom()}, 0.5)`)
        });
        
        addDataSet(dashChart, '# of Downvotes', colors ,dataSetDownvote);
    });

    $('#upvotesCheck').change(function (e) { 
        
        let colors = []
        dataSetDownvote.forEach(item = () =>{
            colors.push(`rgba(${colRandom()}, ${colRandom()}, ${colRandom()}, 0.5)`)
        });

        addDataSet(dashChart, '# of Upvotes', colors, dataSetUpvote);
    });

    $('#priceCheck').change(function (e) { 

        let colors = []
        dataSetPrice.forEach(item = () =>{
            colors.push(`rgba(${colRandom()}, ${colRandom()}, ${colRandom()}, 0.5)`)
        });
        console.log(dataSetPrice)
        addDataSet(dashChart, 'Item price ( In $ )', colors, dataSetPrice);
    });
});