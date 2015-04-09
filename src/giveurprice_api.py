"""Hello World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""


import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from google.appengine.ext import ndb        # for data storage

from endpoints_proto_datastore.ndb import EndpointsAliasProperty
from endpoints_proto_datastore.ndb import EndpointsModel
from endpoints_proto_datastore.ndb import EndpointsUserProperty

# TODO: Replace the following lines with client IDs obtained from the APIs
# Console or Cloud Console.
WEB_CLIENT_ID = '361494477850-7qu3tdv4f3sl8ph3culmd3r5gt91d81f.apps.googleusercontent.com'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID


package = 'Giveurprice'

"""
class Product(messages.Message):
    # Product that stores a message.
    message = messages.StringField(1)


class ProductCollection(messages.Message):
    # Collection of products.
    items = messages.MessageField(Product, 1, repeated=True)


STORED_products = ProductCollection(items=[
    Product(message='hello world!'),
    Product(message='goodbye world!'),
])
"""

class Order(messages.Enum):
    WHEN = 1
    
# Database Model & RPC Model for Chat Message
class Product(EndpointsModel):
    _message_fields_schema = ('id', 'email', 'user', 'user_url', 'user_price', 'found_url', 'found_price', 'created') # Set model schema

    user = ndb.UserProperty(required=True)
    email = ndb.StringProperty(required=True)
    user_url = ndb.StringProperty(required=True)
    user_price = ndb.FloatProperty(required=True)
    found_url = ndb.StringProperty(required=False, default=None)
    found_price = ndb.FloatProperty(required=False, default=None)
    created = ndb.DateTimeProperty(auto_now_add=True)   # when product id added

    # set order
    def OrderSet(self, value):
        if value == Order.WHEN:
            super(Product, self).OrderSet('created')
        else:
            raise TypeError('Unexpected value of Order: %s.' % (value,))

    # apply order
    @EndpointsAliasProperty(setter=OrderSet, property_type=Order, default=Order.WHEN)
    def order_by_date(self):
        return super(Product, self).order

"""
    allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID],
    audiences=[ANDROID_AUDIENCE])
"""
@endpoints.api(name='giveurprice', version='v0.1',
               description="Giveurprice API")
class GiveUrPriceApi(remote.Service):
    """Giveurprice API v1."""

        # Method to POST a Message
    @Product.method(user_required=True,        # for OAuth
                    http_method='POST',
                    request_fields=('user_url', 'user_price', 'email'),
                    name='Product.add',
                    path='Product')
    def add_Product(self, product):
        current_user = endpoints.get_current_user()       #from OAuth
        if current_user is None:
            raise endpoints.UnauthorizedException('Invalid token.')
        product.user = current_user
        product.put()
        return product
    
    @Product.method(user_required=True,
                    path='/Product/{id}',
                    http_method='PUT',
                    name='Product.update',
                    request_fields=('found_url', 'found_price'))
    def update_Product(self, product):
        product.put()
        return product
    
    @Product.method(user_required=True,
                    request_fields=('id',),
                    path='/Product/{id}',
                    http_method='GET',
                    name='Product.get',
                    )
    def get_Product(self, product):
        return product
    
    @Product.query_method(user_required=True,
                    query_fields=('found_url', 'found_price', 'created'),
                    path='/Products',
                    name='Products.query',
                    )
    def query_Products(self, query):
        return query

        
APPLICATION = endpoints.api_server([GiveUrPriceApi])
