# redes-udp
Atividade UDP para a matéria de Redes II

## Atividade 1

![Screenshot From 2025-04-26 15-19-41](https://github.com/user-attachments/assets/ad9af90e-d863-4dc5-9005-f4eeaff5ebf4)

![Screenshot From 2025-04-26 15-19-51](https://github.com/user-attachments/assets/0b5807c8-8f20-4329-8716-15638a3ddd41)

![Screenshot From 2025-04-26 15-20-03](https://github.com/user-attachments/assets/2f22c4ee-dcae-4aeb-a9ba-bc16ad4cf7e1)

![Screenshot From 2025-04-26 15-20-24](https://github.com/user-attachments/assets/c1c54870-5a91-4a49-b97c-2b33fd4de5ff)

## Atividade 2
Arquivo pequeno (10 fragmentos):

![image](https://github.com/user-attachments/assets/e0512e82-1a09-44ec-8253-1050021014c5)

Arquivo médio (1048 fragmentos):

![image](https://github.com/user-attachments/assets/82d721aa-bdaa-4d31-8091-f6e3dd848d0f)

Arquivo grande (10485 fragmentos):

![image](https://github.com/user-attachments/assets/d10b4c40-cd3c-480f-928c-0bb8c8ba704d)

Servidor:

![image](https://github.com/user-attachments/assets/892a70f6-2af7-475c-b03e-27243f6dc652)

Visão do Wireshark:

![image](https://github.com/user-attachments/assets/a707498b-8831-4194-a96a-3e591bc8ad07)

A análise do Wireshark mostra o padrão de envio dos fragmentos do arquivo. Cada fragmento de dados (payload maior, ex: 1046 bytes) é seguido por um pacote de confirmação (ACK) enviado pelo servidor (payload menor, ex: 49-53 bytes).

Os ACKs são os pacotes com tamanho entre 49 e 53, é possível observar isso abrindo o pacote e vendo que o conteúdo dele é "ACK: {numero_do_fragmento}".

![image](https://github.com/user-attachments/assets/9246bb50-008b-4284-812e-3ac5a77161ea)

## Atividade 3
Por falta de acesso a outro computador, tive que rodar os testes com ambos servidor e cliente rodando em meu notebook.

![image](https://github.com/user-attachments/assets/d728b17d-dd8a-494a-bd6d-e371c20b5391)

Rede com perdas:

![image](https://github.com/user-attachments/assets/101dc1ba-a19e-402a-9de3-7d1f57dfe930)

![image](https://github.com/user-attachments/assets/efe93674-4a35-4e3f-ae8a-3e7e11a1a83e)

Rede com alta latência:

![image](https://github.com/user-attachments/assets/fd959794-8e05-431a-bb45-3290dc7118f1)

![image](https://github.com/user-attachments/assets/13fcf4c7-9648-4926-92a5-b5fb41048053)

Como ambos foram rodados na mesma máquina, podemos ver que os cenários de rede não impactaram a transferência.

Mesmo em rede local, o TCP apresentou uma taxa de transferência significativamente maior (ex: ~173 MB/s ) em comparação com a implementação UDP (ex: ~3.8 MB/s ). Isso pode ser atribuído à natureza orientada à conexão e ao controle de fluxo otimizado do TCP, enquanto a implementação UDP, com envio fragmento por fragmento e espera por ACK individual, introduz maior latência entre pacotes.

O overhead calculado para a transferência UDP foi de 0.20%, enquanto para o TCP foi de 0.00%. O overhead no UDP se deve à adição de informações de controle (como número de sequência) em cada fragmento para implementar a confiabilidade. O TCP, embora tenha cabeçalhos maiores, gerencia a confiabilidade e o fluxo de forma mais eficiente em nível de sistema operacional, resultando em menor overhead percentual percebido na camada de aplicação para transferências de dados em massa.

## Perguntas de Reflexão
### Quais foram os principais desafios ao implementar aplicações com UDP?
O maior desafio foi a falta de confiabilidade nativa do UDP. Diferente do TCP, é necessário um cuidado manual com a entrega ordenada e completa dos dados, levando em conta possíveis perdas ou desordem dos pacotes.

### Como você contornou a falta de garantias de entrega do UDP?
- Números de sequência: Para ordenar os fragmentos do arquivo.
- Confirmações (ACKs): O servidor confirma o recebimento de cada fragmento.
- Timeout e Retransmissão: O cliente reenviará um fragmento se não receber o ACK dentro de um tempo limite.
- Tratamento de ordem: O servidor verifica a sequência e solicita reenvio se necessário.

### Em quais situações você recomendaria o uso de UDP ao invés de TCP?
O UDP é mais adequado quando a velocidade e a baixa latência são prioritárias acima até mesmo de falhas eventuais na transmissão, e a perda ocasional de pacotes é aceitável ou pode ser tratada pela aplicação. Bons exemplos são streaming de vídeo/áudio ao vivo, jogos online e chamadas VoIP, onde atrasos são mais prejudiciais que pequenas perdas.

### Como o comportamento do UDP poderia impactar aplicações de tempo real?
Aplicações de tempo real são sensíveis a atrasos e perdas. Com UDP a perda de pacotes pode causar glitches visuais ou sonoros no caso de transmissões de mídia ou perda de informação (por exemplo em jogos). A variação no atraso prejudica a reprodução contínua de mídia e a entrega fora de ordem dos pacotes torna necessário um buffer onde os pacotes podem ser armazenados enquanto esperam por pacotes anteriores que demoraram mais pra chegar ou precisram de retransmissão, aumentando a latência e provavelmente prejudicando a experiência final do usuário.
