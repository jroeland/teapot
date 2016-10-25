'''
Created on Oct 19, 2016

@author: jaime
'''
from customers.models import Customer
from discounts.models import LoyaltyDiscount, FreeProduct, CategoryDiscount
from products.models import Product
from decimal import Decimal
from pprint import pprint


class CalculateDiscounts(object):
    def __init__(self, order):
        self.order = order
        self.product_discounts = []
    
    def set_discounts(self):
        #Step 1: Check that the dictionary has the required customer keys
        order = self.order
        self._check_customer_keys(order)
        
        #Step 2: It may be possible that the same product might appear several times under items,
        #and this could mean that for each of them, a promotion could be applied.
        #For example in data['items']:
        #{
        #  "product-id": "B102",
        #  "quantity": "5",
        #  "unit-price": "4.99",
        #  "total": "24.95"
        #},
        #        {
        #  "product-id": "B102",
        #  "quantity": "5",
        #  "unit-price": "4.99",
        #  "total": "24.95"
        #}
        #This would result in a free product or a discount in the cheapest product could be applied twice.
        #To avoid this, we will have to merge duplicates, and the following method does that
        #It will also find the category for each list and will return it for later use, so then we only need to iterate
        #once in the list
        merged_items, categories = self._merge_items_and_categorize(order)
        
        #For simplicity, we will simply replace the existing list of items with the merged list
        order['items'] = merged_items
        
        #Now, we will search for the free product discounts
        #This method will add a new key to each ordered item item['free_product'], with details of the promotion or
        #None if there is no free product
        order = self._set_free_product_discounts(order)
        
        #Now we get the category discounts
        order = self._set_category_discounts(order, categories)
        
        #Get the loyalty discount
        order['loyalty_discount_details'] = self._get_loyalty_discount(order)
        
        #Calculate the new total
        order['new_total'] = self._calculate_new_total(order, order['loyalty_discount_details'])
        return order
    def _check_customer_keys(self, data):
        required_customer_keys = ("customer-id", "items", "total")
        #Check if a dict has the required keys.
        #Map will create a list with 0 and 1:
        #If 0: key is there
        #If 1, key is not there
        #If there id any key missing, the max value of the list will be 1.
        if max(map(lambda key: 0 if key in data else 1, required_customer_keys)) == 1:
            raise Exception("Missing key in dict, make sure that all required values are included: %s" % required_customer_keys)
        
        #Is items a list?
        items = data['items']
        if type(items) != type([]) and type(items) != type(()):
            #Not a list, not a touple... we cant work with it!
            raise Exception("Items is not a dictionary or a list")
        
    def _get_loyalty_discount(self, data):
        try:
            customer = Customer.objects.get(uid = data['customer-id'])
        except Customer.DoesNotExist:
            return None
        
        #Now check which discount applies:
        try:
            loyalty_discount = LoyaltyDiscount.objects.filter(revenue_required__lte = customer.revenue).order_by("-revenue_required").values("revenue_required", "percent_discount")[0]
        except IndexError:
            #There is no loyalty discount
            loyalty_discount = None
        return loyalty_discount
    
    def _check_order_item_keys(self, order_item):
        #Check that this product has all the keys
        #Map will create a list with 0 and 1:
        #If 0: key is there
        #If 1, key is not there
        #If there id any key missing, the max value of the list will be 1.
        required_order_keys = ("product-id", "quantity", "unit-price", "total")
        if max(map(lambda key: 0 if key in order_item else 1, required_order_keys)) == 1:
            raise Exception("Missing key in dict, make sure that all required values are included for each order: %s" % unicode(required_order_keys))
    
    def _merge_items_and_categorize(self, data):
        
        #In order to find the category for each product, we will have to link the given product and the product in the db
        product_ids = [x['product-id'] for x in data['items']]
        products = Product.objects.filter(uid__in = product_ids).values("category_id", "uid",)
        #To avoid cheating the system, we will merge any duplicated in the items
        #And while on the way, change the values to a correct type
        known_item_ids = []
        merged_items = []
        dict_categories_order = []
        for order in data['items']:
            
            
            
            iid = order['product-id']
            #Now, we need to determine the category of this item to later check for category discounts
            #It may be that a sent product id is not in our DB, then the search will return None
            db_product = next((item for item in products if item["uid"] == order['product-id']), None)
            order['category_id'] = None
            if db_product:
                #We now know which category is this item 
                #any(d['category_id'] == db_instance['categoory_id'] for d in category_discounts):
                order['category_id'] = db_product['category_id']
            if iid not in known_item_ids:
                #This item id is new
                cleanned_dict = {}
                cleanned_dict["product-id"] = unicode(order['product-id'])
                cleanned_dict["quantity"] = int(order['quantity'])
                cleanned_dict["unit-price"] = Decimal(order['unit-price'])
                cleanned_dict["total"] = Decimal(order['total'])
                cleanned_dict["category"] = order['category_id']
                
                
                
                known_item_ids.append(iid)
                merged_items.append(cleanned_dict)
                
            else:
                #TThere is already an oder for this item, we will merge the values
                #Lets find the entry first and update the key
                dict_pointer = (item for item in merged_items if item["product-id"] == iid).next()
                dict_pointer["quantity"] += int(order['quantity'])
                dict_pointer["total"] += Decimal(order['total'])
            
            #Do we know about this product?
            if db_product:
                #Now, let create a list of dicts with the category and quantity bought
                category_match = next((cat for cat in dict_categories_order if cat["category_id"] == order['category_id']), None)
                product_price = Decimal(order['unit-price'])
                if not category_match:
                    #Its not in the list, so we add a new entry!
                    d = {}
                    d['category_id'] = db_product['category_id']
                    d['quantity'] = int(order['quantity'])
                    d['cheapest_product_price'] = product_price
                    d['total'] = Decimal(order['total'])
                    dict_categories_order.append(d)
                else:
                    category_match['quantity'] += int(order['quantity'])
                    category_match['total'] += Decimal(order['total'])
                    #Add the cheapest product bought for this category:
                    if product_price < d['cheapest_product_price']:
                        category_match['cheapest_product_price'] = product_price
        return merged_items, dict_categories_order
    
    def _set_free_product_discounts(self, data):
        #get the product id keys from the list of dicts
        product_ids = [str(x['product-id']) for x in data['items']]
        
        #Get the free products that have a match with the product_ids
        db_free_products =  FreeProduct.objects.filter(product_id__in = product_ids)
        #We are only interested in the fields product_id and quantity
        #Order by quantity so we can find later the best match for the free product
        free_products = db_free_products.order_by("-quantity_required").values("product_id", "quantity_required")
        
        #In case the same product is listed multiple times, we want to take it in account...
        for product_order in data['items']:
            product_order['free_products'] = {}
            #db_instance = (item for item in products if item["uid"] == product_order['product-id']).next()
            
            try:
                #All free products have a match to product, but not all products have a match on FreeProducts, so it will rise index error
                #free_products is sorted by highest to lowest, so we will always get the best offer
                applicable_free_product = [x for x in free_products if x['product_id'] == product_order['product-id']][0]
            except IndexError:
                #No applicable promotion here
                applicable_free_product = None
            else:
                #Calculate how many products will the customer receive
                applicable_free_product['to_receive'] = product_order['quantity'] / applicable_free_product['quantity_required']
                
            #Add a key to the product with the applicable promotion for free product
            product_order['free_products'] = applicable_free_product
        return data
    def _set_category_discounts(self, data, dict_categories_order):
        #Now we know about the categories and the total items bought for each, now just simply search for the matching category discount
        db_category_discounts = CategoryDiscount.objects.filter(category_id__in = [x['category_id'] for x in dict_categories_order])
        db_category_discounts = db_category_discounts.order_by("-quantity_required").values("category_id", "quantity_required", "percent_discount")
        for dco in dict_categories_order:
            dco['cheapest_product_discount_details'] = None
            dco['cheapest_product_discount'] = Decimal("0")
            dco['new_total'] = dco['total']
            #Check that the category and category's discount quiantity items is met
            category_match = next((cat for cat in db_category_discounts if cat["category_id"] == dco['category_id'] and cat['quantity_required'] <= int(dco['quantity'])), None)
            if category_match:
                dco['cheapest_product_discount_details'] = category_match
                dco['cheapest_product_discount'] = (category_match['percent_discount'] * dco['cheapest_product_price'])
                self.product_discounts.append(dco['cheapest_product_discount'])
                dco['new_total'] = dco['total'] - dco['cheapest_product_discount']
        
        data['category_discounts'] = dict_categories_order
        return data
    
    def _calculate_new_total(self, data, loyalty_discount):
        new_total = Decimal(data['total'])
        if self.product_discounts:
            product_discounts = sum(self.product_discounts)
            new_total = new_total - product_discounts
            
            #Apply the loyalty discount to the total
            if loyalty_discount:
                discount = Decimal(new_total * loyalty_discount['percent_discount'])
                data['loyalty_discount'] = str(discount)
                new_total = str(new_total - discount)
            
        return new_total
