import discord
from datetime import datetime

def create_embed():
    # Create the embed object
    embed = discord.Embed(
        title="Auto Post Testing", #title headers
        description="This is a test auto delete, command", #description
        color=0x008080,  #color
        timestamp=datetime.utcnow() #Posted Time
    )

    # Add fields to the embed
    embed.add_field(name="Testing", value="Description.", inline=False)
    embed.add_field(name="Title", value="Description", inline=False)
    embed.add_field(name="Testing Auto Post", value="Testing Auto Post, Using Command, Auto Delete", inline=False)
    embed.add_field(name="This is a test", value="This is a testttttt", inline=False)

    embed.set_thumbnail(url="https://example.com/image.jpg")
    embed.set_image(url="https://example.com/image.jpg")
    embed.set_footer(text="Footer Text", icon_url="https://example.com/image.jpg")

    return embed
