# ⚠️ CURRENTLY NOT TESTED ON WINDOWS ⚠️

## Usage

I strongly suggest using a virtual enviroment  
you can generate a virtual enviroment with the command
```
python -m venv <virtual enviroment name (people generally use venv)>
```
after that you can use the enviroment's binaries generated in `<venv directory name>/bin/{pip, python}`  
for a more comprehensive explanation refer to the [documentation](https://docs.python.org/3/library/venv.html)

```
pip install -r requirements.txt
```
Add the channels you want to the channel_list.txt

Run it with
```
python youtube-channel-archiver.py

or

./youtube-channel-archiver.py
```

### How to get the channel ID's (I can only see the @ handle)
1. Go to the channel you would like to get the channel ID of
2. Inspect element or view source
3. Search for this string: ?channel_id=
4. The string after the equal sign is the channel ID of the channel

### Goals
- [ ] Option for downloading livestreams
- [ ] Saving the community tab
- [ ] Make a web interface

### The script is mostly commented explaining what the lines are doing  

Contributions are welcome as long as it is  
- Well written (Readable and Rational)
- Actual optimizations or a feature
- Not a useless thing (Like Code of Conduct)
