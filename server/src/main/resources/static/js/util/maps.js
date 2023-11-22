var maps = [];

//지도 초기화
function initMap(i, placeName, center) {
  //지도 초기화(생성)
  maps[i] = new google.maps.Map(document.getElementById(`map${i}`), {
    zoom: 15,
    center: center,
  });

  var lodgingMarker = new google.maps.Marker({
    position: center,
    map: maps[i],
    label: {
      text : placeName,
      fontWeight: "bold",
      fontSize: "17px",
    },
    zIndex: 999
  });
}

//맵에 마커 추가
function markPlaceInMap(i, placeName, place){
  new google.maps.Marker({
    position: place,
    map: maps[i],
    label: {
      text : placeName,
      fontWeight: "bold",
      fontSize: "17px",
    },
    icon: {
      url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
    },
  });
}

async function calculateDistanceMatrix(destinations) {
  const service = new google.maps.DistanceMatrixService();

  const request = {
    origins: destinations,
    destinations: destinations,
    travelMode: google.maps.TravelMode.DRIVING,
    unitSystem: google.maps.UnitSystem.METRIC,
    avoidHighways: false,
    avoidFerries: false,
    avoidTolls: false,
  };
  const matrix = [];

  const response = await service.getDistanceMatrix(request);
  // 거리 행렬 결과 처리
  for (let i = 0; i < destinations.length; i++) {
    matrix[i] = [];
    for (let j = 0; j < destinations.length; j++) {
      matrix[i][j] = response.rows[i].elements[j].duration.value; // 소요 시간 정보
    }
  }

  return matrix;
}

function displayRoute(i, origin, destination) {
  var directionsService = new google.maps.DirectionsService();
  var directionsRenderer = new google.maps.DirectionsRenderer({
    suppressMarkers: true // 마커 숨기기
  });

  directionsRenderer.setMap(maps[i]);

  var request = {
    origin: origin,
    destination: destination,
    travelMode: google.maps.TravelMode.DRIVING, // 차량 이동을 기준
  };
  directionsService.route(request, function (result, status) {
    if (status == google.maps.DirectionsStatus.OK) {
      directionsRenderer.setDirections(result);
      
      // 소요 시간 정보 얻기
      var route = result.routes[0];
      var duration = 0;
      for (var i = 0; i < route.legs.length; i++) {
        duration += route.legs[i].duration.value;
      }
      // 소요 시간을 분 단위로 변환하고 표시
      var durationInMinutes = Math.ceil(duration / 60);
      console.log("Estimated travel time: " + durationInMinutes + " minutes");

    } else {
      console.error("경로를 가져오지 못했습니다: " + status);
    }
  });
}

//주소를 위도와 경도로 변환
function geocodeAddress(address) {
  return new Promise((resolve, reject) => {
    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ address: address }, function (results, status) {
      if (status === "OK") {
        const location = results[0].geometry.location;
        resolve({lat: location.lat(), lng: location.lng()}); // 성공 시 Promise를 이용해 값을 반환
      } else {
        console.log(address, "지오코딩 실패");
        reject("지오코딩 실패"); // 실패 시 Promise를 이용해 에러를 반환
      }
    });
  });
}