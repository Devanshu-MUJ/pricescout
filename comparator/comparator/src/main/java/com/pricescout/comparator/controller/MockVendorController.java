package com.pricescout.comparator.controller;

import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
@RequestMapping("/api/vendors")
public class MockVendorController {

    @GetMapping("/search")
    public List<Map<String, Object>> getVendorData(@RequestParam String item) {
        List<Map<String, Object>> results = new ArrayList<>();
        String search = item.toLowerCase();

        // 5 Items for your demo: iPhone, Samsung, Sony, Macbook, iPad
        if (search.contains("iphone")) {
            results.add(createData("ElectroStore", 79900, 4.9, "Apple Warranty"));
            results.add(createData("QuickShop", 69500, 4.2, "Flash Sale - 10k Off"));
            results.add(createData("GadgetHub", 74000, 4.5, "Exchange Available"));
        } 
        else if (search.contains("samsung") || search.contains("s24")) {
            results.add(createData("ElectroStore", 74999, 4.7, "Free Buds 2"));
            results.add(createData("QuickShop", 71000, 4.4, "Instant 4k Discount"));
            results.add(createData("GadgetHub", 73500, 4.6, "Fast Delivery"));
        } 
        else if (search.contains("sony") || search.contains("wh")) {
            results.add(createData("ElectroStore", 29990, 5.0, "Premium Box"));
            results.add(createData("QuickShop", 26500, 4.5, "Bank Offers"));
            results.add(createData("GadgetHub", 28000, 4.8, "Limited Stock"));
        }
        else if (search.contains("macbook")) {
            results.add(createData("ElectroStore", 89900, 4.9, "Student Discount"));
            results.add(createData("QuickShop", 82000, 4.3, "No Cost EMI"));
            results.add(createData("GadgetHub", 85500, 4.7, "Free Sleeve"));
        }
        else if (search.contains("ipad")) {
            results.add(createData("ElectroStore", 45000, 4.8, "Pencil Bundle"));
            results.add(createData("QuickShop", 39999, 4.1, "Clearance Sale"));
            results.add(createData("GadgetHub", 42000, 4.4, "Next Day Shipping"));
        }
        else {
            results.add(createData("ElectroStore", 0, 0, "Check Store"));
            results.add(createData("QuickShop", 0, 0, "Check Store"));
            results.add(createData("GadgetHub", 0, 0, "Check Store"));
        }

        return results;
    }

    private Map<String, Object> createData(String site, double price, double rating, String offer) {
        Map<String, Object> data = new HashMap<>();
        data.put("site", site);
        data.put("price", price);
        data.put("rating", rating);
        data.put("offer", offer);
        return data;
    }
}