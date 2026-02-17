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
    const targetSet = new Set(selectedPhonemes);
    const forcedSet = new Set(forcedPhonemes);
    
    let matches = Object.entries(wordDict).filter(([word, pron]) => {
        const wordPhonemes = pron.split(' ');
        const wordSet = new Set(wordPhonemes);

        // Check if all phonemes in word are in the allowed target set
        const isSubset = wordPhonemes.every(p => targetSet.has(p));
        if (!isSubset) return false;

        // If forced phonemes are provided, check if word contains all of them
        if (forcedSet.size > 0) {
            return [...forcedSet].every(p => wordSet.has(p));
        }

        return true;
    });

    // Sort by length
    return matches.sort((a, b) => a[0].length - b[0].length || a[0].localeCompare(b[0]));
}