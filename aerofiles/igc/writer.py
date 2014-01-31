from aerofiles.igc import patterns


class Writer:
    """
    A writer for the IGC flight log file format.

    see http://www.fai.org/gnss-recording-devices/igc-approved-flight-recorders
    or http://carrier.csi.cam.ac.uk/forsterlewis/soaring/igc_file_format/igc_format_2008.html
    """

    def __init__(self, fp=None):
        self.fp = fp

    def write_line(self, line):
        self.fp.write(line + '\r\n')

    def write_logger_id(self, manufacturer, logger_id, extension=None,
                        validate=True):
        if validate:
            if not patterns.MANUFACTURER_CODE.match(manufacturer):
                raise ValueError('Invalid manufacturer code')
            if not patterns.LOGGER_ID.match(logger_id):
                raise ValueError('Invalid logger id')

        line = 'A%s%s' % (manufacturer, logger_id)
        if extension:
            line = line + extension

        self.write_line(line)

    def write_header(self, source, subtype, value,
                     subtype_long=None, value_long=None):
        if source not in ('F', 'O'):
            raise ValueError('Invalid source')

        if not subtype_long:
            line = 'H%s%s%s' % (source, subtype, value)
        elif not value_long:
            line = 'H%s%s%s:%s' % (source, subtype, subtype_long, value)
        else:
            line = 'H%s%s%s%s:%s' % \
                (source, subtype, value, subtype_long, value_long)

        self.write_line(line)

    def write_fr_header(self, subtype, value,
                        subtype_long=None, value_long=None):
        self.write_header(
            'F', subtype, value,
            subtype_long=subtype_long, value_long=value_long
        )

    def write_date(self, date):
        self.write_fr_header('DTE', date.strftime('%y%m%d'))

    def write_fix_accuracy(self, accuracy=500):
        accuracy = int(accuracy)
        if not 0 < accuracy < 1000:
            raise ValueError('Invalid fix accuracy')

        self.write_fr_header('FXA', accuracy)

    def write_pilot(self, pilot):
        self.write_fr_header('PLT', pilot, subtype_long='PILOTINCHARGE')

    def write_copilot(self, copilot):
        self.write_fr_header('CM2', copilot, subtype_long='CREW2')

    def write_glider_type(self, glider_type):
        self.write_fr_header('GTY', glider_type, subtype_long='GLIDERTYPE')

    def write_glider_id(self, glider_id):
        self.write_fr_header('GID', glider_id, subtype_long='GLIDERID')

    def write_gps_datum(self, code=100, gps_datum='WGS-1984'):
        self.write_fr_header(
            'DTM', code, subtype_long='GPSDATUM', value_long=gps_datum)

    def write_firmware_version(self, firmware_version):
        self.write_fr_header(
            'RFW', firmware_version, subtype_long='FIRMWAREVERSION')
