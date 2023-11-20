package com.coco3x.travelpathfinder.service;

import com.coco3x.travelpathfinder.domain.entity.Destination;
import com.coco3x.travelpathfinder.domain.repository.DestinationRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class DestinationService {
    private final DestinationRepository destinationRepository;

    public List<Destination> getList(){
        return destinationRepository.findAll();
    }

    public boolean isExistingDestination(String name) {
        return (destinationRepository.findByName(name).orElse(null) != null);
    }
}
