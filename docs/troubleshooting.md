# Troubleshooting

Lessons from running this on a budget Android 13 projector. Start with the diagnostics link (short link + `d`,
or `?diag=1`): it shows the mode, screen size, memory, how many photos are stored and decoded, the audio state
and show timing.

## Photos

| Symptom | Cause and fix |
|---|---|
| Frames show only the top strip of a photo, or stay blank | GPU tile memory exhausted. Keep `NW` at 200 (frames are laid out at NW px, then warped; 1000 px frames starved the GPU). Keep photos at 1280 px (`prepare-album.py` default) and the album under ~30 MB |
| Photos take 10-15 s to appear, or the next photo arrives before the last appeared | Slow devices decode slowly. The page decodes off-screen first and never changes a frame faster than every 60 s; don't lower the interval |
| Only some photos downloaded on the first start | Interrupted download; the page resumes missing or incomplete files (byte sizes in album.js) on the next start: reload |
| Photos look soft | Most budget projectors render apps at 1280x720. Check with `?res=1` (stripes should be crisp). Try the projector's 1080p output setting, or move the projector closer (re-align after) |
| Light spills onto the black frames | Pull the corners slightly inside the opening (Align); dim the room |
| Old photos stay after changing the album | Each browser re-places album photos when album.js changes: reload the page on the projector |

## Sound

| Symptom | Cause and fix |
|---|---|
| Sound test silent | Projector volume / mute first. Then Fully: Web Content Settings → Autoplay Videos ON. Some projectors lose audio after standby: reboot |
| Show starts silently with a "sound is blocked" message | The browser needs a user gesture: press any remote key and the music joins at the right point |
| Music stops after a few seconds | Only happens with `?music=live` (live synthesis is too heavy). The default plays the pre-rendered files |
| Music and visuals drift | Visuals follow the music file's clock; if the projector is very slow the visuals drop detail automatically |

## Remote and kiosk

| Symptom | Cause and fix |
|---|---|
| OK does nothing | Use the key log (short link + `k`) to see what the remote sends; the page treats Enter and Select as OK |
| Back leaves the wall or shows an old page | The page keeps its own history entry so Back stays on the wall; restart Fully once to clear older history |
| Menu doesn't appear | It opens with an arrow key while in Play; in Align, OK after the 4th corner opens the Align menu |
| Wall doesn't come back after a power cut | Fully: Launch on Boot ON; check the projector's own "start app on boot" options |

## Alignment

| Symptom | Cause and fix |
|---|---|
| Alignment from alignment.json not applied | It applies once per new file and only if it has the same number of frames as config.js |
| Everything shifted | The projector moved or keystone/zoom changed: re-align, or restore the exact old position |

## Measuring performance

`?fps=1` shows the frame rate. Shows reduce their particle count automatically when drawing is slow.
`?vector=1` (no photos) separates photo/memory problems from drawing problems.
