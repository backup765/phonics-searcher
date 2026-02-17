const PHONEMES = [
    'S', 'T', 'P', 'N', 'M', 'F', 'L', 'K', 'D', 'G', 'B', 'V', 'Z',
    'R', 'HH', 'JH', 'CH', 'SH', 'TH', 'DH', 'NG', 'Y', 'W',
    'AE', 'IH', 'EH', 'AA', 'UH', 'AH', 'EY', 'AY', 'OW', 'AW',
    'OY', 'UW', 'ER', 'AO'
];

/**
 * Logic to search the dictionary
 * @param {Object} wordDict - The JSON data
 * @param {Array} selectedPhonemes - Allowed phonemes
 * @param {Array} forcedPhonemes - Required phonemes
 */
function searchSubset(wordDict, selectedPhonemes, forcedPhonemes = []) {
    // Turn the inputs into sets
    const targetSet = new Set(selectedPhonemes);
    const forcedSet = new Set(forcedPhonemes);

    // Finds all the matches in the input dictionary
    // For each item, the pronunciation is split into a set, then checked against
    //   the input sets. If it matches both, the => returns true, and the item is
    //   kept, otherwise it is filtered
    let matches = Object.entries(wordDict).filter(([word, pron]) => {
        // Turn phoneme part into a set
        const wordPhonemes = pron.split(' ');
        const wordSet = new Set(wordPhonemes);

        // Check if all phonemes in word are in the allowed target set
        // .every() checks all elements, using the condition that each element
        //   p in wordPhonemes is in targetSet
        const isSubset = wordPhonemes.every(p => targetSet.has(p));
        if (!isSubset) return false;

        // If forced phonemes are provided, check if word contains all of them
        // ... operator expands forcedSet into an array, needed for .every()
        if (forcedSet.size > 0) {
            return [...forcedSet].every(p => wordSet.has(p));
        }

        return true;
    });

    // Sort the matches by length and return them
    // .sort() goes through all pairs in matches in nlogn, comparing based on the
    //   => function. The => first compares by length of the word, then goes alphabetically
    //   if the words are of the same length
    return matches.sort((a, b) => a[0].length - b[0].length || a[0].localeCompare(b[0]));
}