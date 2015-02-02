from django.shortcuts import render
from django.conf import settings
from django.core.files import File
from oscar.core.loading import get_class, get_classes

ProductClass, Product, Category, ProductCategory, ProductImage, 
ProductAttribute, ProductAttributeValue, AttributeOption = get_classes(
    'catalogue.models', ('ProductClass', 'Product', 'Category',
                         'ProductCategory', 'ProductImage', 'ProductAttribute', 'ProductAttributeValue', 'AttributeOption'))
Partner, StockRecord = get_classes('partner.models', ('Partner', 'StockRecord'))


def create(request):
	context_dict = {}
	if request.method == 'POST':
		img_data = request.POST.get('imagesrc').decode("base64")
		img_file = open("./public/photo.jpg", "wb")
		img_file.write(img_data)
		img_file.close()

		#create a new parent product
		product_class = ProductClass.objects.get(pk=1)
		product = Product()
		product.product_class = product_class
		product.structure = Product.PARENT
		product.title = 'the first parent product'
		product.description = 'this is the first parent product'
		product.save()

		#create 3 child products
		child1 = Product()
		child1.parent = product
		child1.structure = Product.CHILD
		child1.save()

		child2 = Product()
		child2.parent = product
		child2.structure = Product.CHILD
		child2.save()

		child3 = Product()
		child3.parent = product
		child3.structure = Product.CHILD
		child3.save()

		#create 3 corresponding attribute
		option1 = AttributeOption.objects.get(pk=1)
		option2 = AttributeOption.objects.get(pk=2)
		option3 = AttributeOption.objects.get(pk=3)
		attr = ProductAttribute.objects.get(pk=1)

		attrVal1 = ProductAttributeValue()
		attrVal1.attribute = attr
		attrVal1.product = child1
		attrVal1.value_option = option1
		attrVal1.save()

		attrVal2 = ProductAttributeValue()
		attrVal2.attribute = attr
		attrVal2.product = child2
		attrVal2.value_option = option2
		attrVal2.save()

		attrVal3 = ProductAttributeValue()
		attrVal3.attribute = attr
		attrVal3.product = child3
		attrVal3.value_option = option3
		attrVal3.save()

		#create stockrecords

		partner = Partner.objects.get(pk=2)
		stock1 = StockRecord()
		stock1.product = child1
		stock1.partner = partner
		stock1.num_in_stock = 100
		stock1.save()

		stock2 = StockRecord()
		stock2.product = child2
		stock2.partner = partner
		stock2.num_in_stock = 100
		stock2.save()

		stock3 = StockRecord()
		stock3.product = child3
		stock3.partner = partner
		stock3.num_in_stock = 100
		stock3.save()

		new_file = File(open('./public/photo.jpg', 'rb'))
		im = ProductImage(product=product, display_order=0)
		im.original.save('newtee.jpg', new_file, save=False)
		im.save()
		#save the image
		return render(request, 'designer/success.html')

	else:
		print 'else'
	
	return render(request, 'designer/create.html', context_dict)