"""
Tests for GT_U7GPS class.
"""
import pytest
from gps_data import GPSData
from gps import GT_U7GPS


class TestGT_U7GPSInitialization:
    """Tests for GT_U7GPS initialization."""

    def test_init_with_mock_serial(self, mock_serial):
        """Test GPS initializes with injected serial port."""
        gps = GT_U7GPS(serial_port=mock_serial)

        assert gps.ser is mock_serial
        assert isinstance(gps.data, GPSData)

    def test_init_creates_default_data(self, mock_serial):
        """Test GPS creates default GPSData on init."""
        gps = GT_U7GPS(serial_port=mock_serial)

        assert gps.data.latitude == 0.0
        assert gps.data.longitude == 0.0
        assert gps.data.num_sats == 0


class TestGT_U7GPSProperties:
    """Tests for GT_U7GPS backward compatibility properties."""

    @pytest.fixture
    def gps(self, mock_serial):
        """Create GPS instance with mock serial."""
        return GT_U7GPS(serial_port=mock_serial)

    def test_latitude_property(self, gps):
        """Test latitude property returns data.latitude."""
        gps._data.latitude = 49.2827
        assert gps.latitude == 49.2827

    def test_longitude_property(self, gps):
        """Test longitude property returns data.longitude."""
        gps._data.longitude = -123.1207
        assert gps.longitude == -123.1207

    def test_lat_dir_property(self, gps):
        """Test lat_dir property returns data.lat_dir."""
        gps._data.lat_dir = 'N'
        assert gps.lat_dir == 'N'

    def test_lon_dir_property(self, gps):
        """Test lon_dir property returns data.lon_dir."""
        gps._data.lon_dir = 'W'
        assert gps.lon_dir == 'W'

    def test_height_property(self, gps):
        """Test height property returns data.height."""
        gps._data.height = 70.5
        assert gps.height == 70.5

    def test_num_sats_property(self, gps):
        """Test num_sats property returns data.num_sats."""
        gps._data.num_sats = 8
        assert gps.num_sats == 8

    def test_gps_quality_property(self, gps):
        """Test gps_quality property returns data.gps_quality."""
        gps._data.gps_quality = 1
        assert gps.gps_quality == 1


class TestGT_U7GPSClose:
    """Tests for GT_U7GPS close method."""

    def test_close_closes_serial(self, mock_serial):
        """Test close() closes the serial port."""
        gps = GT_U7GPS(serial_port=mock_serial)
        assert mock_serial.is_open() is True

        gps.close()

        assert mock_serial.is_open() is False

    def test_close_when_already_closed(self, mock_serial):
        """Test close() handles already closed port."""
        gps = GT_U7GPS(serial_port=mock_serial)
        mock_serial.close()

        # Should not raise
        gps.close()


class TestGT_U7GPSReadData:
    """Tests for GT_U7GPS read_gps_data method."""

    def test_read_gps_data_parses_gga(self, mock_serial):
        """Test read_gps_data parses GGA sentence."""
        mock_serial.add_response("$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,47.0,M,,*4F\r\n")

        gps = GT_U7GPS(serial_port=mock_serial)
        gps.read_gps_data()

        assert gps.latitude == pytest.approx(48.1173, rel=0.001)
        assert gps.longitude == pytest.approx(11.5167, rel=0.001)
        assert gps.num_sats == 8

    def test_read_gps_data_handles_empty(self, mock_serial):
        """Test read_gps_data handles no data available."""
        gps = GT_U7GPS(serial_port=mock_serial)

        # Should not raise
        gps.read_gps_data()

        assert gps.latitude == 0.0

    def test_read_gps_data_multiple_sentences(self, mock_serial):
        """Test read_gps_data processes multiple sentences."""
        mock_serial.add_response("$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,47.0,M,,*4F\r\n")
        mock_serial.add_response("$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A\r\n")

        gps = GT_U7GPS(serial_port=mock_serial)
        gps.read_gps_data()

        # Both sentences should have been processed
        assert gps.latitude == pytest.approx(48.1173, rel=0.001)

    def test_read_gps_data_ignores_non_gps(self, mock_serial):
        """Test read_gps_data ignores non-GPS sentences."""
        mock_serial.add_response("$GLGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M*47\r\n")

        gps = GT_U7GPS(serial_port=mock_serial)
        gps.read_gps_data()

        # Should not have updated
        assert gps.latitude == 0.0

    def test_read_gps_data_handles_decode_error(self, mock_serial):
        """Test read_gps_data handles decode errors gracefully."""
        # Add invalid UTF-8 bytes
        mock_serial._responses.append(b'\xff\xfe invalid utf8')

        gps = GT_U7GPS(serial_port=mock_serial)

        # Should not raise, just log error
        gps.read_gps_data()


class TestGT_U7GPSDataProperty:
    """Tests for GT_U7GPS data property."""

    def test_data_property_returns_gps_data(self, mock_serial):
        """Test data property returns GPSData instance."""
        gps = GT_U7GPS(serial_port=mock_serial)

        assert isinstance(gps.data, GPSData)

    def test_data_property_same_instance(self, mock_serial):
        """Test data property returns same instance."""
        gps = GT_U7GPS(serial_port=mock_serial)

        data1 = gps.data
        data2 = gps.data

        assert data1 is data2

    def test_data_updated_by_read(self, mock_serial):
        """Test data is updated by read_gps_data."""
        mock_serial.add_response("$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,47.0,M,,*4F\r\n")

        gps = GT_U7GPS(serial_port=mock_serial)
        data = gps.data

        assert data.latitude == 0.0

        gps.read_gps_data()

        # Same instance should be updated
        assert data.latitude == pytest.approx(48.1173, rel=0.001)
