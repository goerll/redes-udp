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
