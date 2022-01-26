const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

const total_subscribe = document.getElementById('total_subscription');
const total_followers = document.getElementById('total_followers');
total_fol = total_followers.attributes[2].nodeValue;
total = total_subscribe.attributes[2].nodeValue;

document.body.addEventListener("click", function(event){
    if (event.target.id == "subscriptions"){
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
          event.target.id = 'subscribe';
          total_subscribe.innerHTML = 'Subscription ' + (Number(total) - 1);
          total = (Number(total) - 1);
        }
       })
    } else if (event.target.id == "subscribe"){
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
          event.target.id = 'subscriptions';
          total_subscribe.innerHTML = 'Subscription ' + (Number(total) + 1);
          total = (Number(total) + 1);
        }
       })
    } else if (event.target.id == "subscriptions_user"){
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
          event.target.id = 'subscribe_user';
          total_followers.innerHTML = 'Followers ' + (Number(total_fol) - 1);
          total_fol = (Number(total_fol) - 1);
        }
       })
    }  else if (event.target.id == "subscribe_user"){
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
          event.target.id = 'subscriptions_user';
          total_followers.innerHTML = 'Followers ' + (Number(total_fol) + 1);
          total_fol = (Number(total_fol) + 1);
        }
       })
    } else if (event.target.id == "subscriptions_user_w"){
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
