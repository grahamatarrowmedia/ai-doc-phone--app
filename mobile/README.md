# Documentary Production - Android App

Capacitor-based Android wrapper for the Documentary Production web application.

## Prerequisites

- Node.js 18+
- Android Studio (with Android SDK)
- Java 17+ (for Android builds)

## Quick Start

### 1. Install Dependencies

```bash
cd mobile
npm install
```

### 2. Configure Backend URL

Edit `capacitor.config.ts` and update the server URL to your Cloud Run backend:

```typescript
server: {
  url: 'https://doc-production-app-XXXXX.run.app',
  cleartext: false
}
```

### 3. Add Android Platform

```bash
npx cap add android
```

### 4. Sync Web Assets

```bash
npx cap sync android
```

### 5. Open in Android Studio

```bash
npx cap open android
```

## Building APK/AAB

### Debug APK (for testing)

```bash
cd android
./gradlew assembleDebug
```

Output: `android/app/build/outputs/apk/debug/app-debug.apk`

### Release AAB (for Play Store)

First, create a signing keystore:

```bash
keytool -genkey -v -keystore release.keystore -alias docprod -keyalg RSA -keysize 2048 -validity 10000
```

Then build:

```bash
cd android
./gradlew bundleRelease
```

Output: `android/app/build/outputs/bundle/release/app-release.aab`

## App Configuration

### AndroidManifest.xml Permissions

The app requires these permissions (already configured):

- `INTERNET` - Connect to Cloud Run backend
- `ACCESS_NETWORK_STATE` - Detect offline status
- `RECORD_AUDIO` - Speech input feature

### App Details

- **App ID**: `com.arrowmedia.docproduction`
- **App Name**: Documentary Production
- **Min SDK**: 22 (Android 5.1)
- **Target SDK**: 34 (Android 14)

## Generating App Icons

1. Place your 1024x1024 icon in `resources/icon.png`
2. Place your 2732x2732 splash in `resources/splash.png`
3. Generate assets:

```bash
npm install -g @capacitor/assets
npx capacitor-assets generate --android
```

## Development Workflow

1. Make changes to web app (main project)
2. Copy updated files to `www/` directory
3. Sync to Android: `npx cap sync android`
4. Build and test: `npx cap run android`

## Testing

### On Emulator

```bash
npx cap run android
```

### On Physical Device

1. Enable USB debugging on device
2. Connect via USB
3. Run: `npx cap run android --target=<device-id>`

## Play Store Submission

### Required Assets

- Privacy policy URL
- App screenshots (phone: 1080x1920, tablet: 1200x1920)
- Feature graphic: 1024x500
- App icon: 512x512 (high-res)

### Content Rating

Complete the content rating questionnaire in Play Console.

### Release Checklist

- [ ] Update version in `android/app/build.gradle`
- [ ] Build signed AAB
- [ ] Test on multiple devices
- [ ] Prepare store listing
- [ ] Submit for review

## Troubleshooting

### "Network Error" on launch

- Check the server URL in `capacitor.config.ts`
- Ensure Cloud Run backend is deployed and accessible
- Verify internet connectivity

### Build fails with Java error

Ensure JAVA_HOME points to Java 17+:

```bash
export JAVA_HOME=/path/to/java17
```

### Icons not updating

Clear Android build cache:

```bash
cd android
./gradlew clean
```

## Project Structure

```
mobile/
├── package.json          # Node dependencies
├── capacitor.config.ts   # Capacitor configuration
├── www/                  # Web assets
│   ├── index.html        # Standalone app
│   ├── css/style.css     # Styles
│   └── icons/            # Web icons
├── android/              # Android project (generated)
└── resources/            # Source assets for icon generation
```
