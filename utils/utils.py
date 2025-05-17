from discord import Embed, Color

def create_embed(title: str = "", description: str = "", fields: list = None, color=Color.pink()) -> Embed:
    embed = Embed(
        title=title,
        description=description,
        color=color
    )
    
    if fields:
        for field_name, field_value in fields:
            embed.add_field(name=field_name, value=field_value, inline=True)
    
    embed.set_thumbnail(url="attachment://thumbnail.png")
    
    return embed
