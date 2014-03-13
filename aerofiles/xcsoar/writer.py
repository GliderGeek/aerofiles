import datetime
from contextlib import contextmanager


class Writer:
    def __init__(self, fp=None):
        self.fp = fp
        self.indent_level = 0

    def write_line(self, line):
        indent = '\t' * self.indent_level
        self.fp.write(indent + line + '\n')

    def format_tag_content(self, _name, **kw):
        params = map(lambda (k, v): '%s="%s"' % (k, v), kw.iteritems())
        params.sort()
        return _name + ' ' + ' '.join(params)

    def convert_bool(self, kw, key):
        if key in kw:
            value = kw[key]
            if isinstance(value, bool):
                kw[key] = (1 if value else 0)

    def convert_time(self, kw, key):
        if key in kw:
            value = kw[key]
            if isinstance(value, datetime.time):
                kw[key] = value.strftime('%H:%M')

    def convert_timedelta(self, kw, key):
        if key in kw:
            value = kw[key]
            if isinstance(value, datetime.timedelta):
                kw[key] = value.seconds

    @contextmanager
    def write_tag_with_content(self, _name, **kw):
        self.write_line('<%s>' % self.format_tag_content(_name, **kw))
        self.indent_level += 1
        yield
        self.indent_level -= 1
        self.write_line('</%s>' % _name)

    def write_tag(self, _name, **kw):
        self.write_line('<%s/>' % self.format_tag_content(_name, **kw))

    def write_task(self, **kw):
        self.convert_timedelta(kw, 'aat_min_time')
        self.convert_time(kw, 'start_open_time')
        self.convert_time(kw, 'start_close_time')
        self.convert_bool(kw, 'fai_finish')
        self.convert_bool(kw, 'start_requires_arm')

        return self.write_tag_with_content('Task', **kw)

    def write_point(self, **kw):
        return self.write_tag_with_content('Point', **kw)

    def write_waypoint(self, **kw):
        location_kw = {
            'latitude': kw['latitude'],
            'longitude': kw['longitude'],
        }

        del kw['latitude']
        del kw['longitude']

        with self.write_tag_with_content('Waypoint', **kw):
            self.write_tag('Location', **location_kw)

    def write_observation_zone(self, **kw):
        self.write_tag('ObservationZone', **kw)
