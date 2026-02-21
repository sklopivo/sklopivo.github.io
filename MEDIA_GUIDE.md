# Batch Media Guide

Add Instagram posts and photos to your batch detail pages.

## Quick Start

Edit `batch_media.json` to add media for your brews:

```json
{
  "BATCH_ID": {
    "instagram": [
      "https://www.instagram.com/p/YOUR_POST_ID/"
    ]
  }
}
```

## Finding Your Batch ID

1. Open your brewing showcase website
2. Click on a batch in the history
3. Look at the URL: `http://yoursite.com/#batch/BATCH_ID_HERE`
4. Copy the batch ID from the URL

## Adding Instagram Posts

### Simple Format (just URL):
```json
{
  "j93jjSZtQLkPG6x1CvJbhiqTaO6zie": {
    "instagram": [
      "https://www.instagram.com/p/ABC123/",
      "https://www.instagram.com/p/DEF456/"
    ]
  }
}
```

### With Captions:
```json
{
  "j93jjSZtQLkPG6x1CvJbhiqTaO6zie": {
    "instagram": [
      {
        "url": "https://www.instagram.com/p/ABC123/",
        "caption": "First batch of the year! Turned out amazing."
      },
      {
        "url": "https://www.instagram.com/reel/XYZ789/",
        "caption": "Time-lapse of the brew day"
      }
    ]
  }
}
```

## Adding Custom Images

```json
{
  "BATCH_ID": {
    "images": [
      {
        "url": "images/brew-day.jpg",
        "caption": "Brew day setup",
        "alt": "Photo of brewing equipment"
      },
      {
        "url": "images/final-pour.jpg",
        "caption": "Final product!",
        "alt": "Glass of finished beer"
      }
    ]
  }
}
```

## Combining Instagram and Images

```json
{
  "BATCH_ID": {
    "instagram": [
      "https://www.instagram.com/p/ABC123/"
    ],
    "images": [
      {
        "url": "images/special-photo.jpg",
        "caption": "Some photos not on Instagram"
      }
    ]
  }
}
```

## Full Example

```json
{
  "_readme": "Add media for your batches. Use batch ID from URL: #batch/BATCH_ID",

  "j93jjSZtQLkPG6x1CvJbhiqTaO6zie": {
    "instagram": [
      "https://www.instagram.com/p/ABC123/",
      {
        "url": "https://www.instagram.com/reel/DEF456/",
        "caption": "Brew day time-lapse"
      }
    ],
    "images": [
      {
        "url": "images/final-glass.jpg",
        "caption": "Perfect pour",
        "alt": "Glass of American IPA"
      }
    ]
  },

  "5SpZuyZY8EUzK05HWLGgxYQl4t7gzm": {
    "instagram": [
      "https://www.instagram.com/p/WITBEER123/"
    ]
  }
}
```

## Tips

- **Instagram URLs**: Must be full URLs like `https://www.instagram.com/p/POST_ID/`
- **Image paths**: Can be relative (e.g., `images/photo.jpg`) or absolute URLs
- **Multiple posts**: Array format allows multiple Instagram posts per batch
- **Captions**: Optional but recommended for context
- **Alt text**: Recommended for accessibility (images only)

## Display

Media appears in a "Brew Gallery" section at the bottom of the batch detail modal:
- Instagram posts show as embedded iFrames
- Images show as regular image elements
- Grid layout adapts to screen size
- Captions appear below each item

## Notes

- The `batch_media.json` file is optional - site works fine without it
- Media only shows for batches you've added to the config
- Instagram embeds require internet connection to load
- Keep `_readme` and `_example` in the file as documentation
