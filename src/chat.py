from google.appengine.ext import endpoints  # for endpoints
from google.appengine.ext import ndb        # for data storage
from protorpc import remote                 # for API

from protorpc import messages
from endpoints_proto_datastore.ndb import EndpointsAliasProperty
from endpoints_proto_datastore.ndb import EndpointsModel
from endpoints_proto_datastore.ndb import EndpointsUserProperty

# Static Default Channel
IRC_CHANNEL = 'channel'

# order by class, to order by created date time
class Order(messages.Enum):
    WHEN = 1

# Database Model & RPC Model for Chat Message
class ChatMessage(EndpointsModel):
    _message_fields_schema = ('content', 'fromUser', 'toChannel', 'created') # Set model schema

    content = ndb.StringProperty(required=True)         # the message's content
    fromUser = ndb.UserProperty(required=True)          # get username from OAuth
    toChannel = ndb.StringProperty(required=True)       # send to channel
    created = ndb.DateTimeProperty(auto_now_add=True)   # when the messages is created

    # set order
    def OrderSet(self, value):
        if value == Order.WHEN:
            super(ChatMessage, self).OrderSet('created')
        else:
            raise TypeError('Unexpected value of Order: %s.' % (value,))

    # apply order
    @EndpointsAliasProperty(setter=OrderSet, property_type=Order, default=Order.WHEN)
    def order(self):
        return super(ChatMessage, self).order

# The API
@endpoints.api(name='sugarchatersion', version='v1',
               description='Test google endpoints chat')            
class ChatAPI(remote.Service):

    # Method to POST a Message
    @ChatMessage.method(user_required=True,        # for OAuth
                 request_fields=('content',),
                 name='chatMessage.send',
                 path='chatMessage')
    def send_chatMessage(self, chatMessage):
        chatMessage.fromUser = endpoints.get_current_user()       #from OAuth
        chatMessage.toChannel = IRC_CHANNEL        
        chatMessage.put()
        return chatMessage

    # Method to Get a Conversation
    @ChatMessage.query_method(user_required=True,
                       query_fields=('limit', 'order', 'pageToken'),
                       name='chatMessage.conversation',
                       path='conversation')
    def conversation_messages(self, query):
        return query.filter(ChatMessage.toChannel == IRC_CHANNEL)

application = endpoints.api_server([ChatAPI])