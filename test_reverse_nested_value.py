import pytest
from reverse_nested_value import InvalidFormat, serialize, deserialize, reverse_nested_value


def test_as_is():
    input_value = '''{
  'hired': {
    'be': {
      'to': {
        'deserve': 'I'
      }
    }
  }
}'''
    expected = '''{
  'I': {
    'deserve': {
      'to': {
        'be': 'hired'
      }
    }
  }
}'''
    out = reverse_nested_value(input_value, 2)
    assert(out == expected)


def test_extra_curly_brace():
    input_value = '''{
  'hired': {
    'be': {
      'to': {
        'deserve': 'I'
        }
      }
    }
  }
}'''
    with pytest.raises(InvalidFormat, match=r'.*parentheses.*'):
        reverse_nested_value(input_value, 2)


def test_insufficient_curly_brace():
    input_value = '''{
  'hired': {
    'be': {
      'to': {
        'deserve': 'I'
    }
  }
}'''
    with pytest.raises(InvalidFormat):
        reverse_nested_value(input_value, 2)


def test_open_quote():
    input_value = '''{
  'hired': {
    'be': {
      'to': {
        'deserve': 'I
      }
    }
  }
}'''
    with pytest.raises(InvalidFormat):
        reverse_nested_value(input_value, 2)


def test_orphan_characters():
    input_value = '''{
  'hired': {
    'be': {
      'to': {
        'deserve': 'I' xx
      }
    }
  }
}'''
    with pytest.raises(InvalidFormat):
        reverse_nested_value(input_value, 2)

