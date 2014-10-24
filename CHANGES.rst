0.6.1 (2014-07-10)
------------------
- Return None if an action fails validation (instead of raising an exception)

0.6.0 (2014-06-23)
------------------
- Added Trakt.configure() method
- Rebuild session on socket.gaierror (workaround for urllib error)

0.5.3 (2014-05-10)
------------------
- Fixed bugs sending media actions
- Renamed cancel_watching() to cancelwatching()
- "title" and "year" parameters are now optional on media actions

0.5.2 (2014-04-20)
------------------
- [movie] Added seen(), library() and unlibrary() methods
- [movie] Implemented media mapping
- [rate] Added shows(), episodes() and movies() methods
- [show] Added unlibrary() method
- [show/episode] Added library() and seen() methods

0.5.1 (2014-04-19)
------------------
- Added @authenticated to MediaInterface.send()
- Fixed missing imports

0.5.0 (2014-04-18)
------------------
- Initial release