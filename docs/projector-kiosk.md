# Projector: Fully Kiosk Browser

> **Recommended on any Android projector (or Android TV box): [Fully Kiosk Browser](https://www.fully-kiosk.com/).**
> The wall was built and tested with it. Other browsers can show the page, but they don't reliably stay
> full-screen, keep the screen awake, restart on boot, pass every remote key to the page or allow the show
> music to autoplay.

Fully Kiosk Browser shows one web page full-screen, keeps the screen on, restarts after power cuts and passes
the TV remote's keys to the page. Install it from the projector's app store, or download the APK from
fully-kiosk.com on the device. Some features need the paid PLUS licence (a greyed-out setting tells you), and menu names differ between
versions, so look for the settings below by name.

## Settings

| Setting (Fully) | Value | Why |
|---|---|---|
| Web Content Settings → Start URL | the short link, e.g. `photowall-xxxxxx.pages.dev/abc123` | the wall |
| Web Content Settings → Autoplay Videos | ON | lets the show music play without a tap (Web Audio counts as media) |
| Device Management → Keep Screen On | ON | no sleep |
| Device Management → Launch on Boot / Start on boot | ON | the wall comes back after a power cut |
| Screensaver | OFF | |
| Advanced Web Settings → Hardware Acceleration | ON (default) | smooth scenes |

Typing the start URL with a remote is the slowest part: that's why the short link exists. A USB/Bluetooth
keyboard or Fully's remote admin (PLUS) makes it easier.

## First start

1. Open the start URL. A progress bar ("Downloading photos", then "Getting the photos ready") runs once; the
   first time can take a minute or two over Wi-Fi.
2. All frames show photos. Press any arrow: the menu appears at the bottom.
3. Choose **Sound test**. No sound? Check the projector volume first, then Autoplay Videos, then reboot.

## Remote keys

- Arrows: open the menu / move in it; in Align: move the frame or corner (hold = bigger steps).
- OK: choose; in Align: step through corners, then the Align menu.
- Back: closes the menu or stops a show. It never leaves the wall (the page keeps its own history entry).
- If a key does nothing, open the short link + `k` to see what the remote sends.

## Auto-updates

Re-running `./deploy-cloudflare.sh` publishes changes; the projector picks them up on its next page load
(reboot, or Fully's reload). Changed photos are fetched automatically; unchanged ones are kept.
