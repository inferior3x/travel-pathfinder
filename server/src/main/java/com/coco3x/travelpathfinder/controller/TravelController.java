package com.coco3x.travelpathfinder.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@Controller
public class TravelController {
    @GetMapping("/travel-info")
    void goToTravelInfo(){}
    @GetMapping("/travel-plan")
    void goToTravelPlan(){}
}