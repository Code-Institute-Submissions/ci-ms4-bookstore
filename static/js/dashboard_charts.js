$(document).ready(function () {
    let ctx = document.getElementById("dashboardChart")
    let PRODUCTS_URL = '/rest-api/products/'
    let ORDERS_URL = '/rest-api/orders/'   

    let labels = []
    let dataSet = []
    let colors = []

    // Generates random rgba colors for the chart 

    let colRandom = () => Math.random() * 256 >> 0;

    fetch(PRODUCTS_URL).then(
        response => response.json())
        .then(data =>  {   
        
        let fetchDataResult = data.results


        fetchDataResult.forEach(item => {
            

            dataSet.push(item.upvote)
            labels.push(item.title)
            colors.push(`rgba(${colRandom()}, ${colRandom()}, ${colRandom()}, 0.2)`)           
    })

    console.log(colors) 
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