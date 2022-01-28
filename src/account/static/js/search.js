const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

document.body.addEventListener("click", function(event){
    if (event.target.id == "subscriptions_user_w"){
      data = {
        id: event.target.attributes[1].textContent,
        status: false
      }
      fetch("/profile/subscription/", {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json',
          "X-CSRFToken": csrftoken },
        })
       .then(response => response.json())
       .then(data => {
         console.log(data['status'])
        if (data['status'] == 'ok'){
          event.target.textContent = 'Subscribe';
          event.target.classList.remove('btn-outline-secondary');
          event.target.classList.add('btn-danger');
          event.target.id = 'subscribe_user_w';
        }
       })
    } else if (event.target.id == "subscribe_user_w"){
      data = {
        id: event.target.attributes[1].textContent,
        status: true
      }
      fetch("/profile/subscription/", {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json',
          "X-CSRFToken": csrftoken },
        })
       .then(response => response.json())
       .then(data => {
         console.log(data['status'])
        if (data['status'] == 'ok'){
          event.target.textContent = 'Subscriptions';
          event.target.classList.remove('btn-danger');
          event.target.classList.add('btn-outline-secondary');
          event.target.id = 'subscriptions_user_w';
        }
       })
    }
});