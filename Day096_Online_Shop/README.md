# Day 96 - Online Shop

## Overview
A simple Flask e-commerce site with 9 tech products, session-based shopping cart, async add-to-cart via fetch API, and a mock checkout with tax calculation.

## Features
- Product gallery with images, categories, and prices
- Session-based cart (no login required)
- Async add-to-cart with button feedback animation
- Cart page with item list, quantities, and totals
- Checkout with 13% HST calculation and confirmation
- Bootstrap 5 dark theme

## Key Concepts
- Flask sessions for cart state
- fetch() API for async cart operations
- JavaScript DOM manipulation for UI feedback
- Template inheritance with Bootstrap

## Reflection
Using `session` for the cart is simpler than a database and perfect for a demo shop. The fetch-based add-to-cart avoids full page reloads and feels responsive. Real production shops would need inventory management, user accounts, and payment processing — but the core UX pattern is solid.

**Day 96 Complete!** ✅
