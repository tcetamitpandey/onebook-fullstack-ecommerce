from django.db import models

gender_list=[
    ("male","Male"),
    ("female","Female"),
    ("others","others"),
]

class User_Model(models.Model):
    username = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=200)
    gender = models.CharField(max_length=20, choices=gender_list)
    age = models.PositiveIntegerField()

    def __str__(self):
        return self.username


class Product_Model(models.Model):
    title=models.CharField(max_length=500)
    price=models.FloatField()
    desc=models.TextField()

    category=models.CharField(max_length=200)
    image=models.TextField()
    rating=models.FloatField()
    rating_count=models.IntegerField()

    def __str__(self):
        return self.title
    

class Cart_Model(models.Model):
    user = models.ForeignKey(User_Model, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    products_in_cart = models.ManyToManyField(Product_Model)

    def __str__(self):
        return f"Cart : {self.id} - User: {self.user.username}"
    
    # def save_products(self, product_list):
    #     self.products_in_cart = json.dumps(product_list)

    # def get_products(self):
    #     try:
    #         return json.loads(self.products_in_cart)
    #     except json.JSONDecodeError:
    #         return []
