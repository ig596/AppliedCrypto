import binascii
import unittest
import fencrypt

class MyTestCase(unittest.TestCase):
    def test_master_key_creation(self):
        key=fencrypt.generate_master_key(b'e09f8ed71b715ec29d7c6c4db2efbf6a',b'e95af5ec95b703b9fdb119a565df5012')
        # print(binascii.hexlify(key))
        self.assertEqual(b'25340ee53eb54510ac8770f830c7750fa6b850176e35934fce0db56681e0ec4d',binascii.hexlify(key))
    def test_all_key_generation(self):
        result=fencrypt.generate_keys('bb80687f3bb2be6c40322944ee145c947adcf8c8e989da60ebe8a1be5e9aa46b')
        # print(result)
        expected={
  "validator": "7cfbdb5d0bb4de33a0c31a57a8f50a4b",
  "feistel": [
    "fa229054738db8de31881203637a5eeb",
    "2d779e5c90ff180421a072153bd2e830",
    "3dc67b3a09ea7cde33f179fae9806d4d",
    "bd2a0991be66b66622bf5c4ddf39bef7"
  ],
  "mac": "59339365ac8b691c72eeb2c6f99fd6bb",
  "search_terms": "d587bda883addbed8df571f35eafa7fd"
}
        self.assertEqual(expected['validator'],result['validator'],msg='test for validators')
        self.assertSequenceEqual (expected['feistel'],result['feistel'], msg='test for feistel')
        self.assertEqual(expected['mac'],result['mac'], msg='check mac key')
        self.assertEqual(expected['search_terms'], result['search_terms'], msg='check search key')

    def test_aes_ctr_round(self):
        result=fencrypt.aes_ctr_round(key=b"f0976dc478d49e3e501a34c1bc0470d2",data=b"96812ae4e46f6394056a343cd24eabe9da96f03cf6f5ea697b7ca81db801605d306cebf586b15a2738dc45f0cae54f48c2de358a4afcfb190c8742d02142a69b")
        self.assertEqual("96812ae4e46f6394056a343cd24eabe9c6dafa64f3c9d18037916f7ccce8442cc15019214cf268a71a749476175a0bca4f2d5bd0b05c38261cbee6a9fb217a6d",result)
if __name__ == '__main__':
    unittest.main()
