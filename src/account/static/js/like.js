   const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

   document.body.addEventListener("click", function(event){
    if (event.target.id == "like"){
      let id = event.target.attributes[1].textContent
      let action = event.target.attributes[2].textContent
      let total = event.target.attributes[3].textContent
      data = {
        id: id,
        action: action,
      }
      fetch("/image/like/", {
        method: 'POST',
        body: JSON.stringify(data),
        headers: { 
          'Content-Type': 'application/json',
          "X-CSRFToken": csrftoken },
        })
       .then(response => response.json())
       .then(data => {
        if (data['status'] == 'ok'){
           console.log(data)
          if (action === 'like'){
            event.target.attributes[2].textContent = 'unlike';    
            event.target.classList.remove('btn-outline-secondary');
            event.target.classList.add('btn-danger');
            event.target.innerHTML = 'Like ' + (Number(total) + 1);
          }
          if (action === 'unlike'){
            event.target.attributes[2].textContent = 'like';    
            event.target.classList.remove('btn-danger');
            event.target.classList.add('btn-outline-secondary');
            event.target.innerHTML = 'Like ' + (Number(total) - 1);
          }
        }
      });
    }
   });
