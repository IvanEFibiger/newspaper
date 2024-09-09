
    $(document).ready(function(){
        $('.carousel').slick({
            slidesToShow: 4,
            slidesToScroll: 4,
            dots: false,
            infinite: false,
            prevArrow: $('#prevBtn'),
            nextArrow: $('#nextBtn'),
            responsive: [
                {
                    breakpoint: 768,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1
                    }
                }
            ]
        });
    });




    window.addEventListener('DOMContentLoaded', () => {
        obtenerClima();
      });
    
      function obtenerClima() {
        var ciudad = 'Villalonga'; // Ciudad y código de país (ISO 3166-1 alpha-2)
        var apiKey = '00707ce62c0cff539047016f49f8ba0a';
        var endpoint = 'https://api.openweathermap.org/data/2.5/weather?q=' + ciudad + '&appid=' + apiKey;
    
        fetch(endpoint)
          .then(response => response.json())
          .then(data => {
            var weatherIcon = document.getElementById("weatherIcon");
            var weatherTemp = document.getElementById("weatherTemp");
    
            weatherIcon.src = 'http://openweathermap.org/img/wn/' + data.weather[0].icon + '.png';
            weatherTemp.textContent = (data.main.temp - 273.15).toFixed(1) + " ℃";
          })
          .catch(error => {
            console.error('Error al obtener el clima:', error);
            alert('No se pudo obtener el clima para la ciudad especificada.');
          });
      }


      document.addEventListener('DOMContentLoaded', function() {
        const modoBtn = document.getElementById('modoBtn');
        const body = document.body;
      
        // Escuchar el clic en el botón
        modoBtn.addEventListener('click', function() {
          // Cambiar entre modo claro y oscuro
          if (body.classList.contains('light-mode')) {
            body.classList.remove('light-mode');
            body.classList.add('dark-mode');
            modoBtn.textContent = 'Modo Claro';
          } else {
            body.classList.remove('dark-mode');
            body.classList.add('light-mode');
            modoBtn.textContent = 'Modo Oscuro';
          }
        });
      });
      