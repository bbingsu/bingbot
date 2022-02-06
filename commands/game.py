import discord
from discord.ext.commands import Context
import discord.ext.commands as commands

import random

INIT, WIN, LOSE = 0, 1, 2
even_odd_msg = ['선택 한 뒤에 어떤 수가 나왔나 알려 준다냥.', 
                    '정답이다냥! 계속해서 도전해 보라냥!', 
                    '틀렸다냥... 계속 도전해 보라냥!']

@commands.command()
async def 홀짝(ctx: Context):
    """홀짝 게임을 시작합니다."""
    dice = random.randint(1, 6)
    winning, max_winning = 0, 0
    def _make_embed(description: str, before_dice: str):
        embed = discord.Embed(title='홀, 짝 중에 하나를 선택해 보라냥.',
                                description=description)
        embed.add_field(name='> 주사위의 눈', value=before_dice)
        embed.add_field(name='> 홀수', value='🌞')
        embed.add_field(name='> 짝수', value='🌝')
        embed.add_field(name='> 연승횟수', value=str(winning))
        return embed

    embed = _make_embed(even_odd_msg[INIT], '???')
    msg: discord.Message = await ctx.channel.send(embed=embed)
    await msg.add_reaction('🌞')
    await msg.add_reaction('🌝')

    def _check(reaction: discord.reaction.Reaction, user: discord.member.Member):
        return str(reaction) in ['🌞', '🌝'] and \
                user == ctx.author and \
                reaction.message.id == msg.id
    try:
        while True:
            reaction, user = await ctx.bot.wait_for('reaction_add', check=_check, timeout=10)
            await msg.clear_reactions()

            # win
            if  (str(reaction) == '🌞' and dice % 2 == 1) or \
                (str(reaction) == '🌝' and dice % 2 == 0):
                winning += 1
                embed = _make_embed(even_odd_msg[WIN], str(dice))
            # lose
            else:
                winning = 0
                embed = _make_embed(even_odd_msg[LOSE], str(dice))

            await msg.edit(embed=embed)
            await msg.add_reaction('🌞')
            await msg.add_reaction('🌝')
            dice = random.randint(1, 6)
            max_winning = max(max_winning, winning)
    except Exception as e:
        await msg.clear_reactions()
    # print('[알림][홀짝 게임 종료]')
    # print('종료 유저 이름:', ctx.author)
    # print('최고 연승 횟수:', max_winning)
    await ctx.channel.send(ctx.author.name + ' 집사가 최고 ' + str(max_winning) + '연승을 달성했다냥!!')

gameCmd = [ 홀짝 ]