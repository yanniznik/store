var Store = {};

Store.start = function(){
	$(document).ready(function() {
		Store.loadCategories();
		Store.loadStoreName();
	});
};

Store.handlePagination = function(btn, currentPage, currentCategory) {
	(btn.is("#next")) ? currentPage++ : currentPage--;
	Store.loadProducts(currentCategory, currentPage);
}

Store.loadStoreName = function(){
	$.get("/config",function(result){
		if (result["STATUS"] == "ERROR"){
			alert(result["MSG"]);
		}else{
			var storeName = result["CONFIG"]["name"];
			$("title").add('#storeName').text(storeName);
		}
	},"json");
};


Store.loadCategories = function(){
	$.get("/categories",function(result){
		if (result["STATUS"] == "ERROR"){
			alert(result["MSG"]);
		}else{
			var categories = result["CATEGORIES"];
			var categoriesHolder = $("#categories");
			categoriesHolder.empty();
			for (i in categories){
				var categoryBtn = $("<nav />").addClass("nav-btn clickable").text(categories[i].name);
				categoryBtn.attr("id","cat-" + categories[i].id);
				categoryBtn.click(function(e){
					Store.loadProducts($(this).attr("id"), 0);
				});
				categoriesHolder.append(categoryBtn)
			}
			$("#page").addClass("ready");
			var firstCategory = $("#categories .nav-btn").attr("id");
			Store.loadProducts(firstCategory, 0);
		}
	},"json");
};

Store.loadProducts = function(category, page){
	var categoryID = category.replace("cat-","");
	$.get("/category/" + categoryID + "/products/" + page,function(result){
		$("#content").empty();
		var nextPage = $("<span />").attr("id", "next").text("Next");
		var prevPage = $("<span />").attr("id", "prev").text("Prev");
		nextPage.add(prevPage).addClass("clickable").click(function() {
			Store.handlePagination($(this), page, category);
		});
		var paginationHandler = $("<div />").addClass('pagination-holder');
		if (page > 0) {
			paginationHandler.append(prevPage);
		}
		if (result["PRODUCTS"]["has_more"]) {
			paginationHandler.append(nextPage);
		}
		for( i in result["PRODUCTS"]["products"]){
			var productObj = result["PRODUCTS"]["products"][i];
			var product = $("#templates .product").clone();
			product.find(".img").css("background-image","url('"+ productObj.img_url +"')");
			product.find(".title").text(productObj.title);
			product.find(".desc").text(productObj.description);
			product.find(".price").text("$" + productObj.price);
			product.find("form input[name='item_name']").val(productObj.title);
			product.find("form input[name='item_number']").val(productObj.id);
			product.find("form input[name='amount']").val(productObj.price);
			if (productObj.favorite){
				product.addClass("favorite");
			}
			$("#content").append(product).append(paginationHandler);
		}
	},"json");
};
Store.start();

