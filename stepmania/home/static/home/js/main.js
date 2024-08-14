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


function decreaseQuantity(button) {
    var input = button.parentNode.querySelector('input');
    input.stepDown();
    $(input).trigger('change');
}


function increaseQuantity (button) {
    var input = button.parentNode.querySelector('input');
    input.stepUp();
    $(input).trigger('change');
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
    let toastTimeout;
    let buttonDisableTimeout;


    // Order
    $('.buy-button').click(function() {
        var itemId = $(this).data('item-id');
        $('#itemIdInput').val(itemId); // Set the value to the hidden input field in the form

        // Submit the form via AJAX
        $('#orderForm').submit(function(event) {
            event.preventDefault(); // Prevent the default form submission
            var form = $(this);
            var formData = form.serialize(); // Serialize form data
            var url = "/catalogue/order/"; // Get the form action URL

            $.ajax({
                type: 'POST',
                url: url,
                data: formData,
                success: function(response) {
                    showToastMessage(response);
                },
                error: function(error) {
                    console.error('Error:', error.toString());
                }
            });

            $('#exampleModal').modal('hide');
        });
    });


    $('.cancel-order-btn').click(function() {
        var orderId = $(this).data('order-id');

        // Submit the form via AJAX
        $('.confirm-button').click(function(event) {
            event.preventDefault();

            $.ajax({
                type: 'DELETE',
                url: '/catalogue/order/',
                headers: {
                    'X-CSRFToken': getCSRFToken() // Include the CSRF token
                },
                data: JSON.stringify({ 'order_id': orderId }),
                success: function(response) {
                    console.log(response);
                    location.reload();
                },
                error: function(error) {
                    console.error('Error:', error.toString());
                }
            });
        });
    });

    // Cart
    $('.add-to-cart').click(function() {
        var shoesId = $(this).data('shoes-id');
        var button = $(this);

        clearTimeout(buttonDisableTimeout);
        buttonDisableTimeout = setTimeout(function() {
            button.data('disabled', false);  // Re-enable the button after 2 seconds
            button.removeClass('disabled-button');  // Remove the disabled styling
        }, 2000);

        if (button.data('disabled')) {
            showToastMessage('Wait a second before adding one more item', 'warning');
            return;
        }

        // Disable the button immediately
        button.data('disabled', true);

        $.ajax({
            url: `/user/cart-and-shoes/${shoesId}/`,
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': getCSRFToken()
            },
            success: function(response) {
                showToastMessage(response);
            },
            error: function(error) {
                console.log('Failed to add item to cart');
            }
        });
    });


    $('.delete-from-cart').click(function(){
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


    $('.item-quantity').on('change', function() {
        var shoesId = $(this).data('shoes-id');
        var newQuantity = parseInt($(this).val(), 10);

        $.ajax({
            url: `/user/cart-and-shoes/${shoesId}/`,
            method: 'PUT',
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
            },
            data: JSON.stringify({
                quantity: newQuantity,
            }),
            contentType: "application/json",
            success: function(data) {
                console.log('Item updated in cart');
                window.location.reload();
            },
            error: function(error) {
                console.log('Failed to update item');
            }
        });
    });


    $('.cart #orderForm').submit(function(event) {
        event.preventDefault();
        var form = $(this);
        var formData = form.serialize();
        var url = "/user/cart/";

        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            success: function(response) {
                console.log(response);
                window.location.replace("/user/profile/");
            },
            error: function(error) {
                console.error('Error:', error.toString());
            }
        });

        $('#exampleModal').modal('hide');
    });


    $('.feedback-form').submit(function (event) {
        event.preventDefault();

        var form = $(this);
        var formData = form.serialize();
        var url = "/user/feedback/";

        form[0].reset();
        window.scrollTo(0, 0);

        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            success: function(response) {
                showToastMessage(response);
            },
            error: function(error) {
                showToastMessage(error.responseText, 'warning');
            }
        });
    });


    function showToastMessage(message, type = 'success') {
        const toast = $('#toast-message');

        // Clear previous timeout if it exists
        clearTimeout(toastTimeout);

        // Remove previous classes and add new class based on type
        toast.removeClass('toast-success toast-warning');
        if (type === 'success') {
            toast.addClass('toast-success');
        } else if (type === 'warning') {
            toast.addClass('toast-warning');
        }

        toast.text(message);
        toast.show().css('opacity', '1');  // Show the toast with opacity

        // Set timeout for hiding the toast
        toastTimeout = setTimeout(function() {
            toast.css('opacity', '0');  // Start fade-out transition
            setTimeout(function() {
                toast.hide();  // Hide the toast after fade-out transition
            }, 500);  // Match the fade-out duration
        }, 2000);  // Duration the toast stays visible
    }
});