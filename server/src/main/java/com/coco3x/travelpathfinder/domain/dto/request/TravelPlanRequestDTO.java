package com.coco3x.travelpathfinder.domain.dto.request;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import lombok.Getter;
import lombok.NoArgsConstructor;
import javax.validation.constraints.NotEmpty;

@NoArgsConstructor
@Getter
@JsonNaming(value = PropertyNamingStrategies.KebabCaseStrategy.class)
public class TravelPlanRequestDTO {
    @NotEmpty
    private String departurePlace;
    private String destination;
    private String departureDate;
    private String returnDate;
    private String travelerNumber;
    private String roomNumber;
    private String attractionNumber;

    @Override
    public String toString() {
        return "TravelPlanRequestDTO{" +
                "departurePlace='" + departurePlace + '\'' +
                ", travelPlace='" + destination+ '\'' +
                ", departureDate='" + departureDate + '\'' +
                ", returnDate='" + returnDate + '\'' +
                ", travelerNumber='" + travelerNumber + '\'' +
                ", roomNumber='" + roomNumber + '\'' +
                ", attractionNumber='" + attractionNumber + '\'' +
                '}';
    }
}