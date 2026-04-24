package com.pricescout.comparator;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@Controller
public class ProductController {

    private final ProductRepository repository;

    public ProductController(ProductRepository repository) {
        this.repository = repository;
    }

    // 1. Home Page & Search Results
    @GetMapping("/")
    public String index(@RequestParam(value = "query", required = false) String query, Model model) {
        if (query != null && !query.isEmpty()) {
            List<Product> results = repository.findByNameContainingIgnoreCase(query);
            model.addAttribute("results", results);
            model.addAttribute("query", query);
        }
        return "index";
    }

    // 2. Show Add Product Form
    @GetMapping("/admin/add")
    public String showAddForm(Model model) {
        model.addAttribute("product", new Product());
        return "add-product";
    }

    // 3. Save Product to Database
    @PostMapping("/admin/save")
    public String saveProduct(@ModelAttribute Product product) {
        repository.save(product);
        return "redirect:/"; // Redirects to home to see the new item
    }
}