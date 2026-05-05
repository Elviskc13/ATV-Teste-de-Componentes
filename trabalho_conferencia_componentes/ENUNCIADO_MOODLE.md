# Trabalho Prático — Testes de Componente em um Sistema de Conferência

## Objetivo

Neste trabalho, vocês receberão um pequeno sistema de conferência já implementado, contendo:

- código-fonte do subsistema;
- testes de unidade prontos;
- estrutura básica do projeto.

O trabalho de vocês será criar os **testes de componente** do sistema, utilizando `pytest`.

Os testes de componente devem verificar a colaboração real entre as classes do subsistema, cobrindo fluxos de negócio relevantes. Não é permitido transformar o trabalho em testes unitários disfarçados, nem substituir as classes internas do subsistema por mocks.

## Sistema

O sistema representa um pequeno subsistema de inscrição em workshops de uma conferência.

As classes principais do projeto são:

- `WorkshopRepository`
- `ParticipantRepository`
- `EnrollmentRepository`
- `WaitlistRepository`
- `ConferenceService`

## Regras de negócio

### Inscrição em workshop
Um participante pode se inscrever em um workshop somente se:

- o participante existir;
- o workshop existir;
- o participante não estiver bloqueado;
- o participante tiver a taxa do evento paga;
- o workshop estiver disponível;
- o participante tiver menos de 2 inscrições ativas;
- o workshop não estiver reservado para outro participante na fila de espera.

Quando a inscrição é feita com sucesso:

- o workshop deixa de estar disponível;
- a inscrição ativa é registrada;
- se o participante tinha fila de espera para esse workshop, sua entrada na fila deve ser removida.

### Cancelamento da inscrição
Ao cancelar uma inscrição:

- a inscrição ativa correspondente deve existir;
- a inscrição é encerrada;
- se não houver fila de espera para o workshop, ele volta a ficar disponível;
- se houver fila de espera, ele continua indisponível.

### Fila de espera
Um participante pode entrar na fila de espera de um workshop somente se:

- o participante existir;
- o workshop existir;
- o participante não estiver bloqueado;
- o participante tiver a taxa do evento paga;
- o workshop estiver indisponível;
- o participante não tiver uma entrada duplicada na fila para o mesmo workshop;
- o participante não for quem já está inscrito no workshop.

A fila deve respeitar a ordem de chegada.

## Tarefa

Criem os testes de componente em:

```text
tests/components/
```

Sugestão de arquivo:

```text
tests/components/test_conference_component.py
```

## Quantidade esperada
Espera-se entre **10 e 12 testes de componente**.

## Cenários mínimos obrigatórios

1. inscrição com sucesso;
2. inscrição em workshop inexistente;
3. inscrição por participante inexistente;
4. inscrição bloqueada por taxa não paga;
5. inscrição bloqueada por participante bloqueado;
6. inscrição bloqueada por limite de 2 inscrições ativas;
7. entrada na fila de espera com sucesso para workshop indisponível;
8. tentativa de fila duplicada;
9. cancelamento simples sem fila de espera;
10. cancelamento com fila de espera, mantendo o workshop indisponível;
11. inscrição bem-sucedida por participante que tinha fila de espera para o mesmo workshop, removendo a fila;
12. sequência completa: inscrição → fila de espera por outro participante → cancelamento → tentativa de nova inscrição.

## Requisitos de qualidade

Os testes devem:

- usar as classes reais do subsistema;
- refletir fluxos de negócio;
- ser legíveis e bem nomeados;
- evitar duplicação excessiva;
- ser determinísticos.

## Execução

Para executar os testes de unidade:

```bash
pytest tests/unit
```

Para executar todos os testes:

```bash
pytest
```
