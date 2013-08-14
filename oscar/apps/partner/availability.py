from django.utils.translation import ugettext_lazy as _


class Base(object):
    """
    Simple based availability class which defaults to everything being
    unavailable.
    """

    # Standard properties
    code = ''
    message = ''
    lead_time = None
    dispatch_date = None

    @property
    def is_available_to_buy(self):
        """
        Test if this product is available to be bought.
        """
        # We test a purchase of a single item
        is_available, __ = self.is_purchase_permitted(1)

    def is_purchase_permitted(self, quantity):
        """
        Test whether a proposed purchase is allowed

        Should return a boolean and a reason
        """
        return False, u""


class NoStockRecord(Base):
    code = 'outofstock'
    message = _("Unavailable")


class WrappedStockRecord(Base):

    def __init__(self, product, stockrecord=None, user=None):
        self.product = product
        self.stockrecord = stockrecord
        self.user = user

    @property
    def is_available_to_buy(self):
        if self.stockrecord is None:
            return False
        if not self.product.get_product_class().track_stock:
            return True
        return self.stockrecord.is_available_to_buy

    def is_purchase_permitted(self, quantity):
        return self.stockrecord.is_purchase_permitted(
            self.user, quantity, self.product)

    @property
    def code(self):
        return self.stockrecord.availability_code

    @property
    def message(self):
        return self.stockrecord.availability

    @property
    def lead_time(self):
        return self.stockrecord.lead_time

    @property
    def dispatch_date(self):
        return self.stockrecord.dispatch_date