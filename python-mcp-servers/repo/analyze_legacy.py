#!/usr/bin/env python3
"""
English version - Command line tool for Legacy Code Analysis

Usage:
    python analyze_legacy_en.py /path/to/your/legacy/code
    python analyze_legacy_en.py --help
"""

import asyncio
import sys
import argparse
from pathlib import Path
from repo_analyzer import RepoAnalyzer

def print_banner():
    """Display tool banner"""
    print("🏛️  Auckland Library Legacy Code Analyzer")
    print("=" * 50)
    print("AI-Driven Automated Upgrade of Legacy Systems")
    print("=" * 50)
    print()

async def quick_analysis(repo_path: str):
    """Quick analysis of legacy code repository"""
    
    repo_path = Path(repo_path).resolve()
    if not repo_path.exists():
        print(f"❌ Error: Path does not exist '{repo_path}'")
        return False
    
    if not repo_path.is_dir():
        print(f"❌ Error: '{repo_path}' is not a directory")
        return False
    
    print(f"📁 Analyzing directory: {repo_path}")
    print()
    
    analyzer = RepoAnalyzer()
    
    try:
        # Quick structure analysis
        print("⏳ Analyzing repository structure...")
        structure = await analyzer.analyze_structure(str(repo_path))
        
        print("✅ Basic Information:")
        print(f"   📊 Total files: {structure['total_files']}")
        print(f"   📂 Total directories: {structure['total_directories']}")
        print(f"   💾 Total size: {structure['total_size'] / 1024 / 1024:.2f} MB")
        print(f"   🏗️  Architecture: {structure['architecture']['type']} ({structure['architecture']['confidence']}% confidence)")
        print()
        
        # Programming languages
        print("✅ Programming Languages:")
        for i, lang in enumerate(structure['languages'][:5], 1):
            bar = "█" * int(lang['percentage'] / 5)  # Simple progress bar
            print(f"   {i}. {lang['language']:<12} {lang['files']:>3} files {lang['percentage']:>5.1f}% {bar}")
        print()
        
        # Technology stack detection
        print("⏳ Detecting technology stack...")
        frameworks = await analyzer.detect_frameworks(str(repo_path))
        
        has_frameworks = False
        for category, items in frameworks.items():
            if items:
                has_frameworks = True
                category_names = {
                    'backend': '🖥️  Backend',
                    'frontend': '🎨 Frontend', 
                    'database': '🗄️  Database',
                    'testing': '🧪 Testing',
                    'build_tools': '🔨 Build Tools'
                }
                print(f"✅ {category_names.get(category, category)}:")
                for item in items:
                    version = f" v{item['version']}" if item.get('version') else ""
                    print(f"   • {item['name']}{version} ({item['confidence']}% confidence)")
                print()
        
        if not has_frameworks:
            print("ℹ️  No mainstream frameworks detected (might be custom or older tech stack)")
            print()
        
        # Entry points
        print("⏳ Identifying entry points...")
        entry_points = await analyzer.identify_entry_points(str(repo_path))
        
        if entry_points:
            print("✅ Application Entry Points:")
            for ep in entry_points[:5]:  # Show first 5
                icons = {'main': '🚀', 'server': '🖥️', 'cli': '⌨️', 'web': '🌐', 'test': '🧪'}
                icon = icons.get(ep['type'], '📄')
                print(f"   {icon} {ep['path']} ({ep['type']})")
            print()
        
        # Modernization suggestions
        print("🔮 Modernization Suggestions:")
        await show_modernization_tips(structure, frameworks)
        
        print("🎉 Analysis completed!")
        return True
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return False

async def show_modernization_tips(structure, frameworks):
    """Show modernization suggestions"""
    tips = []
    
    # JavaScript/Node.js project suggestions
    js_langs = [lang for lang in structure['languages'] if lang['language'] in ['JavaScript', 'TypeScript']]
    if js_langs:
        js_percentage = sum(lang['percentage'] for lang in js_langs)
        if js_percentage > 30:
            tips.append("💡 Consider adding TypeScript support for better code quality")
            
        if any(f['name'] == 'Express.js' for f in frameworks.get('backend', [])):
            tips.append("🔄 Recommend upgrading Express.js to latest version")
            
        if not frameworks.get('testing'):
            tips.append("🧪 Suggest adding Jest or other testing frameworks")
    
    # Database suggestions
    if any(f['name'] == 'MongoDB' for f in frameworks.get('database', [])):
        tips.append("🗄️  Consider upgrading MongoDB to version 5.0+")
    
    # Architecture suggestions
    if structure['architecture']['confidence'] < 60:
        tips.append("🏗️  Recommend refactoring for clearer architecture pattern")
    
    # General suggestions
    if structure['total_files'] > 50:
        tips.append("📦 Consider adding Docker containerization support")
        tips.append("🚀 Recommend setting up CI/CD automation pipeline")
    
    tips.append("🔐 Perform security audit and dependency updates")
    tips.append("📚 Improve documentation and code comments")
    
    for tip in tips[:6]:  # Show first 6 suggestions
        print(f"   {tip}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Analyze Legacy code repository structure, tech stack and modernization suggestions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage Examples:
  python analyze_legacy.py /path/to/legacy/project
  python analyze_legacy.py ~/old-website
  python analyze_legacy.py "C:\\Projects\\LegacyApp"
  
Supported Project Types:
  • Node.js (Express, Koa, etc.)
  • Python (Django, Flask, etc.)  
  • PHP (Laravel, CodeIgniter, etc.)
  • Mixed technology stack projects
        """
    )
    
    parser.add_argument(
        'path', 
        nargs='?',
        help='Path to the legacy code repository'
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version='Auckland Library Legacy Analyzer v1.0.0'
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    if not args.path:
        print("❓ Usage:")
        print("   python analyze_legacy.py /path/to/your/legacy/code")
        print()
        print("📝 Examples:")
        print("   python analyze_legacy.py ~/projects/old-library-system")
        print("   python analyze_legacy.py /var/www/legacy-website")
        print()
        print("💡 Tip: Use --help for detailed help")
        return 1
    
    # Run analysis
    success = asyncio.run(quick_analysis(args.path))
    return 0 if success else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Program error: {e}")
        sys.exit(1)