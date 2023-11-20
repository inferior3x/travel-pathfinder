package com.coco3x.travelpathfinder.domain.repository;

import com.coco3x.travelpathfinder.domain.entity.Departure;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface DepartureRepository extends JpaRepository<Departure, Long> {
    Optional<Departure> findByName(String name);
}