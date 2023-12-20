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
            document.getElementById("hotel-name").textContent = responseData.hotel.name;
            // document.getElementById("hotel-price").textContent = "가격: " + responseData.hotel.price;
            document.getElementById("hotel-address").textContent = responseData.hotel.address;

            document.getElementById("departure-airline").textContent =  responseData.flights.departure.airline;
            document.getElementById("departure-start-time").textContent =  responseData.flights.departure.start_time;
            document.getElementById("departure-start-airport").textContent =  responseData.flights.departure.start_airport;
            document.getElementById("departure-end-time").textContent =  responseData.flights.departure.end_time;
            document.getElementById("departure-end-airport").textContent =   responseData.flights.departure.end_airport;
            document.getElementById("departure-time-required").textContent =  responseData.flights.departure.time_required;

            document.getElementById("return-airline").textContent =  responseData.flights["return"].airline;
            document.getElementById("return-start-time").textContent =  responseData.flights["return"].start_time;
            document.getElementById("return-start-airport").textContent =  responseData.flights["return"].start_airport;
            document.getElementById("return-end-time").textContent = responseData.flights["return"].end_time;
            document.getElementById("return-end-airport").textContent = responseData.flights["return"].end_airport;
            document.getElementById("return-time-required").textContent = responseData.flights["return"].time_required;

            const days = 1;

        //받은 주소를 위도와 경도로 변환
            const destinations = []; //{위도: , 경도: } 배열
            let hotel;
            if (responseData.hotel !== undefined)
                try {
                    hotel = await geocodeAddress(responseData.hotel.address);
                }catch{
                    console.log("호텔 왜 지오코딩 안돼");
                }
            else
                hotel = {lat: 35.713428400000012, lng: 139.796664}; //도쿄

        //거리 행렬 구하기 - 관광지 간 이동 시간을 가짐
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

        //거리행렬을 최단 경로 알고리즘 함수에 전달하여 최단 경로 반환
            const matrix = await calculateDistanceMatrix(destinations);

            // console.log(responseData.attractions);
            // console.log(destinations);
            console.log(matrix);
            const bodyDataTSP = {};
            bodyDataTSP['matrix'] = matrix;
            bodyDataTSP['n'] = 3;


            // const routes = savings_algorithm(days, matrix);
            let routes;
            await fetchByPost("/travel-route",
                bodyDataTSP,
                async (responseData) => {
                    routes = responseData
                },
                () => {}
            )

            console.log(routes);

        //얻은 경로를 지도에 띄우기
            for(const [i, route] of routes.entries()){
                const newMapElement = document.createElement('div');
                newMapElement.id = `map${i}`;
                newMapElement.style.height = "600px";
                document.querySelector("#maps").appendChild(newMapElement);


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
