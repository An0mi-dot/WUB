    import discord
    import random
    import re
    import os
    from discord.ext import commands

    # ==========================================================
    # CÓDIGO DO KEEP-ALIVE FOI REMOVIDO!
    # Não precisamos mais do Flask nem do Threading.
    # ==========================================================

    # --- CONFIGURAÇÃO INICIAL ---

    # 1. Definição das "Intents" (Intenções)
    intents = discord.Intents.default()
    intents.message_content = True

    # 2. Criação do objeto do Bot
    bot = commands.Bot(command_prefix='!', intents=intents)


    # --- EVENTOS DO BOT ---

    @bot.event
    async def on_ready():
        """Este evento é chamado quando o bot se conecta com sucesso ao Discord."""
        print(f'Bot conectado como {bot.user}')
        print('Wuitalur Bot está pronto para rolar!')
        print('------')


    # --- COMANDOS BÁSICOS ---

    @bot.command(name='s', help='Soma dois números. Uso: !s <num1> <num2>')
    async def soma(ctx, num1: int, num2: int):
        """Calcula a soma de dois números."""
        resultado = num1 + num2
        await ctx.send(f'➕ A soma de {num1} e {num2} é {resultado}!')

    @bot.command(name='m', help='Multiplica dois números. Uso: !m <num1> <num2>')
    async def multiplicacao(ctx, num1: int, num2: int):
        """Calcula a multiplicação de dois números."""
        resultado = num1 * num2
        await ctx.send(f'✖️ A multiplicação de {num1} e {num2} é {resultado}!')

    @bot.command(name='p', help='Calcula a porcentagem. Uso: !p <parte> <total>')
    async def porcentagem(ctx, parte: float, total: float):
        """Calcula a porcentagem de um número em relação a outro."""
        if total == 0:
            await ctx.send('🚫 Não é possível dividir por zero!')
            return

        resultado_porcentagem = (parte / total) * 100
        await ctx.send(f'📊 {parte} é {resultado_porcentagem:.2f}% de {total}')


    # --- COMANDO DE ROLAGEM DE DADOS (A FUNÇÃO ESPECIAL *) ---

    @bot.command(name='r', help='Rola dados em formato complexo. Ex: !r 2d6+3 ou !r 1d20 + 2d4 - 2')
    async def rolar(ctx, *, expressao: str):
        """
        Rola dados seguindo uma expressão complexa.
        Exemplos: 2d6, 1d20+5, 2d8 - 1d4 + 2
        """
        padrao_dado = re.compile(r'(\d*)d(\d+)')
        expressao_para_eval = expressao.lower()
        detalhes_rolagens = []

        for rolagem_encontrada in padrao_dado.finditer(expressao):
            texto_completo_dado = rolagem_encontrada.group(0)
            num_dados_str = rolagem_encontrada.group(1)
            tipo_dado = int(rolagem_encontrada.group(2))
            num_dados = 1 if num_dados_str == '' else int(num_dados_str)

            if num_dados > 100 or tipo_dado > 1000:
                await ctx.send(f"🚫 Calma aí, mestre! Limite de 100 dados e dado de 1000 lados. Você tentou `{texto_completo_dado}`.")
                return

            rolagens_individuais = [random.randint(1, tipo_dado) for _ in range(num_dados)]
            soma_da_rolagem = sum(rolagens_individuais)
            detalhes_rolagens.append(f"{texto_completo_dado} ({rolagens_individuais})")
            expressao_para_eval = expressao_para_eval.replace(texto_completo_dado, str(soma_da_rolagem), 1)

        try:
            caracteres_permitidos = "0123456789+-*/(). "
            if not all(c in caracteres_permitidos for c in expressao_para_eval):
                raise ValueError("Expressão contém caracteres inválidos.")
            resultado_final = eval(expressao_para_eval)

        except (SyntaxError, ZeroDivisionError, ValueError) as e:
            await ctx.send(f"Houve um erro ao tentar calcular a sua expressão: `{expressao}`. Verifique a sintaxe. ({e})")
            return

        resposta_final = f"🎲 **{ctx.author.display_name}** rolou: `{expressao}`\n"
        if detalhes_rolagens:
            resposta_final += f"🔹 **Detalhes:** {', '.join(detalhes_rolagens)}\n"
        resposta_final += f" soma dos dados: `{expressao_para_eval}` \n"
        resposta_final += f"✨ **Resultado Final: {resultado_final}**"

        if len(resposta_final) > 2000:
            await ctx.send("O resultado da sua rolagem é muito longo para ser exibido!")
        else:
            await ctx.send(resposta_final)


    # --- TRATAMENTO DE ERROS GENÉRICO ---

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("🚫 Faltam argumentos! Use `!help <comando>` para ver como usar.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("🚫 Argumento inválido! Verifique se você digitou números onde deveria.")
        elif isinstance(error, commands.CommandNotFound):
            pass
        else:
            print(f"Erro inesperado: {error}")
            await ctx.send("Ocorreu um erro inesperado ao executar o comando.")


    # --- INICIALIZAÇÃO DO BOT ---

    TOKEN = os.getenv("DISCORD_TOKEN")
    if TOKEN is None:
        print("Erro: O token do Discord não foi encontrado nas variáveis de ambiente.")
    else:
        # A única coisa que precisamos fazer é iniciar o bot.
        # A chamada `keep_alive()` foi removida.
        bot.run(TOKEN)
