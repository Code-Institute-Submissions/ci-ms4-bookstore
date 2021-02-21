    // Globally scoping these variables on initialization as empty arrays.

    let labels = []
    let dataSetUpvote = []
    let dataSetDownvote = []
    let dataSetPrice = []


$(document).ready(() => {
    let ctx = document.getElementById("dashboardChart")
    let PRODUCTS_URL = '/rest-api/products/'
    let ORDERS_URL = '/rest-api/orders/'   
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


    // Checkbox handler for all checkboxes involved in the chart-filters

    const checkboxHandler = () => {
        $this = $(this)
        $this.attr("checked", !$this.attr("checked"));    
    };

    $(":checkbox").change(() => {
        checkboxHandler()
    });


    // Generates random rgba colors for the chart 

    const colRandom = () => Math.random() * 256 >> 0;

    // Sets up the CSRF token being passed to the API

    const product_request = new Request(
        PRODUCTS_URL,
        {headers: {'X-CSRFToken': csrftoken}}
    );

    const order_request = new Request(
        ORDERS_URL,
        {headers: {'X-CSRFToken': csrftoken}}
    );

    
    // On load performs a fetch request for the first 10 items in the Products category. Add pagination.

    fetch(product_request, {
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

    // Functionality for adding more datasets to the chart and updating it

    function addDataSet(chart, label, colors, data) {

		chart.data.datasets.push({
	    label: label,
        backgroundColor: colors,
        data: data
    });
    }   

    window.dashChart = new Chart(ctx, {
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

    // Event listeners for adding / removing data from the Chart object. Randomizing colours for each new dataset, to make separations clearer.

    $('#redrawChartBtn').click(() => { 

        // Specifying the chart as a window-variable is crucial, because otherwise the data is not cleared between refreshes.

        if(window.dashChart != undefined)
            window.dashChart.destroy();

            window.dashChart = new Chart(ctx, {
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


    // Order time-axis chart cut for time, just kept it for after assessment so I can pick up the work after.
    $('#orderAJAX').click(() =>{
        fetch(order_request, {
            method: 'GET',
            mode: 'same-origin'})
            .then(
            response => response.json())
            .then(data =>  {   
                let dateResults = data.results

                dateResults.forEach(result => {
                    let date = moment(result.date)
                    console.log(date)
                    
                });
            });
    });


});