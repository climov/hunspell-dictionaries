# Dzonghka syllable spellchecker for Hunspell

You can find here the necessary files to use spell checking for Dzongkha at syllable level (not composed words) in [Hunspell](http://hunspell.sourceforge.net/) (used in [many applications](https://en.wikipedia.org/wiki/Hunspell#Uses)).

Note that checking compound words for Dzongkha is not possible with hunspell alone due to the absence of separation between words.

This work is largely based on the [Classical Tibetan spell checker](https://github.com/eroux/hunspell-dz), see [documentation](doc/).

## Using

#### Global installation

Under Linux or OSX, you can install the spellchecker globally and benefit from it in most applications.

- under Linux, copy `dz.dic` and `dz.aff` to `/usr/share/hunspell`
- Under OSX, copy `dz.dic` and `dz.aff` to `/Library/Spelling` and restart your machine

#### Application-specific installation

- extensions will be released for Firefox and LibreOffice
- for Adobe products (>= CS5.5), see the instructions on [this page](http://blog.napsys.com/2012/11/adding-hyphenation-and-spelling.html)

## Changes

See [CHANGELOG.md](CHANGELOG.md).

## Thanks

This spell checker has been made possible with the help of:
- Pema Galey (པདྨ་དགེ་ལེགས།)
- the [Dzongkha Development Commission](http://www.dzongkha.gov.bt/)

## License

This work and the derived files are under the [Creative Commons CC0 license](LICENSE).
