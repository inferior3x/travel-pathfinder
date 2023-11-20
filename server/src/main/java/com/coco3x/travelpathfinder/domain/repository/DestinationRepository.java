package com.coco3x.travelpathfinder.domain.repository;

import com.coco3x.travelpathfinder.domain.entity.Departure;
import com.coco3x.travelpathfinder.domain.entity.Destination;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface DestinationRepository extends JpaRepository<Destination, Long> {
    Optional<Destination> findByName(String name);
}
