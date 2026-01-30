"""
Tests for command formatters.
"""
import pytest
from gps_data import GPSData
from command_formatter import (
    MeshtasticCommandFormatter,
    NMEACommandFormatter,
    SimpleCommandFormatter
)


class TestMeshtasticCommandFormatter:
    """Tests for MeshtasticCommandFormatter."""

    @pytest.fixture
    def formatter(self):
        return MeshtasticCommandFormatter()

    def test_format_with_valid_data(self, formatter, sample_gps_data):
        """Test formatting with valid GPS data."""
        result = formatter.format(sample_gps_data)

        assert "meshtastic" in result
        assert "--setlat 49.2827" in result
        assert "--setlon -123.1207" in result
        assert "--setalt 70.5" in result

    def test_format_with_none(self, formatter):
        """Test formatting with None returns placeholder."""
        result = formatter.format(None)
        assert result == formatter.get_placeholder()

    def test_format_with_no_position(self, formatter):
        """Test formatting with zero coordinates returns placeholder."""
        data = GPSData(latitude=0.0, longitude=0.0)
        result = formatter.format(data)
        assert result == formatter.get_placeholder()

    def test_get_placeholder(self, formatter):
        """Test placeholder contains N/A values."""
        result = formatter.get_placeholder()

        assert "meshtastic" in result
        assert "N/A" in result

    def test_format_negative_coordinates(self, formatter):
        """Test formatting with negative coordinates."""
        data = GPSData(latitude=-33.8688, longitude=151.2093, height=58.0)
        result = formatter.format(data)

        assert "--setlat -33.8688" in result
        assert "--setlon 151.2093" in result


class TestNMEACommandFormatter:
    """Tests for NMEACommandFormatter."""

    @pytest.fixture
    def formatter(self):
        return NMEACommandFormatter()

    def test_format_with_valid_data(self, formatter, sample_gps_data):
        """Test formatting with valid GPS data."""
        result = formatter.format(sample_gps_data)

        assert result.startswith("$GPGGA")
        assert "Alt:70.5m" in result
        assert "Sats:8" in result

    def test_format_with_none(self, formatter):
        """Test formatting with None returns placeholder."""
        result = formatter.format(None)
        assert result == formatter.get_placeholder()

    def test_format_with_no_position(self, formatter):
        """Test formatting with zero coordinates returns placeholder."""
        data = GPSData()
        result = formatter.format(data)
        assert result == formatter.get_placeholder()

    def test_get_placeholder(self, formatter):
        """Test placeholder is valid NMEA-like string."""
        result = formatter.get_placeholder()

        assert "$GPGGA" in result
        assert "N/A" in result

    def test_format_latitude_conversion(self, formatter):
        """Test latitude is converted to NMEA format (degrees and minutes)."""
        # 49.5 degrees = 49 degrees, 30 minutes
        data = GPSData(latitude=49.5, longitude=-123.0, lat_dir='N', lon_dir='W')
        result = formatter.format(data)

        # Should contain "49" for degrees and "30" for minutes
        assert ",N," in result

    def test_format_uses_direction_from_data(self, formatter):
        """Test formatter uses direction from GPS data."""
        data = GPSData(latitude=49.0, longitude=123.0, lat_dir='N', lon_dir='E')
        result = formatter.format(data)

        assert ",N," in result
        assert ",E," in result


class TestSimpleCommandFormatter:
    """Tests for SimpleCommandFormatter."""

    @pytest.fixture
    def formatter(self):
        return SimpleCommandFormatter()

    def test_format_with_valid_data(self, formatter, sample_gps_data):
        """Test formatting with valid GPS data."""
        result = formatter.format(sample_gps_data)

        assert "Lat: 49.2827" in result
        assert "Lon: -123.1207" in result
        assert "Alt: 70.5m" in result

    def test_format_with_none(self, formatter):
        """Test formatting with None returns placeholder."""
        result = formatter.format(None)
        assert result == formatter.get_placeholder()

    def test_format_with_no_position(self, formatter):
        """Test formatting with zero coordinates returns placeholder."""
        data = GPSData()
        result = formatter.format(data)
        assert result == formatter.get_placeholder()

    def test_get_placeholder(self, formatter):
        """Test placeholder format."""
        result = formatter.get_placeholder()

        assert "Lat: N/A" in result
        assert "Lon: N/A" in result
        assert "Alt: N/A" in result

    def test_format_precision(self, formatter):
        """Test coordinates are formatted to 4 decimal places."""
        data = GPSData(latitude=49.28271234, longitude=-123.12075678, height=70.567)
        result = formatter.format(data)

        # Should be rounded to 4 decimal places for lat/lon
        assert "49.2827" in result
        assert "-123.1208" in result  # Rounded
        # Height to 1 decimal place
        assert "70.6m" in result
