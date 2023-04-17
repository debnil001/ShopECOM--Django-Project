from django import template
register=template.Library()

@register.filter(name="is_in_cart")
def is_in_cart(product,cart):
    keys=cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False


@register.filter(name="cart_quantity")
def cart_quantity(product,cart):
    keys=cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return 0


@register.filter(name="price_total")
def price_total(product,cart):
    return (product.price*cart_quantity(product,cart))


@register.filter(name="price_sum")
def price_sum(products,cart):
    sum=0
    for prodcut in products:
        sum=sum+price_total(prodcut,cart)
    return sum

@register.filter(name="count")
def count(number):
    return 1+int(number)

@register.filter(name="multiply")
def multiply(number,number1):
    return number*number1