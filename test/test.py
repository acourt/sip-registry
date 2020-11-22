import unittest
import time
import socket
from subprocess import Popen

invalidAor  =   '01554ff4501912c5a500010062000A'
validAor    =   '01554ff4501912c5a5000100620009'
validRecordString = '{"addressOfRecord":"01554ff4501912c5a5000100620009","tenantId":"0127d974-f9f3-0704-2dee-000100420001","uri":"sip:01554ff4501912c5a5000100620009@40.255.16.32:1055","contact":"<sip:01554ff4501912c5a5000100620009@42.50.137.11:1055>;methods=\\"INVITE, ACK, BYE, CANCEL, OPTIONS, INFO, MESSAGE, SUBSCRIBE, NOTIFY, PRACK, UPDATE, REFER\\"","path":["<sip:Mi0xOTAuMTQ4LjI1NC4yNy0xMDUz@19.235.214.18:5060;lr>"],"source":"158.131.24.166:1053","target":"189.210.60.153:5061","userAgent":"polycom.vvx.400","rawUserAgent":"PolycomVVX-VVX_400-UA/115.43.182.253","created":"2017-01-06T03:06:20.299Z","lineId":"01554ff3-dad0-ec00-45a5-000100620009"}\n'



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
        time.sleep(11)
        print("timeout")
    
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
    p = Popen(["python", "../src/SipRegistryServer.py", "--file", "./testdata/testregs"])
    unittest.main()
    p.terminate()