document.querySelectorAll(".add-to-cart").forEach(function(btn) {
    btn.addEventListener("click", function() {
        var id = this.dataset.id;
        fetch("/api/cart/add", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ product_id: parseInt(id) })
        })
        .then(function(r) { return r.json(); })
        .then(function(data) {
            var badge = document.getElementById("cart-badge");
            if (badge) badge.textContent = data.cart_count;
            btn.innerHTML = '<i class="fa-solid fa-check me-1"></i>Added!';
            btn.classList.add("btn-success");
            btn.classList.remove("btn-outline-light");
            setTimeout(function() {
                btn.innerHTML = '<i class="fa-solid fa-cart-plus me-1"></i>Add to Cart';
                btn.classList.remove("btn-success");
                btn.classList.add("btn-outline-light");
            }, 1500);
        });
    });
});

document.querySelectorAll(".remove-from-cart").forEach(function(btn) {
    btn.addEventListener("click", function() {
        var id = this.dataset.id;
        fetch("/api/cart/remove", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ product_id: parseInt(id) })
        })
        .then(function() { location.reload(); });
    });
});
