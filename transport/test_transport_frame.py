import unittest

from transport_frame import TransportFrame, unmarshall, TRANSPORT_FRAME_SIZE

TEST_MSG = "Hello, World!"


class TransportFrameTestCase(unittest.TestCase):

    def test_marshall(self):
        frame = TransportFrame(TEST_MSG)
        frame_bytes = frame.build()
        self.assertEqual(TRANSPORT_FRAME_SIZE, len(frame_bytes))

    # noinspection PyTypeChecker
    def test_unmarshall(self):
        self.addTypeEqualityFunc(TransportFrame, lambda first, second, msg: first.message == second.message)
        frame = TransportFrame(TEST_MSG)
        wire_data = frame.build()
        result = unmarshall(wire_data)
        self.assertEqual(frame, result)


if __name__ == '__main__':
    unittest.main()
