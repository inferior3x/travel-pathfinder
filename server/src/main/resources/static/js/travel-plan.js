window.addEventListener('DOMContentLoaded', async()=>{
    showSpinner();
    await fetchByPost("/travel-plan",
        convertQueryStringToJson(),
        async (responseData) => {
            if (!responseData.success){
                showOkModal(responseData.message,
                    ()=> {window.location.href = "/travel-info.js";}
                    )
            }
            document.getElementById("hotel-name").textContent = "호텔 이름: " + responseData.hotel.name;
            document.getElementById("hotel-price").textContent = "호텔 가격: " + responseData.hotel.price;
            document.getElementById("hotel-price").textContent = "호텔 주소: " + responseData.hotel.address;

            document.getElementById("departure-airline").textContent = "항공사: " + responseData.flights.departure.airline;
            document.getElementById("departure-start-time").textContent = "출발 시간: " + responseData.flights.departure.start_time;
            document.getElementById("departure-start-airport").textContent = "출발 공항: " + responseData.flights.departure.start_airport;
            document.getElementById("departure-end-time").textContent = "도착 시간: " + responseData.flights.departure.end_time;
            document.getElementById("departure-end-airport").textContent = "도착 공항: " + responseData.flights.departure.end_airport;
            document.getElementById("departure-time-required").textContent = "소요 시간: " + responseData.flights.departure.time_required;

            document.getElementById("return-airline").textContent = "항공사: " + responseData.flights["return"].airline;
            document.getElementById("return-start-time").textContent = "출발 시간: " + responseData.flights["return"].start_time;
            document.getElementById("return-start-airport").textContent = "출발 공항: " + responseData.flights["return"].start_airport;
            document.getElementById("return-end-time").textContent = "도착 시간: " + responseData.flights["return"].end_time;
            document.getElementById("return-end-airport").textContent = "도착 공항: " + responseData.flights["return"].end_airport;
            document.getElementById("return-time-required").textContent = "소요 시간: " + responseData.flights["return"].time_required;

            const days = 1;

            const destinations = []; //{위도: , 경도: } 배열
            let hotel;
            if (responseData.hotel !== undefined){
                hotel = await geocodeAddress(responseData.hotel.address);
            }else{
                hotel = {lat: 35.713428400000012, lng: 139.796664}; //도쿄
            }


            destinations.push(hotel);// 숙소 첫 번째에 넣기
            for(const attraction of responseData.attractions){
                const destination = await geocodeAddress(attraction.address);
                if ((Math.abs(destination.lat - hotel.lat) > 3) || (Math.abs(destination.lng - hotel.lng) > 3)) {
                    console.log("유효하지 않은 관광지");
                    continue;
                }
                destinations.push(destination);
                if (destinations.length === (responseData.attractions.length/2 + 1))
                    break;
            }

            const matrix = await calculateDistanceMatrix(destinations);

            console.log(responseData.attractions);
            console.log(destinations);
            console.log(matrix);

            const routes = savings_algorithm(days, matrix);
            console.log(routes);

            for(const [i, route] of routes.entries()){
                const newMapElement = document.createElement('div');
                newMapElement.id = `map${i}`;
                newMapElement.style.height = "600px";
                document.body.appendChild(newMapElement);


                initMap(i, "숙소", hotel);
                let pre = 0;
                for(let j = 1; j < route.length ; j++) {
                    displayRoute(i, destinations[pre], destinations[route[j]]);
                    if (route[j] != 0) {
                        markPlaceInMap(i, `${route[j] - 1} - ${responseData.attractions[route[j] - 1].name}`, destinations[route[j]]);
                    }
                    pre = route[j];
                }
            }

        },
        () => {},
    );

    hideSpinner();
});
