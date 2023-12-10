var updateBtns = document.getElementsByClassName('update-btn')

for (var i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener('click', function() {
    var action = this.dataset.action;
    var productId = this.dataset.product;

  var data = {
    'productId': productId,
    'action': action,
  }

  submitUserData(data)
  })
}



function submitUserData(data) {
  var url = '/update_order/'

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify(data)
  })
  .then((response) => {return response.json()})
  
  location.reload()
}