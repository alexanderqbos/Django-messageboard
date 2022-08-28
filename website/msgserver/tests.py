from django.test import TestCase
from .models import Message
import json

test_key = '12345678'
test_message = 'Test message'

# Create your tests here.
class MessageTestCase(TestCase):
    #
    # PURPOSE:
    # Test the create url for the database
    #
    # NOTES:
    # we test that the created value is within the Message object
    #
    def test_message_create(self):
        response = self.client.post("/msgserver/create/",
        {'key': test_key, 'message': test_message})
        m = Message.objects.get(key=test_key)
        self.assertEqual(m.key, test_key)
        self.assertEqual(m.message, test_message)
    
    #
    # PURPOSE:
    # Test the database for error messaging in the form by posting the same data twice to
    # the create endpoint.
    #
    # NOTES:
    # Unique constraint is only on the key so we can test with the same key twice since
    # it will always throw and error first.
    #
    def test_message_duplicate(self):
        test_message = 'Test message'
        # First run to add test case to model
        response = self.client.post("/msgserver/create/",
        {'key': test_key, 'message': test_message})
        # Second run to test conflict
        response = self.client.post("/msgserver/create/",
        {'key': test_key, 'message': test_message}, follow=True)
        self.assertEqual(200, response.status_code)

    #
    # PURPOSE:
    # Test for the field constraints of the key and message column.
    #
    # NOTES:
    # Testing a key less then eight characters, and over eight.
    # Testing a message of length zero and and length 165
    #
    def test_message_field_contraints(self):
        short_test_key = '1234567' # too short
        long_test_key = '123456789' # too long
        short_test_message = ''
        long_test_message = '1324657891234567981324567891346579813245679813246579813246578913246578913246578913246579813246578941233154864651631657984651631654646546513132124567894567894561221333'
        
        response = self.client.post("/msgserver/create/",
        {'key': short_test_key, 'message': test_message})

        self.assertIn(b'Ensure this value has at least 8 characters', response._container[0]) # Ensure this value has at least 8 characters

        response = self.client.post("/msgserver/create/",
        {'key': long_test_key, 'message': test_message})

        self.assertIn(b'Ensure this value has at most 8 characters', response._container[0])

        response = self.client.post("/msgserver/create/",
        {'key': test_key, 'message': long_test_message})

        
        self.assertIn(b'Ensure this value has at most 160 characters', response._container[0])

        response = self.client.post("/msgserver/create/",
        {'key': test_key, 'message': short_test_message})

        
        self.assertIn(b'This field is required.', response._container[0])
    
    #
    # PURPOSE:
    # Testing the update message for the given key.
    #
    # NOTES:
    # Testing to update with a new message. Of an existing key.
    # Testing to update with a bad key.
    #
    def test_message_update(self):
        test_message = 'Test message'
        updated_test_message = 'Updated test message'
        
        self.client.post("/msgserver/create/",
        {'key': test_key, 'message': test_message})

        response = self.client.post("/msgserver/update/" + test_key + "/",
        {'message': updated_test_message})
        
        m = Message.objects.get(key=test_key)
        
        self.assertEqual(updated_test_message, m.message)
        
        response = self.client.post("/msgserver/update/" + test_key + '1' + "/",
        {'message': updated_test_message})

        self.assertIn(b'Invalid key used', response._container[0])

    #
    # PURPOSE:
    # Create 3 unique messages with keys and messages lists.
    # Get the /msgserver/ json response and parse it for the values
    # used to create the messages to confirm that it can be correctly
    # destructured and is readable.
    #
    def test_message_JSON_format(self):
        max_values = 3

        keys = [
            '1234ABCD',
            '1234A123',
            '123456CD'
        ]

        messages = [
            'Testing',
            'Tests',
            'Test'
        ]

        create_response = self.client.post("/msgserver/create/",
        {'key': keys[0], 'message': messages[0]})
        self.client.post("/msgserver/create/",
        {'key': keys[1], 'message': messages[1]})
        self.client.post("/msgserver/create/",
        {'key': keys[2], 'message': messages[2]})
        response = self.client.get("/msgserver/", {})
        data = response._container[0]
        data = data.decode('utf-8')
        data = json.loads(data)
        for i in range(max_values):
            self.assertEqual(data[i]['key'], keys[i])
            self.assertEqual(data[i]['message'], messages[i])
