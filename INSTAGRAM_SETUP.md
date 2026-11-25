# Conectar o Instagram ao site PRINCE' GUTT

A seção de Instagram já está implementada. Para começar a exibir as cinco publicações reais, falta autorizar o acesso de leitura da conta @princeguttreal.

## 1. Criar e configurar o app da Meta

1. Entre em https://developers.facebook.com/ e faça login com a conta Meta que administra o Instagram.
2. Crie um aplicativo no painel de desenvolvedores.
3. Adicione o produto Instagram e escolha a configuração Instagram API with Instagram Login (login do Instagram).
4. Configure o login para a conta profissional de Criador de Conteúdo.
5. Solicite somente a permissão instagram_business_basic. Ela é suficiente para ler o perfil e as mídias; não conceda permissões de publicação, mensagens ou comentários para este feed.
6. Autorize/conecte a conta @princeguttreal e gere um token de acesso de longa duração (long-lived access token).

Documentação oficial:
- https://developers.facebook.com/docs/instagram/platform/instagram-api-with-instagram-login/
- https://developers.facebook.com/docs/instagram/platform/instagram-api/changelog/

## 2. Guardar o token como Secret no GitHub

No repositório https://github.com/princeguttreal/princeguttreal:

1. Abra Settings → Secrets and variables → Actions.
2. Clique em New repository secret.
3. Nome: INSTAGRAM_ACCESS_TOKEN
4. Valor: cole o token de longa duração gerado pela Meta.
5. Salve.

Nunca coloque o token no HTML, JavaScript, em arquivos públicos do repositório ou em mensagens. O token deve ficar apenas no Secret privado do GitHub.

## 3. Testar a automação

1. Abra a aba Actions do repositório.
2. Selecione Atualizar feed do Instagram.
3. Clique em Run workflow.
4. Confira se a execução terminou com sucesso e se o arquivo instagram-feed.json foi atualizado.

Depois disso, o GitHub Actions executará a sincronização automaticamente uma vez por hora. O site exibirá as cinco publicações mais recentes e seus links para o Instagram.

## Manutenção do token

Tokens de longa duração do Instagram têm prazo de validade. Renove o token antes de expirar e substitua o valor do Secret INSTAGRAM_ACCESS_TOKEN no GitHub. Não compartilhe o token publicamente.

## Observações

- A integração é somente de leitura: não publica nem altera nada na conta.
- O feed é atualizado pelo GitHub Actions; pode haver atraso de até aproximadamente uma hora entre uma publicação e sua aparição no site.
- A Meta pode limitar a disponibilidade de URLs de mídia; a automação atualiza as URLs em cada sincronização.
- O workflow usa a versão v25.0 da API, configurável no arquivo .github/workflows/instagram-feed.yml.
