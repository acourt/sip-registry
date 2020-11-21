import unittest
import time
import socket

validAor = '0148c1f489badb837d000100620002'
validRecordString = '{"addressOfRecord":"0148c1f489badb837d000100620002","tenantId":"0127d974-f9f3-0704-2dee-000100420001","uri":"sip:0148c1f489badb837d000100620002@9.98.167.222;jbcuser=cpe70","contact":"<sip:0148c1f489badb837d000100620002@120.133.72.122;jbcuser=cpe70>;methods=\\"INVITE, ACK, BYE, CANCEL, OPTIONS, INFO, MESSAGE, SUBSCRIBE, NOTIFY, PRACK, UPDATE, REFER\\"","path":["<sip:Mi0xOTkuMTkyLjE2NS4xOTQtMTk2MjI@61.0.24.25:5060;lr>"],"source":"191.12.63.101:19622","target":"69.92.33.38:5061","userAgent":"polycom.vvx.500","rawUserAgent":"PolycomVVX-VVX_500-UA/59.124.31.194","created":"2016-12-13T04:48:30.889Z","lineId":"0148c1f4-8913-4d7f-d37d-000100620002"}\n'
validAor2 = 'h1uDjvwQcLWDOEfqcwwT9rpMGLPsVD'
validRecordString2 = '{"addressOfRecord":"h1uDjvwQcLWDOEfqcwwT9rpMGLPsVD","tenantId":"0127d974-f9f3-0704-2dee-000100420001","uri":"sip:h1uDjvwQcLWDOEfqcwwT9rpMGLPsVD@221.33.20.80","contact":"<sip:h1uDjvwQcLWDOEfqcwwT9rpMGLPsVD@105.183.18.90>;methods=\\"INVITE, ACK, BYE, CANCEL, OPTIONS, INFO, MESSAGE, SUBSCRIBE, NOTIFY, PRACK, UPDATE, REFER\\"","path":["<sip:Mi00NS41Ni4yMS4zLTUwNjA@219.85.9.241:5060;lr>"],"source":"129.124.91.78:5060","target":"18.70.131.10:5061","userAgent":"polycom.vvx.500","rawUserAgent":"PolycomVVX-VVX_500-UA/242.196.97.185","created":"2017-01-06T05:19:37.137Z","lineId":"6d69c4ad-13b6-4fd1-a412-4d8112410ecc"}\n'
invalidAor = '0148c1f489badb837d000100620001'


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

        # Get the host's response, no more than, say, 1,024 bytes
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

        # Get the host's response, no more than, say, 1,024 bytes
        response_data = sock.recv(1024)
        
        self.assertEqual(response_data.decode('utf-8'), '\n')


if __name__ == '__main__':
    unittest.main()