# 🍺 Sklopivo Brewing Statistics

Beautiful brewing analytics and showcase for your Brewfather batches, powered by GitHub Pages.

**Live Demo**: [View Showcase](https://sklopivo.github.io/)

## 📋 Overview

This project automatically generates comprehensive brewing statistics from your Brewfather account, including:

- **Interactive HTML Showcase** - Beautiful one-page website with charts and visualizations (Nuclear theme)
- **JSON Data** - Structured data for programmatic access
- **GitHub Pages Hosting** - Automatically deployed and publicly accessible
- **Automated Updates** - Manual GitHub Action to refresh data on demand

## 🚀 Quick Start

### 1. Fork or Clone This Repository

```bash
git clone https://github.com/sklopivo/sklopivo.github.io.git
cd sklopivo.github.io
```

### 2. Set Up GitHub Pages

1. Go to repository **Settings** → **Pages**
2. Under "Build and deployment":
   - **Source**: Deploy from a branch
   - **Branch**: `master`
   - **Folder**: `/ (root)`
3. Click **Save**
4. Your site will be available at: `https://sklopivo.github.io/`

### 3. Configure API Credentials

#### For GitHub Actions (Required for automated updates)

1. Go to repository **Settings** → **Secrets and variables** → **Actions**
2. Add two **Repository secrets**:
   - `BREWFATHER_USER_ID`: Your Brewfather user ID
   - `BREWFATHER_API_KEY`: Your Brewfather API key

Get your credentials from [Brewfather Settings → API Key](https://web.brewfather.app/tabs/settings)

#### For Local Development (Optional)

Create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```bash
BREWFATHER_USER_ID=your_user_id_here
BREWFATHER_API_KEY=your_api_key_here
```

Then load environment variables before running scripts:

```bash
export $(cat .env | xargs)
./refresh_stats.sh
```

## 🔄 Updating Statistics

### Option 1: Automatic (Push to Master)

Simply push any changes to the `master` branch, and GitHub Actions will automatically:
1. Fetch latest data from Brewfather
2. Generate statistics
3. Commit updated data to `master` branch
4. Update your live site

```bash
git add .
git commit -m "Update configuration"
git push origin master
```

### Option 2: Manual Trigger (GitHub Actions)

1. Go to **Actions** tab in your repository
2. Select **"Refresh Brewing Statistics"** workflow
3. Click **"Run workflow"** → **"Run workflow"**
4. Wait for the workflow to complete (~2-3 minutes)
5. Your GitHub Pages site will be automatically updated

### Option 3: Local Development

For local testing only (won't update live site):

```bash
# Load credentials
export $(cat .env | xargs)

# Run refresh script
./refresh_stats.sh

# Open locally
open index.html
```

## 📁 Repository Structure

```
sklopivo.github.io/
├── .github/
│   └── workflows/
│       └── refresh-stats.yml    # GitHub Actions workflow
├── index.html                   # Main showcase page (Nuclear theme)
├── brewing_statistics.json      # Generated statistics data
├── analyze_brewing_data.py      # Data analysis script
├── refresh_stats.sh            # Data refresh script
├── sklopivo_logo.png           # Logo
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## 📊 What Gets Analyzed

### Beer Statistics
- Total batches brewed
- Beer styles distribution
- Average ABV, IBU, batch size, efficiency
- Color (SRM) ranges

### Ingredients
- **Grains**: Types, quantities (kg), frequency of use
- **Hops**: Varieties, amounts (g), usage patterns with percentages
- **Yeasts**: Strains and frequency

### Timeline
- Complete monthly brewing timeline (includes empty months)
- Yearly and monthly trends
- Batch progression over time

### Visualizations
- Beer styles bar chart
- Monthly brewing timeline (with all months)
- Hop varieties doughnut chart (sorted with percentages)
- Interactive ingredient lists
- Clickable brewing history with batch details modal

## 🎨 Theme & Customization

The showcase uses the **Nuclear theme** from Bulmaswatch:
- **Cyberpunk aesthetic** with neon lime/green colors
- **Primary**: #d9ff00 (neon lime)
- **Secondary**: #00ff48 (neon green)
- **Accent**: #0ff (cyan)
- **Font**: Varela Round (Google Fonts)

### Change Colors

Edit `index.html` CSS variables:

```css
:root {
    --black: #080808;
    --dark-gray: #131313;
    --primary: #d9ff00;
    --secondary: #00ff48;
    --accent: #0ff;
}
```

### Modify Analysis

Edit `analyze_brewing_data.py` to add new metrics or change report format.

## 🔐 Security

- ✅ `.env` file is in `.gitignore` (local credentials never committed)
- ✅ API credentials stored as GitHub Secrets (encrypted)
- ✅ Only processed statistics are committed to repository
- ✅ Raw API data (`detailed_batches_all.json`) is excluded from commits

**Never commit your API credentials to the repository!**

## 🐛 Troubleshooting

### GitHub Actions Failing

1. Check that secrets are correctly set in repository settings
2. Verify API credentials are valid in Brewfather
3. Check workflow logs in Actions tab for specific errors

### GitHub Pages Not Updating

1. Check that GitHub Pages is enabled in repository settings
2. Wait 1-2 minutes after pushing changes
3. Hard refresh browser: `Cmd + Shift + R` (Mac) or `Ctrl + F5` (Windows)
4. Check Pages build status in Settings → Pages

### Local Script Errors

**"No credentials found"**
```bash
# Make sure environment variables are set
export $(cat .env | xargs)
./refresh_stats.sh
```

**"Permission denied"**
```bash
chmod +x refresh_stats.sh
./refresh_stats.sh
```

**"jq command not found"**
```bash
# macOS
brew install jq

# Linux
sudo apt install jq
```

## 📦 Dependencies

### For Local Development
- **Python 3** - Data analysis script
- **curl** - API requests (pre-installed on Mac/Linux)
- **jq** - JSON processing

### For GitHub Actions
All dependencies are automatically installed by the workflow.

## 🎯 Features

- ✅ Brewfather API integration with complete batch data
- ✅ Comprehensive statistics analysis
- ✅ Beautiful Nuclear-themed showcase with Varela Round font
- ✅ Interactive charts (Chart.js)
- ✅ Clickable batch history with detail modals
- ✅ Responsive design (mobile-friendly)
- ✅ GitHub Pages hosting
- ✅ Manual GitHub Actions workflow
- ✅ Environment variable support
- ✅ Cache-busting for instant updates
- ✅ Complete monthly timeline (no skipped months)
- ✅ Sorted hop chart with percentages

## 🔄 Automated Updates (Optional)

To enable automatic weekly updates, edit `.github/workflows/refresh-stats.yml` and uncomment the schedule line:

```yaml
schedule:
  - cron: '0 0 * * 0'  # Runs every Sunday at midnight UTC
```

## 📝 License

Personal project for Sklopivo brewing. Feel free to adapt for your own brewing analytics!

## 🍻 Cheers!

*"Good people drink good beer."* - Hunter S. Thompson

---

**Sklopivo** | Craft Beer Excellence | [View Stats](https://sklopivo.github.io/)
