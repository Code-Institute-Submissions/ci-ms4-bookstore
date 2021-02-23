    // Globally scoping these variables on initialization
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const pk = document.querySelector('[name=item_pk').value;
    let PRODUCTS_URL = '/rest-api/products/';

    const product_request = new Request(
        PRODUCTS_URL+pk,
        {headers: {'X-CSRFToken': csrftoken}}
        
    );

$(document).ready(() => {   

    fetch(product_request, {
        method: 'GET',
        mode: 'same-origin'})
        .then(
        response => response.json())
        .then(data =>  {   
        let UPVOTES = data.upvote;
        let DOWNVOTES = data.downvote;

  let ctx = document.getElementById("reviewChart")
  let reviewChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Positive', 'Negative'],
      datasets: [{
        label: 'Positive and Negative votes',
        data: [UPVOTES, DOWNVOTES],
        backgroundColor: [
            'rgba(0, 214, 57, 0.2)',
            'rgba(240, 14, 14, 0.2)'],
        borderColor: [
            'rgba(47, 74, 58, 1)',
            'rgba(255, 94, 94, 1)'],
        borderWidth: 1
        }]
    },
    options: {
      responsive: true,
      cutoutPercentage: 25
  }
  });
  reviewChart.update()
    });
});
