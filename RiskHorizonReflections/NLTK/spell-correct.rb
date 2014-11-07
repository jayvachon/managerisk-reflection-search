
# be sure to have ffi-aspell installed: https://github.com/YorickPeterse/ffi-aspell

require 'ffi/aspell'

def correct_spelling(speller, word)
	if speller.correct?(word)
		return word
	else
		return speller.suggestions(word)[0]
	end
end

speller = FFI::Aspell::Speller.new('en_US')
puts correct_spelling(speller, 'cokie')
speller.close