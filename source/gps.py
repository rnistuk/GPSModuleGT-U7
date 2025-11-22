import logging

from gps_data import GPSData
from nmea_parser import NMEAParser
from serial_port import ISerialPort, SerialPort

logger = logging.getLogger(__name__)


class GT_U7GPS:
    def __init__(self, port='/dev/tty.usbmodem2101', baudrate=9600, timeout=1, serial_port: ISerialPort = None):
        """
        Initialize GPS module.

        Args:
            port: Serial port device path (used if serial_port not provided)
            baudrate: Communication speed (used if serial_port not provided)
            timeout: Read timeout in seconds (used if serial_port not provided)
            serial_port: Optional ISerialPort implementation for dependency injection
        """
        if serial_port is None:
            self.ser = SerialPort(port, baudrate, timeout)
        else:
            self.ser = serial_port

        logger.info("GPS connected!")
        self._data = GPSData()
        self._parser = NMEAParser(self._data)

    @property
    def data(self) -> GPSData:
        """Get current GPS data."""
        return self._data

    # Backward compatibility properties
    @property
    def latitude(self) -> float:
        return self._data.latitude

    @property
    def longitude(self) -> float:
        return self._data.longitude

    @property
    def lat_dir(self) -> str:
        return self._data.lat_dir

    @property
    def lon_dir(self) -> str:
        return self._data.lon_dir

    @property
    def height(self) -> float:
        return self._data.height

    @property
    def num_sats(self) -> int:
        return self._data.num_sats

    @property
    def gps_quality(self) -> int:
        return self._data.gps_quality

    def close(self):
        if hasattr(self, 'ser') and self.ser.is_open():
            self.ser.close()
            logger.debug("GPS disconnected!")

    def _read_nmea_sentence(self):
        """Read and decode a single NMEA sentence from serial port."""
        try:
            return self.ser.readline().decode('utf-8').strip()
        except UnicodeDecodeError as e:
            logger.error(f"Error decoding NMEA: {e}")
            return None

    def read_gps_data(self):
        """Read and process all available GPS data from serial port."""
        try:
            while self.ser.in_waiting() > 0:
                nmea_sentence = self._read_nmea_sentence()
                if nmea_sentence:
                    self._parser.parse_sentence(nmea_sentence)
        except Exception as e:
            logger.error(f"Error reading serial port: {e}")
            raise RuntimeError(f"Failed to read GPS serial port: {e}")
