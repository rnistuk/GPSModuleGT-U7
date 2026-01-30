"""
Tests for GPSData dataclass.
"""
import pytest
from gps_data import GPSData


class TestGPSData:
    """Tests for GPSData dataclass."""

    def test_default_values(self, gps_data):
        """Test that GPSData initializes with correct defaults."""
        assert gps_data.latitude == 0.0
        assert gps_data.longitude == 0.0
        assert gps_data.lat_dir == ''
        assert gps_data.lon_dir == ''
        assert gps_data.height == 0.0
        assert gps_data.num_sats == 0
        assert gps_data.gps_quality == 0

    def test_custom_values(self):
        """Test GPSData with custom values."""
        data = GPSData(
            latitude=49.2827,
            longitude=-123.1207,
            lat_dir='N',
            lon_dir='W',
            height=70.5,
            num_sats=8,
            gps_quality=1
        )
        assert data.latitude == 49.2827
        assert data.longitude == -123.1207
        assert data.lat_dir == 'N'
        assert data.lon_dir == 'W'
        assert data.height == 70.5
        assert data.num_sats == 8
        assert data.gps_quality == 1


class TestGPSDataIsValid:
    """Tests for GPSData.is_valid() method."""

    def test_is_valid_with_fix(self, sample_gps_data):
        """Test is_valid returns True with GPS fix."""
        assert sample_gps_data.is_valid() is True

    def test_is_valid_no_quality(self):
        """Test is_valid returns False with no GPS quality."""
        data = GPSData(num_sats=5, gps_quality=0)
        assert data.is_valid() is False

    def test_is_valid_no_satellites(self):
        """Test is_valid returns False with no satellites."""
        data = GPSData(num_sats=0, gps_quality=1)
        assert data.is_valid() is False

    def test_is_valid_default(self, gps_data):
        """Test is_valid returns False for default data."""
        assert gps_data.is_valid() is False


class TestGPSDataHasPosition:
    """Tests for GPSData.has_position() method."""

    def test_has_position_with_coordinates(self, sample_gps_data):
        """Test has_position returns True with coordinates."""
        assert sample_gps_data.has_position() is True

    def test_has_position_latitude_only(self):
        """Test has_position returns True with only latitude."""
        data = GPSData(latitude=49.2827)
        assert data.has_position() is True

    def test_has_position_longitude_only(self):
        """Test has_position returns True with only longitude."""
        data = GPSData(longitude=-123.1207)
        assert data.has_position() is True

    def test_has_position_at_origin(self):
        """Test has_position returns False at 0,0 (edge case)."""
        data = GPSData(latitude=0.0, longitude=0.0)
        assert data.has_position() is False

    def test_has_position_default(self, gps_data):
        """Test has_position returns False for default data."""
        assert gps_data.has_position() is False


class TestGPSDataToDict:
    """Tests for GPSData.to_dict() method."""

    def test_to_dict_contains_all_fields(self, sample_gps_data):
        """Test to_dict returns all expected fields."""
        result = sample_gps_data.to_dict()

        expected_keys = ['latitude', 'longitude', 'lat_dir', 'lon_dir',
                         'height', 'num_sats', 'gps_quality']
        assert set(result.keys()) == set(expected_keys)

    def test_to_dict_values_match(self, sample_gps_data):
        """Test to_dict values match original data."""
        result = sample_gps_data.to_dict()

        assert result['latitude'] == sample_gps_data.latitude
        assert result['longitude'] == sample_gps_data.longitude
        assert result['lat_dir'] == sample_gps_data.lat_dir
        assert result['lon_dir'] == sample_gps_data.lon_dir
        assert result['height'] == sample_gps_data.height
        assert result['num_sats'] == sample_gps_data.num_sats
        assert result['gps_quality'] == sample_gps_data.gps_quality

    def test_to_dict_default_values(self, gps_data):
        """Test to_dict with default values."""
        result = gps_data.to_dict()

        assert result['latitude'] == 0.0
        assert result['longitude'] == 0.0
        assert result['lat_dir'] == ''
        assert result['lon_dir'] == ''
        assert result['height'] == 0.0
        assert result['num_sats'] == 0
        assert result['gps_quality'] == 0
