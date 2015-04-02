from django.shortcuts import render
from django.conf import settings
from django.core.files import File
from oscar.core.loading import get_class, get_classes
from PIL import Image
from apps.designer.models import TshirtSKU

ProductClass, Product, Category, ProductCategory = get_classes(
    'catalogue.models', ('ProductClass', 'Product', 'Category',
                         'ProductCategory'))
ProductImage, ProductAttribute, ProductAttributeValue, AttributeOption = get_classes(
	'catalogue.models', ('ProductImage', 'ProductAttribute', 'ProductAttributeValue', 'AttributeOption'))

Partner, StockRecord = get_classes('partner.models', ('Partner', 'StockRecord'))

def home(request):
	if request.method == 'GET':
		return render(request, 'home.html')

		
def create(request):
	context_dict = {}
	if request.method == 'POST':
	
		img_src  = request.POST.get('imagesrc')
		img_idx  = img_src.find('base64')
		img_data = img_src[img_idx+7:].decode("base64")
		img_file = open("./public/photo.png", "wb")
		img_file.write(img_data)
		img_file.close()

		height = int(float(request.POST.get('valueh')))
		width  = int(float(request.POST.get('valuew')))
		x = int(float(request.POST.get('valuex')))
		y = int(float(request.POST.get('valuey')))
		baseim = Image.open('./public/static/wuyi/plugins/images/black_front.png')
		floatimg = Image.open('./public/photo.png')
		resized = floatimg.resize((width, height), Image.BILINEAR)
		baseim.paste(resized, (x, y), resized)
		baseim.save('./public/pasted.png')

		#create a new parent product
		product_class = ProductClass.objects.get(pk=1)
		product = Product()
		product.product_class = product_class
		product.structure = Product.PARENT
		product.title = 'the first parent product'
		product.description = 'this is the first parent product'
		product.save()

		# #create 3 child products
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

		# #create 3 corresponding attribute
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

		# #create stockrecords
		# Get the latest sku
		latest_sku = TshirtSKU.objects.order_by('-pk')[0]
		new_sku1 = latest_sku.sku + 1
		new_sku2 = latest_sku.sku + 2
		new_sku3 = latest_sku.sku + 3

		tshirtsku = TshirtSKU()
		tshirtsku.sku = new_sku1
		tshirtsku.save()

		tshirtsku2 = TshirtSKU()
		tshirtsku2.sku = new_sku2
		tshirtsku2.save()

		tshirtsku3 = TshirtSKU()
		tshirtsku3.sku = new_sku3
		tshirtsku3.save()

		partner = Partner.objects.get(pk=2)
		stock1 = StockRecord()
		stock1.product = child1
		stock1.partner = partner
		stock1.num_in_stock = 100
		stock1.partner_sku = new_sku1
		stock1.save()

		stock2 = StockRecord()
		stock2.product = child2
		stock2.partner = partner
		stock2.num_in_stock = 100
		stock2.partner_sku = new_sku2

		stock3 = StockRecord()
		stock3.product = child3
		stock3.partner = partner
		stock3.num_in_stock = 100
		stock3.partner_sku = new_sku3
		stock3.save()

		new_file = File(open('./public/pasted.png', 'rb'))
		new_file_back = File(open('./public/static/wuyi/plugins/images/black_back.png'))
		im = ProductImage(product=product, display_order=0)
		im2 = ProductImage(product=product, display_order=1)
		im.original.save('newtee.png', new_file, save=False)
		im2.original.save('newtee_back.png', new_file_back, save=False)

		im.save()
		im2.save()
		#save the image
		return render(request, 'designer/success.html')

	else:
		print 'else'
	
	return render(request, 'designer/create.html', context_dict)