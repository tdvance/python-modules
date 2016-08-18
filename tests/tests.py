from unittest import TestCase

from util.mkdict import MKDict
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
        self.assertEqual(Tag('xY', 2), tags.get_from_key('Xy'))


class TestMKDict(TestCase):
    def setUp(self):
        num_tag_sets = 20
        num_mkdicts = 20
        num_tags = 20
        self.tags = []
        for iteration in range(num_tags):
            i = (iteration * iteration - iteration + num_tags) % num_tags
            if iteration % 3 == 0:
                j = 2 * iteration * iteration + 3 * iteration + 1
                tag = Tag('x' + str(i), j)
            elif iteration % 3 == 1:
                j = 3 * iteration * iteration + 2 * iteration + 5
                tag = Tag('x' + str(i), j)
            else:
                tag = Tag('x' + str(i))
            self.tags.append(tag)

        self.t = []
        for iteration in range(num_tag_sets):
            tl = []
            for i in range(iteration):
                ii = (i * i * i + 2 * i + 3) % num_tags
                tl.append(self.tags[ii])
            ts = TagSet(*tl)
            self.t.append(ts)

        self.m = []
        for iteration in range(num_mkdicts):
            self.m.append(MKDict())
            for i in range(iteration):
                ii = (i * i * i + 2 * i + 3) % num_tag_sets
                self.m[iteration][self.t[
                    ii]] = 2 * iteration * iteration + 3 * iteration + 1

    def test_constructor(self):
        m = MKDict()
        self.assertEqual(0, len(m))

    def test_put_adds_one(self):
        for m in self.m:
            for t in self.t:
                if t in m:
                    mm = m.copy()
                    mm[t] = m[t]
                    self.assertEqual(mm, m)
                else:
                    mm = m.copy()
                    mm[t] = 12
                    self.assertEqual(len(m) + 1, len(mm))

    def test_remove_subtracts_one(self):
        for m in self.m:
            for t in self.t:
                if t not in m:
                    mm = m.copy()
                    mm.pop(t, None)
                    self.assertEqual(mm, m)
                else:
                    mm = m.copy()
                    del mm[t]
                    self.assertEqual(len(m) - 1, len(mm))

    def test_empty_contains_none(self):
        m = MKDict()
        for t in self.t:
            self.assertFalse(t in m)

    def test_put_contains_element(self):
        for m in self.m:
            for t in self.t:
                mm = m.copy()
                mm[t] = 123
                self.assertTrue(t in mm)

    def test_put_no_effect_other_keys(self):
        for m in self.m:
            for t in self.t:
                for u in self.t:
                    if t != u:
                        mm = m.copy()
                        mm[t] = 123
                        self.assertEqual(u in m, u in mm)

    def test_remove_not_contains_element(self):
        for m in self.m:
            for t in self.t:
                mm = m.copy()
                mm.pop(t, None)
                self.assertFalse(t in mm)

    def test_remove_no_effect_other_keys(self):
        for m in self.m:
            for t in self.t:
                for u in self.t:
                    if t != u:
                        mm = m.copy()
                        mm.pop(t, None)
                        self.assertEqual(u in m, u in mm)
