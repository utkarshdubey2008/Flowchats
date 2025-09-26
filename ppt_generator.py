import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import io
import textwrap
from design_elements import COLOR_SCHEMES, ICON_FUNCTIONS, create_gradient_background, add_decorative_elements, create_title_banner

def setup_high_quality_rendering():
    """Configure matplotlib for high-quality text rendering"""
    plt.rcParams.update({
        'text.antialiased': True,
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'DejaVu Sans', 'Liberation Sans'],
        'axes.unicode_minus': False,
        'svg.fonttype': 'none',
        'pdf.fonttype': 42,
        'ps.fonttype': 42,
        'figure.dpi': 150,
        'savefig.dpi': 600,
        'savefig.format': 'png',
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.1
    })

def create_title_slide(slide_data, theme='professional'):
    setup_high_quality_rendering()
    colors = COLOR_SCHEMES[theme]
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.set_dpi(150)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor(colors['bg'])
    create_gradient_background(ax, [colors['bg'], colors['light']], 'diagonal')
    title = slide_data.get('title', 'Presentation Title')
    ax.text(5, 7, title, fontsize=32, fontweight='bold', 
            color=colors['primary'], ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.5", facecolor=colors['light'], 
                     edgecolor=colors['accent'], linewidth=3))
    subtitle = slide_data.get('subtitle', '')
    if subtitle:
        ax.text(5, 5.5, subtitle, fontsize=20, 
                color=colors['text'], ha='center', va='center', style='italic')
    icon_name = slide_data.get('icon', 'lightbulb')
    if icon_name in ICON_FUNCTIONS:
        ICON_FUNCTIONS[icon_name](ax, 5, 3.5, size=1.5, color=colors['accent'])
    add_decorative_elements(ax, theme)
    ax.text(5, 1, 'Slide 1', fontsize=12, color=colors['text'], ha='center', va='center', alpha=0.7)
    plt.tight_layout()
    return fig

def create_definition_slide(slide_data, slide_num, theme='professional'):
    setup_high_quality_rendering()
    colors = COLOR_SCHEMES[theme]
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.set_dpi(150)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor(colors['bg'])
    create_gradient_background(ax, [colors['bg'], colors['light']], 'horizontal')
    title = slide_data.get('title', f'Definition - Slide {slide_num}')
    create_title_banner(ax, title, theme, 8.5)
    definition = slide_data.get('definition', '')
    if definition:
        wrapped_def = textwrap.fill(definition, width=70)
        def_bg = FancyBboxPatch((0.5, 5.5), 9, 1.5, 
                               boxstyle="round,pad=0.3", 
                               facecolor=colors['light'], 
                               edgecolor=colors['primary'], 
                               linewidth=2, alpha=0.9)
        ax.add_patch(def_bg)
        ax.text(5, 6.25, wrapped_def, fontsize=16, 
                color=colors['text'], ha='center', va='center', weight='normal')
    characteristics = slide_data.get('characteristics', [])
    if characteristics:
        ax.text(5, 4.8, 'Key Characteristics:', fontsize=18, fontweight='bold',
                color=colors['primary'], ha='center', va='center')
        for i, char in enumerate(characteristics[:4]):
            y_pos = 4.2 - (i * 0.4)
            bullet = FancyBboxPatch((1, y_pos-0.1), 0.2, 0.2, 
                                   boxstyle="round,pad=0.02", 
                                   facecolor=colors['accent'], 
                                   edgecolor='white', linewidth=1)
            ax.add_patch(bullet)
            ax.text(1.1, y_pos, '✓', fontsize=12, color='white', 
                    ha='center', va='center', fontweight='bold')
            wrapped_char = textwrap.fill(char, width=55)
            ax.text(1.5, y_pos, wrapped_char, fontsize=14, 
                    color=colors['text'], ha='left', va='center')
    icon_name = slide_data.get('icon', 'brain')
    if icon_name in ICON_FUNCTIONS:
        ICON_FUNCTIONS[icon_name](ax, 8.5, 3.5, size=1, color=colors['secondary'])
    add_decorative_elements(ax, theme)
    ax.text(5, 0.5, f'Slide {slide_num}', fontsize=12, color=colors['text'], ha='center', va='center', alpha=0.7)
    plt.tight_layout()
    return fig

def create_use_cases_slide(slide_data, slide_num, theme='professional'):
    setup_high_quality_rendering()
    colors = COLOR_SCHEMES[theme]
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.set_dpi(150)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor(colors['bg'])
    create_gradient_background(ax, [colors['bg'], colors['light']], 'vertical')
    title = slide_data.get('title', f'Use Cases - Slide {slide_num}')
    create_title_banner(ax, title, theme, 8.5)
    use_cases = slide_data.get('use_cases', [])
    y_start = 7.2
    for i, use_case in enumerate(use_cases[:4]):
        y_pos = y_start - (i * 1.2)
        number_circle = FancyBboxPatch((0.8, y_pos-0.15), 0.3, 0.3, 
                                      boxstyle="round,pad=0.05", 
                                      facecolor=colors['primary'], 
                                      edgecolor='white', linewidth=2)
        ax.add_patch(number_circle)
        ax.text(0.95, y_pos, str(i+1), fontsize=16, color='white', 
                ha='center', va='center', fontweight='bold')
        case_title = use_case.get('title', f'Use Case {i+1}')
        case_desc = use_case.get('description', '')
        ax.text(1.5, y_pos+0.15, case_title, fontsize=16, fontweight='bold',
                color=colors['primary'], ha='left', va='center')
        if case_desc:
            wrapped_desc = textwrap.fill(case_desc, width=50)
            ax.text(1.5, y_pos-0.15, wrapped_desc, fontsize=13, 
                    color=colors['text'], ha='left', va='center')
    icon_name = slide_data.get('icon', 'gear')
    if icon_name in ICON_FUNCTIONS and len(use_cases) <= 3:
        ICON_FUNCTIONS[icon_name](ax, 8.5, 4, size=1.2, color=colors['secondary'])
    add_decorative_elements(ax, theme)
    ax.text(5, 0.5, f'Slide {slide_num}', fontsize=12, color=colors['text'], ha='center', va='center', alpha=0.7)
    plt.tight_layout()
    return fig

def create_examples_slide(slide_data, slide_num, theme='professional'):
    setup_high_quality_rendering()
    colors = COLOR_SCHEMES[theme]
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.set_dpi(150)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor(colors['bg'])
    create_gradient_background(ax, [colors['light'], colors['bg']], 'diagonal')
    title = slide_data.get('title', f'Examples - Slide {slide_num}')
    create_title_banner(ax, title, theme, 8.5)
    examples = slide_data.get('examples', [])
    if len(examples) <= 2:
        for i, example in enumerate(examples):
            y_base = 6.5 - (i * 2.5)
            example_box = FancyBboxPatch((0.5, y_base-0.8), 9, 1.6, 
                                        boxstyle="round,pad=0.2", 
                                        facecolor='white', 
                                        edgecolor=colors['primary'], 
                                        linewidth=2, alpha=0.9)
            ax.add_patch(example_box)
            ex_title = example.get('title', f'Example {i+1}')
            ax.text(5, y_base+0.3, ex_title, fontsize=18, fontweight='bold',
                    color=colors['primary'], ha='center', va='center')
            ex_desc = example.get('description', '')
            if ex_desc:
                wrapped_desc = textwrap.fill(ex_desc, width=80)
                ax.text(5, y_base-0.2, wrapped_desc, fontsize=14, 
                        color=colors['text'], ha='center', va='center')
    else:
        for i, example in enumerate(examples[:4]):
            col = i % 2
            row = i // 2
            x_pos = 2.5 + (col * 5)
            y_pos = 6 - (row * 2.5)
            example_box = FancyBboxPatch((x_pos-2, y_pos-0.8), 4, 1.6, 
                                        boxstyle="round,pad=0.15", 
                                        facecolor='white', 
                                        edgecolor=colors['accent'], 
                                        linewidth=2, alpha=0.9)
            ax.add_patch(example_box)
            ex_title = example.get('title', f'Example {i+1}')
            ax.text(x_pos, y_pos+0.2, ex_title, fontsize=14, fontweight='bold',
                    color=colors['primary'], ha='center', va='center')
            ex_desc = example.get('description', '')[:80] + '...' if len(example.get('description', '')) > 80 else example.get('description', '')
            if ex_desc:
                wrapped_desc = textwrap.fill(ex_desc, width=30)
                ax.text(x_pos, y_pos-0.3, wrapped_desc, fontsize=11, 
                        color=colors['text'], ha='center', va='center')
    add_decorative_elements(ax, theme)
    ax.text(5, 0.5, f'Slide {slide_num}', fontsize=12, color=colors['text'], ha='center', va='center', alpha=0.7)
    plt.tight_layout()
    return fig

def create_benefits_challenges_slide(slide_data, slide_num, theme='professional'):
    setup_high_quality_rendering()
    colors = COLOR_SCHEMES[theme]
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.set_dpi(150)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor(colors['bg'])
    create_gradient_background(ax, [colors['bg'], colors['light']], 'horizontal')
    title = slide_data.get('title', f'Benefits & Challenges - Slide {slide_num}')
    create_title_banner(ax, title, theme, 8.5)
    benefits = slide_data.get('benefits', [])
    ax.text(2.5, 7.5, '✅ Benefits', fontsize=20, fontweight='bold',
            color='#27AE60', ha='center', va='center')
    for i, benefit in enumerate(benefits[:4]):
        y_pos = 6.8 - (i * 0.6)
        ax.text(0.5, y_pos, '•', fontsize=16, color='#27AE60', 
                ha='center', va='center', fontweight='bold')
        wrapped_benefit = textwrap.fill(benefit, width=35)
        ax.text(0.8, y_pos, wrapped_benefit, fontsize=13, 
                color=COLOR_SCHEMES[theme]['text'], ha='left', va='center')
    challenges = slide_data.get('challenges', [])
    ax.text(7.5, 7.5, '⚠️ Challenges', fontsize=20, fontweight='bold',
            color='#E74C3C', ha='center', va='center')
    for i, challenge in enumerate(challenges[:4]):
        y_pos = 6.8 - (i * 0.6)
        ax.text(5.5, y_pos, '•', fontsize=16, color='#E74C3C', 
                ha='center', va='center', fontweight='bold')
        wrapped_challenge = textwrap.fill(challenge, width=35)
        ax.text(5.8, y_pos, wrapped_challenge, fontsize=13, 
                color=COLOR_SCHEMES[theme]['text'], ha='left', va='center')
    ax.axvline(x=5, ymin=0.2, ymax=0.8, color=colors['primary'], linewidth=3, alpha=0.7)
    add_decorative_elements(ax, theme)
    ax.text(5, 0.5, f'Slide {slide_num}', fontsize=12, color=colors['text'], ha='center', va='center', alpha=0.7)
    plt.tight_layout()
    return fig

def create_detailed_content_slide(slide_data, slide_num, theme='professional'):
    setup_high_quality_rendering()
    colors = COLOR_SCHEMES[theme]
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.set_dpi(150)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor(colors['bg'])
    create_gradient_background(ax, [colors['bg'], colors['light']], 'horizontal')
    title = slide_data.get('title', f'Slide {slide_num}')
    create_title_banner(ax, title, theme, 8.5)
    description = slide_data.get('description', '')
    if description:
        wrapped_desc = textwrap.fill(description, width=80)
        ax.text(5, 7, wrapped_desc, fontsize=15, 
                color=colors['text'], ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', 
                         edgecolor=colors['light'], linewidth=1, alpha=0.9))
    points = slide_data.get('points', [])
    y_start = 5.8
    for i, point in enumerate(points[:5]):
        y_pos = y_start - (i * 0.7)
        bullet = FancyBboxPatch((0.8, y_pos-0.12), 0.25, 0.25, 
                               boxstyle="round,pad=0.03", 
                               facecolor=colors['accent'], 
                               edgecolor='white', linewidth=2)
        ax.add_patch(bullet)
        ax.text(0.925, y_pos, '●', fontsize=14, color='white', 
                ha='center', va='center', fontweight='bold')
        wrapped_text = textwrap.fill(point, width=55)
        ax.text(1.3, y_pos, wrapped_text, fontsize=14, 
                color=colors['text'], ha='left', va='center',
                bbox=dict(boxstyle="round,pad=0.2", facecolor='white', 
                         edgecolor=colors['light'], linewidth=1, alpha=0.8))
    icon_name = slide_data.get('icon', 'chart')
    if icon_name in ICON_FUNCTIONS and len(points) <= 3:
        ICON_FUNCTIONS[icon_name](ax, 8.5, 3.5, size=1.2, color=colors['secondary'])
    add_decorative_elements(ax, theme)
    ax.text(5, 0.5, f'Slide {slide_num}', fontsize=12, color=colors['text'], ha='center', va='center', alpha=0.7)
    plt.tight_layout()
    return fig

def create_conclusion_slide(slide_data, slide_num, theme='professional'):
    setup_high_quality_rendering()
    colors = COLOR_SCHEMES[theme]
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.set_dpi(150)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor(colors['bg'])
    create_gradient_background(ax, [colors['light'], colors['bg']], 'vertical')
    ax.text(5, 8, 'Conclusion', fontsize=28, fontweight='bold', 
            color='white', ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.4", facecolor=colors['primary'], 
                     edgecolor=colors['accent'], linewidth=2, alpha=0.9))
    conclusion = slide_data.get('conclusion', 'Thank you for your attention!')
    wrapped_conclusion = textwrap.fill(conclusion, width=60)
    ax.text(5, 6.2, wrapped_conclusion, fontsize=18, 
            color=colors['text'], ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='white', 
                     edgecolor=colors['primary'], linewidth=2, alpha=0.9))
    takeaways = slide_data.get('takeaways', [])
    if takeaways:
        ax.text(5, 4.8, '🎯 Key Takeaways:', fontsize=18, fontweight='bold',
                color=colors['primary'], ha='center', va='center')
        for i, takeaway in enumerate(takeaways[:4]):
            y_pos = 4.2 - (i * 0.4)
            ax.text(5, y_pos, f'• {takeaway}', fontsize=15, 
                    color=colors['text'], ha='center', va='center',
                    bbox=dict(boxstyle="round,pad=0.1", facecolor=colors['light'], 
                             alpha=0.7))
    ICON_FUNCTIONS['lightbulb'](ax, 5, 1.8, size=1, color=colors['accent'])
    ax.text(5, 1, 'Thank You!', fontsize=20, fontweight='bold',
            color=colors['primary'], ha='center', va='center')
    add_decorative_elements(ax, theme)
    ax.text(5, 0.3, f'Slide {slide_num}', fontsize=12, color=colors['text'], ha='center', va='center', alpha=0.7)
    plt.tight_layout()
    return fig

def determine_theme_from_topic(topic):
    topic_lower = topic.lower()
    if any(word in topic_lower for word in ['business', 'professional', 'corporate', 'finance', 'management']):
        return 'professional'
    elif any(word in topic_lower for word in ['tech', 'technology', 'ai', 'computer', 'digital', 'software']):
        return 'tech'
    elif any(word in topic_lower for word in ['creative', 'design', 'art', 'marketing', 'brand']):
        return 'creative'
    else:
        return 'modern'

def suggest_icons_for_topic(topic):
    topic_lower = topic.lower()
    icon_mapping = {
        'computer': ['computer', 'tech', 'software', 'digital', 'programming'],
        'brain': ['ai', 'intelligence', 'learning', 'psychology', 'education'],
        'rocket': ['startup', 'growth', 'innovation', 'space', 'future'],
        'chart': ['business', 'data', 'analytics', 'sales', 'finance'],
        'gear': ['process', 'system', 'engineering', 'manufacturing'],
        'lightbulb': ['idea', 'creative', 'innovation', 'solution']
    }
    for icon, keywords in icon_mapping.items():
        if any(keyword in topic_lower for keyword in keywords):
            return icon
    return 'lightbulb'

def create_slide_images(presentation_data, theme=None):
    slides = []
    if not theme:
        theme = determine_theme_from_topic(presentation_data.get('topic', ''))
    title_data = {
        'title': presentation_data.get('title', 'Presentation'),
        'subtitle': presentation_data.get('subtitle', ''),
        'icon': suggest_icons_for_topic(presentation_data.get('topic', ''))
    }
    title_fig = create_title_slide(title_data, theme)
    slides.append(title_fig)
    content_slides = presentation_data.get('slides', [])
    for i, slide_data in enumerate(content_slides, 2):
        slide_type = slide_data.get('type', 'content')
        if slide_type == 'definition':
            fig = create_definition_slide(slide_data, i, theme)
        elif slide_type == 'use_cases':
            fig = create_use_cases_slide(slide_data, i, theme)
        elif slide_type == 'examples':
            fig = create_examples_slide(slide_data, i, theme)
        elif slide_type == 'benefits_challenges':
            fig = create_benefits_challenges_slide(slide_data, i, theme)
        elif slide_type == 'conclusion':
            fig = create_conclusion_slide(slide_data, i, theme)
        else:
            slide_data['icon'] = suggest_icons_for_topic(slide_data.get('title', ''))
            fig = create_detailed_content_slide(slide_data, i, theme)
        slides.append(fig)
    return slides

def convert_slides_to_images(slides):
    image_buffers = []
    for slide in slides:
        buf = io.BytesIO()
        slide.savefig(buf, format='png', dpi=600, bbox_inches='tight', 
                     facecolor='white', edgecolor='none', 
                     pil_kwargs={'optimize': True, 'quality': 95})
        buf.seek(0)
        image_buffers.append(buf)
        plt.close(slide)
    return image_buffers
