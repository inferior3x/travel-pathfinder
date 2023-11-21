var map;

var lodging = { lat: 35.6273033, lng: 139.7948661 }; //숙소
//지도 초기화 - 자동 실행
function initMap() {
  //지도 초기화(생성)
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 15,
    center: lodging,
  });

  var lodgingMarker = new google.maps.Marker({
    position: lodging,
    map: map,
    label: {
      text : "숙소",
      fontWeight: "bold",
      fontSize: "17px",
    },
    zIndex: 999
  });

  var placeMarkerPoint1 = { lat: 48.8606111, lng: 2.337644 };
  var placeMarker = new google.maps.Marker({
    position: placeMarkerPoint1,
    map: map,
    label: {
      text : "관광지1",
      fontWeight: "bold",
      fontSize: "17px",
    },
    icon: {
      url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
    },
  });

  var placeMarkerPoint2 = { lat: 48.8737917, lng: 2.2950275 };
  var placeMarker = new google.maps.Marker({
    position: placeMarkerPoint2,
    map: map,
    label: {
      text : "관광지2",
      fontWeight: "bold",
      fontSize: "17px",
    },
    icon: {
      url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png",

    },
  });

  displayRoute(lodging, placeMarkerPoint1);
  displayRoute(placeMarkerPoint1, placeMarkerPoint2);
  displayRoute(placeMarkerPoint2, lodging)

}





function displayRoute(origin, destination) {
  var directionsService = new google.maps.DirectionsService();
  var directionsRenderer = new google.maps.DirectionsRenderer({
    suppressMarkers: true // 마커 숨기기
  });

  directionsRenderer.setMap(map);

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
  var geocoder = new google.maps.Geocoder();
  geocoder.geocode({ address: address }, function (results, status) {
    if (status === "OK") {
      var location = results[0].geometry.location;
      var lat = location.lat();
      var lng = location.lng();
      console.log("주소: " + address);
      console.log("위도: " + lat);
      console.log("경도: " + lng);
    } else {
      console.error("지오코딩에 실패했습니다: " + status);
    }
  });
}






var button = document.getElementById("map_button");
button.addEventListener("click", changeCenter);
function changeCenter() {
  //설정한 위치로 지도를 다시 이동시킴

  map.panTo(lodging);
  map.setZoom(15);
}