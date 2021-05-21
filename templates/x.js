var timer;
  function startTimer() {
    timer = setInterval(function() { 
        x = fetch("http://localhost:5000/restapi/admin/views").then(function (response) {
            document.getElementById('views').innerHTML = response.body;
          }) 
    }, 5000);
    }