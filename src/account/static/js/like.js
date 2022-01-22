   const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

   const like = document.getElementById('like')
   like.onclick = () => {
       let id = like.attributes[1].textContent
       let action = like.attributes[2].textContent
       let total = like.attributes[3].textContent
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
            like.attributes[2].textContent = 'unlike';    
            like.classList.remove('btn-outline-secondary');
            like.classList.add('btn-danger');
            like.innerHTML = 'Like ' + (Number(total) + 1);
           }
           if (action === 'unlike'){
            like.attributes[2].textContent = 'like';    
            like.classList.remove('btn-danger');
            like.classList.add('btn-outline-secondary');
            like.innerHTML = 'Like ' + (Number(total) - 1);
           }
         }
       });
   };
