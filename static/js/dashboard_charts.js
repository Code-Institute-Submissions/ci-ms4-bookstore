$(document).ready(function () {
    let ctx = document.getElementById("dashboardChart")
    let PRODUCTS_URL = '/rest-api/products/'
    let ORDERS_URL = '/rest-api/orders/'   
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    let labels = []
    let dataSet = []
    let colors = []

    // Generates random rgba colors for the chart 

    let colRandom = () => Math.random() * 256 >> 0;

    // Sets up the CSRF token being passed to the API

    const request = new Request(
        PRODUCTS_URL,
        {headers: {'X-CSRFToken': csrftoken}}
    );

    fetch(request, {
        method: 'GET',
        mode: 'same-origin'})
        .then(
        response => response.json())
        .then(data =>  {   
        
        let fetchDataResult = data.results


        fetchDataResult.forEach(item => {
            

            dataSet.push(item.upvote)
            labels.push(item.title)
            colors.push(`rgba(${colRandom()}, ${colRandom()}, ${colRandom()}, 0.2)`)           
    })

    let dashChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: '# of Upvotes',
                data: dataSet,
                backgroundColor: colors,
            }]
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
    });
});