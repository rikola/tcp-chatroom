import unittest
from asyncio import StreamWriter, StreamReader

from asynctest import TestCase
from asynctest.mock import Mock, create_autospec, patch, MagicMock

from chat.server import handle


class TestServer(TestCase):
    async def test_handle(self):
        reader = StreamReader()
        reader.feed_data(b"test message 1\r\nexit")
        reader.feed_eof()
        mock_writer: MagicMock = create_autospec(StreamWriter)
        mock_writer.get_extra_info = MagicMock(return_value="Test User")

        forward_mock: Mock
        with patch("chat.server.forward") as forward_mock:
            await handle(reader, mock_writer)

        self.assertTrue(reader.at_eof())
        forward_mock.assert_called()
        mock_writer.get_extra_info.assert_called()


if __name__ == '__main__':
    unittest.main()
