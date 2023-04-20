
// document.getElementById("filter").addEventListener("click", function () {
//     document.getElementById("filter-button").style.display = "none";
//     document.getElementById("filter-block").style.display = "block";
// });

$(document).ready(function(){
    $(".filter-ajax").hide();
    $(".filter-checkbox, #priceFilter").on('click', function(){
        var _filterObj = {};
        var _min = $("#maxPrice").attr('min');
        var _max = $("#maxPrice").val();
        _filterObj.minPrice = _min;
        _filterObj.maxPrice = _max;
        $(".filter-checkbox").each(function(index, ele){
            var _filterVal = $(this).val();
            var _filterKey = $(this).data('filter');
            _filterObj[_filterKey]=Array.from(document.querySelectorAll('input[data-filter='+_filterKey+']:checked')).map(function(el){
                return el.value;
            });
        });
        // console.log(_filterObj); 
        
        $.ajax({
            url: '/filter-data',
            data: _filterObj,
            dataType: 'json',
            beforeSend:function(){
                $(".filter-ajax").show();
            },
            success:function(res){
                console.log(res);
                $("#filterData").html(res.data)
                $(".filter-ajax").hide();
            }
        })
    });
});


// filter product according price
$("#maxPrice").on('blur', function(){
    var min = $(this).attr('min');
    var max = $(this).attr('max');
    var val = $(this).val();

    if (val>parseInt(max) || val<parseInt(min)) {
        alert('Values should be ' + min +'-'+ max);
        $(this).val(min);
        $(this).focus();
        $('#rangePrice').val(min);
        return false;
    }

});



// load more pagination
$(document).ready(function(){
    $("#loadMore").on('click', function(){
        var currentProd = $(".product-card").length;
        var limit = $(this).attr('data-limit');
        var total = $(this).attr('data-total');
        // console.log(currentProd, limit, total);

        $.ajax({
            url: '/load-more',
            data: {
                limit: limit,
                offset: currentProd
            },
            dataType: 'json',
            beforeSend:function(){
                $("#loadMore").attr("disabled", true);
                $(".load-more-icon").addClass('fa-spin');
            },
            success:function(res){
                $("#filterData").append(res.data)
                $("#loadMore").attr("disabled", false);
                $(".load-more-icon").removeClass('fa-spin');

                var totalShow = $(".product-card").length;

                if(totalShow==total){
                    $("#loadMore").remove()
                }
            }
        });

    });

    // show size according to color
    $(".chooseSize").hide();

    $(".chooseColor").on('click', function(){
        var color = $(this).attr('data-color');
        $(".chooseSize").hide();
        $(".color"+color).show();
        $(".chooseSize").removeClass('active');
        $(".color"+color).first().addClass('active');

        var price = $(".color"+color).first().attr('data-price');
        $(".choosePrice").text(price);
    });

    $(".chooseSize").on('click', function(){
        $(".chooseSize").removeClass('active');
        $(this).addClass('active');

        var price = $(this).attr('data-price');
        $(".choosePrice").text(price);
    });

    var color = $(".chooseColor").first().attr('data-color');
    $(".color"+color).show();
    $(".color"+color).first().addClass('active');

    var price = $(".color"+color).first().attr('data-price');
    $(".choosePrice").text(price);


    // add cart
    $(document).on('click', ".add-to-cart", function(){
        var id = $(this).attr('data-index')
        var qty = $(".product-qty-"+id).val();
        var product_image = $(".product-image-"+id).val();
        var product_id = $(".product-id-"+id).val();
        var product_title = $(".product-title-"+id).val();
        var price = $(".product-price-"+id).text();
       
        console.log(id, qty,product_id, product_title, price);

        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': product_id,
                'image': product_image,
                'product_title': product_title,
                'price': price,
                'qty': qty,
            },
            dataType: 'json',
            beforeSend: function(){
                $(this).attr('disabled', true);
            },
            success: function(res){
                // console.log(res);
                $(".cart-item").text(res.total);
                $(this).attr('disabled', false);
            },
        });
    });

    //delete item from cart

    $(document).on('click','.delete-item', function(){
        var id = $(this).attr('data-item');

        $.ajax({
            url: '/delete-cart-item',
            data: {
                'id': id,
            },
            dataType: 'json',
            beforeSend: function(){
                $(this).attr('disabled', true);
            },
            success: function(res){
                // console.log(res);
                $("#cart-list").html(res.data);
                $(".cart-item").text(res.total);
                $(this).attr('disabled', false);
            },
        });
    });


    //update item from cart

    $(document).on('click','.update-item', function(){
        var id = $(this).attr('data-item');
        var pQty = $(".qty-"+id).val();
        console.log(pQty);

        $.ajax({
            url: '/update-cart-item',
            data: {
                'id': id,
                'qty': pQty,
            },
            dataType: 'json',
            beforeSend: function(){
                $(this).attr('disabled', true);
            },
            success: function(res){
                $("#cart-list").html(res.data);
                $(this).attr('disabled', false);
            },
        });
    });


    $(document).on('click','.add-wishlist', function(){
        var p_id = $(this).attr('data-product');
        var vm = $(this);
        // var user_id = $(this).attr('data-user');
        // console.log(p_id);

        $.ajax({
            url: '/add-to-wishlist',
            data: {
                'product': p_id,
            },
            dataType: 'json',
            success: function(res){
                if (res.bool==true) {
                    vm.addClass('disabled').removeClass('add-wishlist');
                }
            },
        });
    });

    $(document).on('click','.delete-wish', function(){
        var id = $(this).attr('data-item');

        $.ajax({
            url: '/delete-wish-item',
            data: {
                'id': id,
            },
            dataType: 'json',
            beforeSend: function(){
                $(this).attr('disabled', true);
            },
            success: function(res){
                $("#wish-list").html(res.data);
                $(this).attr('disabled', false);
            },
        });
    });

});





