function getCSRFToken() {
    return $('meta[name="csrf-token"]').attr('content');
}


function filterProducts() {
    let slider = document.getElementById('price-slider');
    let minPrice = slider.noUiSlider.get()[0];
    let maxPrice = slider.noUiSlider.get()[1];

    let category_checkboxes = document.querySelectorAll('#category-filter input:checked');
    let categories = [];
    category_checkboxes.forEach(function(checkbox) {
        let li = checkbox.parentElement;
        let categoryName = li.textContent.trim();
        categories.push(categoryName);
    });

    let brands_checkboxes = document.querySelectorAll('#brand-filter input:checked')
    let brands = [];
    brands_checkboxes.forEach(function(checkbox){
        let li = checkbox.parentElement;
        let brandName = li.textContent.trim();
        brands.push(brandName);
    })

    let availabilityFilter = document.querySelectorAll('#availability-filter input')[0].checked;

    // console.log(
    //     `
    //     minPrice: ${minPrice}\n
    //     maxPrice: ${maxPrice}\n
    //     categories: ${categories}\n
    //     brands: ${brands}\n
    //     availabilityFilter: ${availabilityFilter}
    //     `
    // );

    let products = document.querySelectorAll('.item');

    products.forEach(function(product) {
        let price = parseFloat(product.dataset.price);
        let category = product.dataset.category;
        let brand = product.dataset.brand;
        let availability = product.dataset.availability === "True";

        // alert(
        //     `
        //     price: ${price}\n
        //     category: ${category}\n
        //     brand: ${brand}\n
        //     availability: ${availability}
        //     `
        // );

        let display = true;

        if (price < minPrice || price > maxPrice) {
            display = false;
        }
        if (!categories.includes(category)){
            display = false;
        }
        if (!brands.includes(brand)){
            display = false;
        }
        if (availabilityFilter && !availability){
            display = false;
        }

        if (display) {
            product.style.display = 'flex';
        } else {
            product.style.display = 'none';
        }
    });
}


function redirectToLoginPage() {
    window.location.replace("/login");
}


document.addEventListener('DOMContentLoaded', function () {
    const carouselControls = document.querySelectorAll('.carousel-control-prev, .carousel-control-next');

    carouselControls.forEach(function (control) {
        control.addEventListener('click', function () {
            this.blur();
        });
    });
});


$(document).ready(function() {
    $('.buy-button').click(function() {
        var itemId = $(this).data('item-id');
        $('#itemIdInput').val(itemId); // Set the value to the hidden input field in the form

        // Submit the form via AJAX
        $('#itemForm').submit(function(event) {
            event.preventDefault(); // Prevent the default form submission
            var form = $(this);
            var formData = form.serialize(); // Serialize form data
            var url = form.attr('action'); // Get the form action URL

            $.ajax({
                type: 'POST',
                url: url,
                data: formData,
                success: function(response) {
                    console.log(response);
                },
                error: function(error) {
                    console.error('Error:', error.toString());
                }
            });

            $('#exampleModal').modal('hide');
        });
    });

    $('.add-to-cart').click(function() {
        var shoesId = $(this).data('shoes-id');

        $.ajax({
            url: `/user/cart-and-shoes/${shoesId}/`,
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': getCSRFToken()
            },
            success: function(data) {
                console.log('Item added to cart');
            },
            error: function(error) {
                console.log('Failed to add item to cart');
            }
        });
    });

    $('.delete-order-btn').click(function(){
        var shoesId = $(this).data('shoes-id');

        $.ajax({
            url: `/user/cart-and-shoes/${shoesId}/`,
            method: 'DELETE',
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
            },
            success: function(data) {
                console.log('Item deleted from cart');
                window.location.reload();
            },
            error: function(error) {
                console.log('Failed to remove item');
            }
        });
    });
});