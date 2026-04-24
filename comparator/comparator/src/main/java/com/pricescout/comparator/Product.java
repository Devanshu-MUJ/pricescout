package com.pricescout.comparator;

import jakarta.persistence.*;

@Entity
@Table(name = "products")
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private String brand;
    private Double amazonPrice;
    private Double flipkartPrice;

    public Product() {}

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getBrand() { return brand; }
    public void setBrand(String brand) { this.brand = brand; }
    public Double getAmazonPrice() { return amazonPrice; }
    public void setAmazonPrice(Double amazonPrice) { this.amazonPrice = amazonPrice; }
    public Double getFlipkartPrice() { return flipkartPrice; }
    public void setFlipkartPrice(Double flipkartPrice) { this.flipkartPrice = flipkartPrice; }
}