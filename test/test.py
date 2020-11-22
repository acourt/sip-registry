import unittest
import json
import time
import socket
from subprocess import Popen

testRegsFileName = "./testdata/testregs"
invalidAor  =   '01554ff4501912c5a500010062000A'

class TestSipRegistryServer(unittest.TestCase):

    def setUp(self):
        global sock
        # Create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the remote host and port
        sock.connect(('127.0.0.1', 8888))
    
    def tearDown(self):
        global sock
        # Terminate
        sock.close(  )


    def test_correct_aor(self):
        """
        Test that it returns the correct Aor string present in the regs file
        """
        # Send a request to the host
        sock.send(validAor.encode('utf-8'))

        response_data = sock.recv(1024)
        
        self.assertEqual(response_data.decode('utf-8'), validRecordString)

    def test_timeout(self):
        """
        Test that the server closes the connection when waiting for too long
        """
        timeoutOccured = False
        time.sleep(11)
        try:
            sock.send(validAor.encode('utf-8'))
            sock.recv(1024)
        except ConnectionAbortedError:
            timeoutOccured = True
        self.assertTrue(timeoutOccured)

    def test_incorrect_aor(self):
        """
        Test that sending an invalid AoR returns a empty line
        """
        # Send a request to the host
        sock.send(invalidAor.encode('utf-8'))

        response_data = sock.recv(1024)
        
        self.assertEqual(response_data.decode('utf-8'), '\n')


if __name__ == '__main__':
    """
    Start the server asynchronously with test values and then execute unit tests.
    Terminate server subprocess when finished
    """
    global validRecordString
    global validAor

    # Read the test regs file
    with open(testRegsFileName, 'r') as f:
        line = f.readline()
        sipRecord = json.loads(line)
    validRecordString = line
    validAor = sipRecord['addressOfRecord']

    # Start a server subprocess
    p = Popen(["python", "../src/SipRegistryServer.py", "--file", testRegsFileName])
    
    # Execute the tests
    unittest.main(exit=False)
    
    # Kill the server subprocess
    p.terminate()
    poll = p.wait(10)
    