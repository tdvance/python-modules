from unittest import TestCase

from util.switch import switch
from util.tag import Tag
from util.tag_set import TagSet


def func_a(arg1, arg2):
    return 'a' + str(arg1) + str(arg2)


def func_b(arg1, arg2):
    return 'b' + str(arg1) + str(arg2)


def func_c(arg1, arg2):
    return 'c' + str(arg1) + str(arg2)


def func_d(arg1, arg2):
    return 'd' + str(arg1) + str(arg2)


class TestSwitch(TestCase):
    def test_switch(self):
        value = 'a'
        result = switch(value, 'xx', 'yy', a=func_a, b=func_b, c=func_c,
                        default=func_d)
        self.assertEqual('axxyy', result)
        value = 'b'
        result = switch(value, 'xx', 'yy', a=func_a, b=func_b, c=func_c,
                        default=func_d)
        self.assertEqual('bxxyy', result)
        value = 'c'
        result = switch(value, 'xx', 'yy', a=func_a, b=func_b, c=func_c,
                        default=func_d)
        self.assertEqual('cxxyy', result)
        value = 'x'
        result = switch(value, 'xx', 'yy', a=func_a, b=func_b, c=func_c,
                        default=func_d)
        self.assertEqual('dxxyy', result)


class TestTag(TestCase):
    def test_tag(self):
        t = Tag('  _aBC__123   XyZ_   ', 12.3)
        self.assertEqual('abc_123_xyz', t.key)
        self.assertEqual('  _aBC__123   XyZ_   ', t.name)
        self.assertEqual(12.3, t.value)

    def test_tag_set(self):
        tags = TagSet(Tag('a', 1), Tag('abc'), Tag('xy', 2))
        self.assertTrue(Tag(' A ', 1) in tags)
        self.assertTrue((tags.contains_key('ABC')))
        self.assertEqual(Tag('xY',2), tags.get_from_key('Xy'))
