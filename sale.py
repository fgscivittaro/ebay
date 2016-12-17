class Sale(object):
    """
    Represents the data of a single sales transaction.
    """

    TRANSACTION_ID = 0

    def __init__(self, datetime, price, quantity, color):
        Sale.TRANSACTION_ID += 1
        self._transaction_id = str(Sale.TRANSACTION_ID)
        self._datetime = datetime
        self._price = price
        self._quantity = quantity
        self._color = color


    @property
    def transaction_id(self):
        return self._transaction_id


    @property
    def datetime(self):
        return self._datetime


    @property
    def price(self):
        return self._price


    @property
    def quantity(self):
        return self._quantity


    @property
    def color(self):
        return self._color


    def __str__(self):
        return ("ID: {}, Date and Time: {}, Price: {}, Quantity: {}, Color: {}"
                .format(self.transaction_id,
                        self.datetime,
                        self.price,
                        self.quantity,
                        self.color))


    def __repr__(self):
        return str(self)
