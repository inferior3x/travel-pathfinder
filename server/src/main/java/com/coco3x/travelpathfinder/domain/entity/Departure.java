package com.coco3x.travelpathfinder.domain.entity;

import lombok.Getter;

import javax.persistence.*;

@Entity
@Getter
public class Departure {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;
}
