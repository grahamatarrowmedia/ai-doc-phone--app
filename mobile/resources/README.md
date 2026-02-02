# App Resources

## Icons Required

Place the following icon files in this directory:

### Master Icon
- `icon.png` - 1024x1024 PNG with app logo (no transparency recommended for Android)

### Splash Screen
- `splash.png` - 2732x2732 PNG for splash screen

## Generating Android Icons

After adding `icon.png`, use Capacitor's asset generation:

```bash
npm install -g @capacitor/assets
npx capacitor-assets generate --android
```

Or manually create these sizes in `android/app/src/main/res/`:

| Directory | Size | Purpose |
|-----------|------|---------|
| mipmap-mdpi | 48x48 | Medium density |
| mipmap-hdpi | 72x72 | High density |
| mipmap-xhdpi | 96x96 | Extra high density |
| mipmap-xxhdpi | 144x144 | Extra extra high density |
| mipmap-xxxhdpi | 192x192 | Extra extra extra high density |

## Recommended Icon Design

- Use the app's primary blue color (#2563eb) as background
- Film/documentary related iconography (film reel, camera, clapperboard)
- Keep design simple and recognizable at small sizes
- Avoid fine details that disappear at 48x48

## Splash Screen Design

- Center the app logo on solid background
- Use primary blue (#2563eb) or gradient to purple (#9333ea)
- Logo should be max 200x200 in center
- Remaining area is solid color
