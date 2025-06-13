from app_store.models import ProductColor

color = ProductColor.objects.first()
print(color)
images = color.images.all()
print(images)
for img in images:
    print(img.image.url, img.image.path)
