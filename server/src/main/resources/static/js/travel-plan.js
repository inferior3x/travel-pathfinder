window.addEventListener('DOMContentLoaded', async()=>{
    showSpinner();
    await fetchByPost("/travel-plan",
        convertQueryStringToJson(),
        (responseData) => {
            document.getElementById("hotel-name").textContent = "호텔 이름: " + responseData.hotel.name;
            document.getElementById("hotel-price").textContent = "호텔 가격: " + responseData.hotel.price;

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
            // data = responseData;
        },
        () => {},
    );

    hideSpinner();
});


// geocodeAddress("3-11-1, Ariake, 고토, 도쿄, 도쿄도, 관동, 일본");
