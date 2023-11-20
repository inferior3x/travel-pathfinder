package com.coco3x.travelpathfinder.util;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

public class DateCalculator {
    public static long calculateDateDifference(String departureDate, String returnDate){
        LocalDate startDate = LocalDate.parse(departureDate);
        LocalDate endDate = LocalDate.parse(returnDate);

        // 두 날짜 사이의 차이를 계산하여 반환
        return ChronoUnit.DAYS.between(startDate, endDate);
    }
}
