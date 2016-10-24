def fact(n)
  if n<= 1
    1
  else
    n * fact( n - 1 )
  end
end


def main()
  n = gets.chomp
  puts fact(n.to_i)
end

main()