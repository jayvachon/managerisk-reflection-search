
# be sure to have ffi-aspell installed: https://github.com/YorickPeterse/ffi-aspell

require 'ffi/aspell'

def correct_spelling(speller, word)
	if speller.correct?(word)
		return word
	else
		suggestions = speller.suggestions(word)
		if suggestions.length > 0
			return speller.suggestions(word)[0]
		else
			return word
		end
	end
end

# if I can figure out how to send an array, this might be faster...
def correct_spellings(speller, words)
	word_count = words.length
	corrections = []
	for i in 0..word_count
		corrections << correct_spelling(speller, words[i])
	end
	return corrections
end

speller = FFI::Aspell::Speller.new('en_US')

word = STDIN.gets
puts correct_spelling(speller, word)
STDOUT.flush
