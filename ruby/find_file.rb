require 'fileutils'

path = Dir.pwd
lockfile = path + "/secrets.lock"

out_file = File.new(lockfile, "w")

out_file.puts("Secrets file created " + Time.now.inspect)
out_file.close

if(File.exist?(lockfile))
  puts 'file or directory exists'
else
  puts 'file or directory not found'
end

puts path
puts Time.now.inspect
