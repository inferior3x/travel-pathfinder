package com.coco3x.travelpathfinder.service;

import com.coco3x.travelpathfinder.domain.entity.Departure;
import com.coco3x.travelpathfinder.domain.repository.DepartureRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class DepartureService {
    private final DepartureRepository departureRepository;

    public List<Departure> getList(){
        return departureRepository.findAll();
    }
    public boolean isExistingDeparture(String name) {
        return (departureRepository.findByName(name).orElse(null) != null);
    }
}
