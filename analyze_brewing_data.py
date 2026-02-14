#!/usr/bin/env python3
"""
Comprehensive Brewfather Batch Analysis Script
Analyzes all brewing batches and generates statistics
"""

import json
from datetime import datetime
from collections import defaultdict, Counter
from typing import Dict, List, Any

def load_batch_data(filename: str) -> List[Dict[str, Any]]:
    """Load batch data from JSON file"""
    with open(filename, 'r') as f:
        return json.load(f)

def analyze_batches(batches: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Comprehensive analysis of brewing batches"""

    stats = {
        'total_batches': len(batches),
        'styles': Counter(),
        'grains': Counter(),
        'hops': Counter(),
        'yeasts': Counter(),
        'abv_distribution': [],
        'ibu_distribution': [],
        'og_distribution': [],
        'fg_distribution': [],
        'batch_timeline': [],
        'brewers': Counter(),
        'batch_sizes': [],
        'boil_times': [],
        'fermentation_temps': [],
        'grain_totals': defaultdict(float),
        'hop_totals': defaultdict(float),
        'yearly_brews': Counter(),
        'monthly_brews': Counter(),
        'color_srm': [],
        'efficiency': []
    }

    for batch in batches:
        try:
            recipe = batch.get('recipe', {})

            # Basic info
            batch_name = batch.get('name', 'Unknown')
            brewer = batch.get('brewer', 'Unknown')
            brew_date = batch.get('brewDate')

            stats['brewers'][brewer] += 1

            # Timeline analysis
            if brew_date:
                dt = datetime.fromtimestamp(brew_date / 1000)
                stats['batch_timeline'].append({
                    'date': dt.strftime('%Y-%m-%d'),
                    'name': batch_name,
                    'style': recipe.get('style', {}).get('name', 'Unknown'),
                    'batch_id': batch.get('_id', ''),
                    'brew_number': batch.get('batchNo', 0),
                    'brewer': batch.get('brewer', 'Unknown'),
                    'status': batch.get('status', 'Unknown'),
                    'abv': recipe.get('abv', 0),
                    'og': recipe.get('og', 0),
                    'fg': recipe.get('fg', 0),
                    'ibu': recipe.get('ibu', 0)
                })
                stats['yearly_brews'][dt.year] += 1
                stats['monthly_brews'][dt.strftime('%Y-%m')] += 1

            # Style
            style = recipe.get('style', {})
            if style:
                style_name = style.get('name', 'Unknown')
                stats['styles'][style_name] += 1

            # ABV, IBU, OG, FG
            if 'abv' in batch:
                stats['abv_distribution'].append(batch['abv'])
            if 'ibu' in recipe:
                stats['ibu_distribution'].append(recipe['ibu'])
            if 'og' in batch:
                stats['og_distribution'].append(batch['og'])
            if 'fg' in batch:
                stats['fg_distribution'].append(batch['fg'])
            if 'estimatedColor' in recipe:
                stats['color_srm'].append(recipe['estimatedColor'])
            if 'efficiency' in batch:
                stats['efficiency'].append(batch['efficiency'])

            # Batch size
            if 'batchSize' in recipe:
                stats['batch_sizes'].append(recipe['batchSize'])

            # Boil time
            equipment = recipe.get('equipment', {})
            if 'boilTime' in equipment:
                stats['boil_times'].append(equipment['boilTime'])

            # Grains/Fermentables
            fermentables = recipe.get('fermentables', [])
            for ferm in fermentables:
                name = ferm.get('name', 'Unknown')
                amount = ferm.get('amount', 0)
                grain_type = ferm.get('type', 'Unknown')

                stats['grains'][name] += 1
                stats['grain_totals'][name] += amount

            # Hops
            hops = recipe.get('hops', [])
            for hop in hops:
                name = hop.get('name', 'Unknown')
                amount = hop.get('amount', 0)

                stats['hops'][name] += 1
                stats['hop_totals'][name] += amount

            # Yeasts
            yeasts = recipe.get('yeasts', [])
            for yeast in yeasts:
                name = yeast.get('name', 'Unknown')
                lab = yeast.get('laboratory', '')
                product_id = yeast.get('productId', '')
                yeast_full = f"{lab} {product_id} - {name}" if lab else name

                stats['yeasts'][yeast_full] += 1

            # Fermentation temperature
            fermentation = recipe.get('fermentation', {})
            if 'steps' in fermentation and len(fermentation['steps']) > 0:
                primary_temp = fermentation['steps'][0].get('stepTemp')
                if primary_temp:
                    stats['fermentation_temps'].append(primary_temp)

        except Exception as e:
            print(f"Error processing batch {batch.get('name', 'Unknown')}: {e}")
            continue

    # Sort timeline
    stats['batch_timeline'].sort(key=lambda x: x['date'])

    # Calculate averages
    if stats['abv_distribution']:
        stats['avg_abv'] = sum(stats['abv_distribution']) / len(stats['abv_distribution'])
        stats['min_abv'] = min(stats['abv_distribution'])
        stats['max_abv'] = max(stats['abv_distribution'])

    if stats['ibu_distribution']:
        stats['avg_ibu'] = sum(stats['ibu_distribution']) / len(stats['ibu_distribution'])
        stats['min_ibu'] = min(stats['ibu_distribution'])
        stats['max_ibu'] = max(stats['ibu_distribution'])

    if stats['batch_sizes']:
        stats['avg_batch_size'] = sum(stats['batch_sizes']) / len(stats['batch_sizes'])

    if stats['efficiency']:
        stats['avg_efficiency'] = sum(stats['efficiency']) / len(stats['efficiency'])

    if stats['color_srm']:
        stats['avg_color'] = sum(stats['color_srm']) / len(stats['color_srm'])

    # Calculate total volume brewed
    if stats['batch_sizes']:
        stats['total_volume'] = sum(stats['batch_sizes'])
    else:
        stats['total_volume'] = 0

    # Calculate years brewing (from first to last brew)
    if len(stats['batch_timeline']) >= 2:
        first_brew = datetime.strptime(stats['batch_timeline'][0]['date'], '%Y-%m-%d')
        last_brew = datetime.strptime(stats['batch_timeline'][-1]['date'], '%Y-%m-%d')
        stats['years_brewing'] = (last_brew - first_brew).days / 365.25
    else:
        stats['years_brewing'] = 0

    return stats

def generate_markdown_report(stats: Dict[str, Any]) -> str:
    """Generate comprehensive markdown report"""

    md = "# 🍺 Sklopivo Brewing Statistics\n\n"
    md += f"## Overview\n\n"
    md += f"**Total Batches Brewed:** {stats['total_batches']}\n\n"

    # Brewers
    md += "### 👨‍🍳 Brewers\n\n"
    for brewer, count in stats['brewers'].most_common():
        md += f"- **{brewer}**: {count} batches\n"
    md += "\n"

    # Yearly statistics
    if stats['yearly_brews']:
        md += "### 📅 Brewing Timeline\n\n"
        md += "#### Brews by Year\n\n"
        for year, count in sorted(stats['yearly_brews'].items()):
            md += f"- **{year}**: {count} batches\n"
        md += "\n"

    # Beer statistics
    md += "## 🍻 Beer Statistics\n\n"

    if 'avg_abv' in stats:
        md += f"### Alcohol Content (ABV)\n\n"
        md += f"- **Average ABV**: {stats['avg_abv']:.2f}%\n"
        md += f"- **Range**: {stats['min_abv']:.2f}% - {stats['max_abv']:.2f}%\n\n"

    if 'avg_ibu' in stats:
        md += f"### Bitterness (IBU)\n\n"
        md += f"- **Average IBU**: {stats['avg_ibu']:.1f}\n"
        md += f"- **Range**: {stats['min_ibu']:.1f} - {stats['max_ibu']:.1f}\n\n"

    if 'avg_batch_size' in stats:
        md += f"### Batch Size\n\n"
        md += f"- **Average**: {stats['avg_batch_size']:.1f} liters\n\n"

    if 'avg_efficiency' in stats:
        md += f"### Brewing Efficiency\n\n"
        md += f"- **Average Efficiency**: {stats['avg_efficiency']:.1f}%\n\n"

    if 'avg_color' in stats:
        md += f"### Beer Color\n\n"
        md += f"- **Average SRM**: {stats['avg_color']:.1f}\n\n"

    # Styles
    md += "## 🎨 Beer Styles\n\n"
    for style, count in stats['styles'].most_common():
        md += f"- **{style}**: {count} batches\n"
    md += "\n"

    # Grains
    if stats['grains']:
        md += "## 🌾 Grains & Fermentables\n\n"
        md += "### Most Used Grains\n\n"
        for grain, count in stats['grains'].most_common(15):
            total_kg = stats['grain_totals'][grain]
            md += f"- **{grain}**: {count} times ({total_kg:.2f} kg total)\n"
        md += "\n"

    # Hops
    if stats['hops']:
        md += "## 🌿 Hops\n\n"
        md += "### Most Used Hops\n\n"
        for hop, count in stats['hops'].most_common(15):
            total_g = stats['hop_totals'][hop] * 1000  # Convert to grams
            md += f"- **{hop}**: {count} times ({total_g:.1f} g total)\n"
        md += "\n"

    # Yeasts
    if stats['yeasts']:
        md += "## 🧫 Yeasts\n\n"
        for yeast, count in stats['yeasts'].most_common():
            md += f"- **{yeast}**: {count} times\n"
        md += "\n"

    # Batch timeline
    if stats['batch_timeline']:
        md += "## 📆 Brewing History\n\n"
        for batch_info in stats['batch_timeline']:
            md += f"- **{batch_info['date']}**: {batch_info['name']} ({batch_info['style']})\n"
        md += "\n"

    return md

def main():
    """Main execution"""
    print("Loading batch data...")
    batches = load_batch_data('detailed_batches_all.json')

    print(f"Analyzing {len(batches)} batches...")
    stats = analyze_batches(batches)

    # Save stats as JSON for HTML generation
    # Convert Counter and defaultdict to regular dict for JSON serialization
    # Also include detailed batch data indexed by batch ID
    detailed_batches_dict = {batch['_id']: batch for batch in batches}

    stats_json = {
        'total_batches': stats['total_batches'],
        'styles': dict(stats['styles']),
        'grains': dict(stats['grains']),
        'hops': dict(stats['hops']),
        'yeasts': dict(stats['yeasts']),
        'brewers': dict(stats['brewers']),
        'yearly_brews': dict(stats['yearly_brews']),
        'monthly_brews': dict(stats['monthly_brews']),
        'batch_timeline': stats['batch_timeline'],
        'grain_totals': dict(stats['grain_totals']),
        'hop_totals': dict(stats['hop_totals']),
        'avg_abv': stats.get('avg_abv', 0),
        'min_abv': stats.get('min_abv', 0),
        'max_abv': stats.get('max_abv', 0),
        'avg_ibu': stats.get('avg_ibu', 0),
        'min_ibu': stats.get('min_ibu', 0),
        'max_ibu': stats.get('max_ibu', 0),
        'avg_batch_size': stats.get('avg_batch_size', 0),
        'avg_efficiency': stats.get('avg_efficiency', 0),
        'avg_color': stats.get('avg_color', 0),
        'total_volume': stats.get('total_volume', 0),
        'years_brewing': stats.get('years_brewing', 0),
        'detailed_batches': detailed_batches_dict
    }

    with open('brewing_statistics.json', 'w') as f:
        json.dump(stats_json, f, indent=2)

    print("✅ Analysis complete!")
    print(f"   - JSON data: brewing_statistics.json")

    # Print summary
    print(f"\n📊 Summary:")
    print(f"   Total batches: {stats['total_batches']}")
    print(f"   Unique styles: {len(stats['styles'])}")
    print(f"   Different grains used: {len(stats['grains'])}")
    print(f"   Different hops used: {len(stats['hops'])}")
    if 'avg_abv' in stats:
        print(f"   Average ABV: {stats['avg_abv']:.2f}%")

if __name__ == "__main__":
    main()
