"""
Tests for NMEA parser.
"""
import pytest
from gps_data import GPSData


# Import with fallback for different import styles
try:
    from nmea_parser import NMEAParser, NMEA_GPS_PREFIX
except ImportError:
    from source.nmea_parser import NMEAParser, NMEA_GPS_PREFIX


class TestNMEAParserBasics:
    """Basic tests for NMEAParser."""

    @pytest.fixture
    def parser(self, gps_data):
        """Create parser with fresh GPS data."""
        return NMEAParser(gps_data)

    def test_parser_initialization(self, gps_data):
        """Test parser initializes with GPS data reference."""
        parser = NMEAParser(gps_data)
        assert parser._data is gps_data

    def test_parse_empty_sentence(self, parser):
        """Test parsing empty string returns False."""
        result = parser.parse_sentence("")
        assert result is False

    def test_parse_none_sentence(self, parser):
        """Test parsing None returns False."""
        result = parser.parse_sentence(None)
        assert result is False

    def test_parse_non_gps_sentence(self, parser):
        """Test parsing non-GPS NMEA sentence returns False."""
        # GLONASS sentence (starts with $GL)
        result = parser.parse_sentence("$GLGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M*47")
        assert result is False

    def test_parse_invalid_sentence(self, parser):
        """Test parsing malformed sentence returns False."""
        # Malformed sentence without proper structure
        result = parser.parse_sentence("$GPXXX,invalid,data")
        assert result is False


class TestNMEAParserGGA:
    """Tests for parsing GGA (Global Positioning System Fix Data) sentences."""

    @pytest.fixture
    def parser(self, gps_data):
        return NMEAParser(gps_data)

    def test_parse_gga_extracts_position(self, parser, gps_data):
        """Test GGA sentence extracts latitude and longitude."""
        # Valid GGA sentence with correct checksum
        sentence = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,47.0,M,,*4F"

        result = parser.parse_sentence(sentence)

        assert result is True
        # pynmea2 converts to decimal degrees
        assert gps_data.latitude == pytest.approx(48.1173, rel=0.001)
        assert gps_data.longitude == pytest.approx(11.5167, rel=0.001)

    def test_parse_gga_extracts_direction(self, parser, gps_data):
        """Test GGA sentence extracts lat/lon directions."""
        sentence = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,47.0,M,,*4F"

        parser.parse_sentence(sentence)

        assert gps_data.lat_dir == 'N'
        assert gps_data.lon_dir == 'E'

    def test_parse_gga_extracts_altitude(self, parser, gps_data):
        """Test GGA sentence extracts altitude."""
        sentence = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,47.0,M,,*4F"

        parser.parse_sentence(sentence)

        assert gps_data.height == pytest.approx(545.4, rel=0.01)

    def test_parse_gga_extracts_satellites(self, parser, gps_data):
        """Test GGA sentence extracts satellite count."""
        sentence = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,47.0,M,,*4F"

        parser.parse_sentence(sentence)

        assert gps_data.num_sats == 8

    def test_parse_gga_extracts_quality(self, parser, gps_data):
        """Test GGA sentence extracts GPS quality indicator."""
        sentence = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,47.0,M,,*4F"

        parser.parse_sentence(sentence)

        assert gps_data.gps_quality == 1

    def test_parse_gga_no_fix(self, parser, gps_data):
        """Test GGA sentence with no fix (quality=0)."""
        sentence = "$GPGGA,123519,,,,,0,00,,,M,,M,,*6B"

        result = parser.parse_sentence(sentence)

        assert result is True
        assert gps_data.gps_quality == 0
        assert gps_data.num_sats == 0


class TestNMEAParserRMC:
    """Tests for parsing RMC (Recommended Minimum) sentences."""

    @pytest.fixture
    def parser(self, gps_data):
        return NMEAParser(gps_data)

    def test_parse_rmc_extracts_position(self, parser, gps_data):
        """Test RMC sentence extracts position."""
        sentence = "$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A"

        result = parser.parse_sentence(sentence)

        assert result is True
        assert gps_data.latitude == pytest.approx(48.1173, rel=0.001)
        assert gps_data.longitude == pytest.approx(11.5167, rel=0.001)

    def test_parse_rmc_extracts_direction(self, parser, gps_data):
        """Test RMC sentence extracts directions."""
        sentence = "$GPRMC,123519,A,4807.038,S,01131.000,W,022.4,084.4,230394,003.1,W*65"

        parser.parse_sentence(sentence)

        assert gps_data.lat_dir == 'S'
        assert gps_data.lon_dir == 'W'


class TestNMEAParserMultipleSentences:
    """Tests for parsing multiple NMEA sentences."""

    @pytest.fixture
    def parser(self, gps_data):
        return NMEAParser(gps_data)

    def test_parse_multiple_updates_data(self, parser, gps_data):
        """Test multiple sentences update data progressively."""
        # First sentence sets position
        sentence1 = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,47.0,M,,*4F"
        parser.parse_sentence(sentence1)

        initial_lat = gps_data.latitude

        # Second sentence with different position
        sentence2 = "$GPGGA,123520,4907.038,N,01231.000,E,1,10,0.8,600.0,M,47.0,M,,*49"
        parser.parse_sentence(sentence2)

        # Data should be updated
        assert gps_data.latitude != initial_lat
        assert gps_data.num_sats == 10
        assert gps_data.height == pytest.approx(600.0, rel=0.01)
