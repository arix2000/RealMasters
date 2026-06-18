from backend.models import CharacterSheet


def render(char: CharacterSheet) -> str:
    stats = char.stats
    stats_dict = {
        "Siła": stats.strength,
        "Zręczność": stats.dexterity,
        "Kondycja": stats.constitution,
        "Inteligencja": stats.intelligence,
        "Mądrość": stats.wisdom,
        "Charyzma": stats.charisma
    }

    stats_html = "".join(
        [f'<div class="cs-row"><span class="cs-label">{name}</span><span class="cs-value">{val}</span></div>' for
         name, val in stats_dict.items()])

    eq_html = "".join([f'<div class="cs-row-eq"><span class="cs-label">{item}</span></div>' for item in char.equipment])

    traits_html = ""
    if char.special_traits:
        for trait in char.special_traits:
            parts = trait.split(":", 1)
            if len(parts) > 1:
                traits_html += f'<div class="cs-trait-card"><h4>{parts[0]}</h4><p>{parts[1]}</p></div>'
            else:
                traits_html += f'<div class="cs-trait-card"><p>{trait}</p></div>'

    story = char.background_story.replace('\n', '<br>')

    return f""" <style>
  .cs-container {{
    background-color: #1a1919;
    border-radius: 16px;
    padding: 24px;
    display: grid;
    grid-template-columns: 260px 1fr;
    gap: 32px;
    color: #d1d1d1;
    font-family: sans-serif;
    margin-top: 8px;
    margin-bottom: 8px;
  }}

  .cs-sidebar {{
    display: flex;
    flex-direction: column;
    gap: 24px;
  }}

  .cs-section-title {{
    font-size: 20px;
    font-weight: normal;
    color: #E2E2E2;
    text-align: center;
    margin-bottom: 12px;
  }}

  .cs-row {{
    background-color: #1E1C1C;
    border: 1px solid #710246;
    border-radius: 24px;
    padding: 8px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }}
  
  .cs-row-eq {{
    background-color: #1E1C1C;
    border: 1px solid #5F0271;
    border-radius: 24px;
    padding: 8px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }}

  .cs-label {{
    color: #a3a3a3;
    font-size: 14px;
  }}

  .cs-value {{
    color: #FF82CE;
    font-weight: bold;
    font-size: 16px;
  }}

  .cs-header h1 {{
    margin: 0 0 4px 0;
    color: #E2E2E2;
    font-size: 32px;
  }}

  .cs-header h3 {{
    margin: 0 0 24px 0;
    color: #7a7a7a;
    font-weight: normal;
    font-size: 18px;
  }}

  .cs-story {{
    line-height: 1.6;
    font-size: 14px;
    color: #b5b5b5;
    margin-bottom: 32px;
  }}

  .cs-traits-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
  }}

  .cs-trait-card {{
    background-color: #242222;
    border-radius: 12px;
    padding: 16px;
  }}

  .cs-trait-card h4 {{
    margin: 0 0 8px 0;
    color: #E2E2E2;
    font-size: 15px;
  }}

  .cs-trait-card p {{
    margin: 0;
    font-size: 13px;
    color: #a3a3a3;
    line-height: 1.5;
  }}

  @media (max-width: 800px) {{
    .cs-container {{
      grid-template-columns: 1fr;
    }}
  }}
</style>

<div class="cs-container">
  <div class="cs-sidebar">
    <div>
      <div class="cs-section-title">Statystyki:</div>
      {stats_html}
    </div>
    <div>
      <div class="cs-section-title">Ekwipunek:</div>
      {eq_html}
    </div>
  </div>
  <div>
    <div class="cs-header">
      <h1>{char.name}</h1>
      <h3>{char.race} - {char.role_or_class}</h3>
    </div>
    <div class="cs-story">
      {story}
    </div>
    <h2 style="color: #E2E2E2; font-size: 20px; margin-bottom: 16px;">Umiejętności specjalne:</h2>
    <div class="cs-traits-grid">
      {traits_html}
    </div>
  </div>
</div>
    """
