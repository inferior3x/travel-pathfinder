package com.coco3x.travelpathfinder.controller;

import com.coco3x.travelpathfinder.domain.entity.Departure;
import com.coco3x.travelpathfinder.domain.entity.Destination;
import com.coco3x.travelpathfinder.domain.dto.request.TravelPlanRequestDTO;
import com.coco3x.travelpathfinder.service.DepartureService;
import com.coco3x.travelpathfinder.service.DestinationService;
import com.coco3x.travelpathfinder.util.Crawler;
import com.coco3x.travelpathfinder.util.DateCalculator;
import com.fasterxml.jackson.databind.util.JSONPObject;
import lombok.RequiredArgsConstructor;
import org.apache.tomcat.util.json.JSONFilter;
import org.json.JSONObject;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.List;

@RequiredArgsConstructor
@RestController
public class TravelRestController {
    private final DepartureService departureService;
    private final DestinationService destinationService;
    private final Crawler crawler;

    //출발지 요청
    @GetMapping("/departure-place")
    public List<Departure> sendDeparturePlace(){
        return departureService.getList();
    }

    //도착지 요청
    @GetMapping("/travel-place")
    public List<Destination> sendTravelPlace(){
        return destinationService.getList();
    }

    //경로 계산 요청
    @PostMapping("/travel-plan")
    public String sendTravelPlan(@RequestBody @Valid TravelPlanRequestDTO travelPlanRequestDTO){
        //출발지와 도착지를 골랐는지 확인
        if (!departureService.isExistingDeparture(travelPlanRequestDTO.getDeparturePlace()) || //출발지가 db에 없을 경우
                !destinationService.isExistingDestination(travelPlanRequestDTO.getDestination())){ //도착지가 db에 없을 경우
            //"출발지 혹은 도착지를 선택하세요"
        }

        //날짜인지 확인하는 로직 추가하기

        //2박 3일 이상인지 확인
        if (DateCalculator.calculateDateDifference(
                travelPlanRequestDTO.getDepartureDate(),
                travelPlanRequestDTO.getReturnDate())
                < 2){
            //"최소 2박 3일부터 가능합니다."
        }

        //관광지 개수, 객실과 인원이 숫자이며 1이상 자연수인지 확인하는 로직 추가하기, 관광지는 30개 이하

        //객실 개수 <= 인원 확인
        if (Integer.parseInt(travelPlanRequestDTO.getRoomNumber()) >
                Integer.parseInt(travelPlanRequestDTO.getTravelerNumber())){
            //"객실 개수보다 인원 수가 더 많아야 합니다."
        }

        //비행기, 호텔, 관광지 가져오기
        JSONObject jsonObject = new JSONObject(travelPlanRequestDTO); //명령어로 만들 json 객체 생성
        jsonObject.put("cmd", "plan"); //출발지, 도착지, 가는 날짜/오는 날짜, 사람 수 / 객실 수
        return crawler.command(jsonObject.toString());
    }
}