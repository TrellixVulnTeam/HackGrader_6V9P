require_relative "solution"
require "test/unit"

class TestSimpleNumber < Test::Unit::TestCase

  def test_add_positive
    assert_equal(4, add(3, 1))
    assert_equal(15, add(7, 8))
  end

  def test_add_negative
    assert_equal(-10, add(-6, -4))
    assert_equal(-25, add(-20, -5))
  end

  def test_add_positive_and_negative
    assert_equal(0, add(-5, 5))
    assert_equal(-1, add(-9, 8))
  end

end