SITES = {
    "caramelkids.ir": {
        "item": "div.wd-product",
        "name": "h3.wd-entities-title a",
        "price": ["span.price ins bdi", "span.price bdi"],   # به ترتیب اولویت
        "link_attr": "href",
        "page_url": "{base}page/{page}/",
    },
    # نمونه: سایت دیگر (selectorها را با Inspect پر کن)
    # "example.ir": {
    #     "item": "li.product",
    #     "name": "h2.woocommerce-loop-product__title",
    #     "price": ["span.price ins bdi", "span.price bdi"],
    #     "link_attr": "href",
    #     "page_url": "{base}page/{page}/",
    # },
}