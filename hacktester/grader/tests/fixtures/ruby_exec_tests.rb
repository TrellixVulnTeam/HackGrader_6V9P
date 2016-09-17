require 'minitest/autorun'

require_relative 'solution'

class SolutionTest < Minitest::Test
  def test_100_sms_number_to_message
    assert_equal 'abc', numbers_to_message([2, -1, 2, 2, -1, 2, 2, 2])
    assert_equal 'a', numbers_to_message([2, 2, 2, 2])
    assert_equal 'Ivo e Panda', numbers_to_message([1, 4, 4, 4, 8, 8, 8, 6, 6, 6, 0, 3, 3, 0, 1, 7, 7, 7, 7, 7, 2, 6, 6, 3, 2])
  end

  def test_100_sms_message_to_numbers
    assert_equal [2, -1, 2, 2, -1, 2, 2, 2], message_to_numbers('abc')
    assert_equal [2], message_to_numbers('a')
    assert_equal [1, 4, 4, 4, 8, 8, 8, 6, 6, 6, 0, 3, 3, 0, 1, 7, 2, 6, 6, 3, 2], message_to_numbers('Ivo e panda')
    assert_equal [2, -1, 2, -1, 2, 2, -1, 2, 2, -1, 2, 2, 2, -1, 2, 2, 2], message_to_numbers('aabbcc')
  end

  def test_spam_and_eggs
    assert_equal 'spam', prepare_meal(3)
    assert_equal 'spam spam spam', prepare_meal(27)
    assert_equal '', prepare_meal(7)

    assert_equal 'eggs', prepare_meal(5)
    assert_equal 'spam and eggs', prepare_meal(15)
    assert_equal 'spam spam and eggs', prepare_meal(45)
  end

  def test_reduce_file_path
    assert_equal '/', reduce_file_path('/')
    assert_equal '/', reduce_file_path('/srv/../')
    assert_equal '/srv/www/htdocs/wtf', reduce_file_path('/srv/www/htdocs/wtf/')
    assert_equal '/srv/www/htdocs/wtf', reduce_file_path('/srv/www/htdocs/wtf')
    assert_equal '/srv', reduce_file_path('/srv/./././././')
    assert_equal '/etc/wtf', reduce_file_path('/etc//wtf/')
    assert_equal '/', reduce_file_path('/etc/../etc/../etc/../')
    assert_equal '/', reduce_file_path('//////////////')
    assert_equal '/', reduce_file_path('/../')
  end

  def test_words_from_an_bn
    assert an_bn?('')
    assert !an_bn?('rado')
    assert !an_bn?('aaabb')
    assert an_bn?('aaabbb')
    assert !an_bn?('aabbaabb')
    assert !an_bn?('bbbaaa')
    assert an_bn?('aaaaabbbbb')
  end

  def test_credit_card_validation
    assert valid_credit_card?(79927398713)
    assert !valid_credit_card?(79927398715)
  end

  def test_goldbach_conjecture
    assert_equal [[2, 2]], goldbach(4)
    assert_equal [[3, 3]], goldbach(6)
    assert_equal [[3, 5]], goldbach(8)
    assert_equal [[3,7], [5,5]], goldbach(10)
    assert_equal [[3, 97], [11, 89], [17, 83], [29, 71], [41, 59], [47, 53]], goldbach(100)
  end

  def test_magic_square?
    assert !magic_square?([[1,2,3], [4,5,6], [7,8,9]])
    assert magic_square?([[4,9,2], [3,5,7], [8,1,6]])
    assert magic_square?([[7,12,1,14], [2,13,8,11], [16,3,10,5], [9,6,15,4]])
    assert magic_square?([[23, 28, 21], [22, 24, 26], [27, 20, 25]])
    assert !magic_square?([[16, 23, 17], [78, 32, 21], [17, 16, 15]])
  end
end

