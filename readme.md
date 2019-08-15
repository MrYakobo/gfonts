# gfonts

This is a tool to download Google Fonts for use locally. It depends on `python3` and `BeautifulSoup`.

The table below shows where fonts are placed by default.

| Linux                |      MacOS      | Windows and other OSes |
|----------------------|:---------------:|:----------------------:|
| ~/.local/share/fonts | ~/Library/fonts |      $HOME/gfonts      |

# Try it

`curl -L git.io/gfonts | python3`

# Install it

```bash
curl -L git.io/gfonts > ~/bin/gfonts
chmod +x ~/bin/gfonts
gfonts
```